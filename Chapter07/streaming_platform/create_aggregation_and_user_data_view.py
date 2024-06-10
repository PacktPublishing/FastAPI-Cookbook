from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")


pipeline_redact = {
    "$redact": {
        "$cond": {
            "if": {
                "$eq": ["$consent_to_share_data", True]
            },
            "then": "$$KEEP",
            "else": "$$PRUNE",
        }
    }
}


pipeline_remove_email_and_name = {"$unset": ["email", "name"]}


obfuscate_day_of_date = {
    "$concat": [
        {
            "$substrCP": [
                "$$action.date",
                0,
                7,
            ]
        },
        "-XX",
    ]
}

rebuild_actions_elements = {
    "input": "$actions",
    "as": "action",
    "in": {
        "$mergeObjects": [
            "$$action",
            {"date": obfuscate_day_of_date},
        ]
    },
}


pipeline_set_actions = {
    "$set": {
        "actions": {"$map": rebuild_actions_elements},
    }
}


pipeline = [
    pipeline_redact,
    pipeline_remove_email_and_name,
    pipeline_set_actions,
]


if __name__ == "__main__":
    client["beat_streaming"].drop_collection(
        "users_data_view"
    )

    client["beat_streaming"].create_collection(
        "users_data_view",
        viewOn="users",
        pipeline=pipeline,
    )
