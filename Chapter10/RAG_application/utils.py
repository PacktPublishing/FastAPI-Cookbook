def format_docs(docs):
    return "\n\n".join(
        [d.page_content for d in docs]
    )
