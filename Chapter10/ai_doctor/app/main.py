from huggingface_hub import hf_hub_download
import joblib
from typing import Annotated
from pydantic import create_model
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.utils import symptoms_list

ml_model = {}
REPO_ID = "AWeirdDev/human-disease-prediction"
FILENAME = "sklearn_model.joblib"


@asynccontextmanager
async def lifespan(app: FastAPI):
    ml_model["doctor"] = joblib.load(
        hf_hub_download(
            repo_id=REPO_ID, filename=FILENAME
        )
    )

    yield
    ml_model.clear()


app = FastAPI(title="AI Doctor", lifespan=lifespan)


query_params = {
    symp: (bool, False)
    for symp in symptoms_list[:10]
}

Symptoms = create_model("Symptoms", **query_params)


@app.get("/diagnosis")
async def get_diagnosis(
    symptoms: Annotated[Symptoms, Depends()],
):
    array = [
        int(value)
        for _, value in symptoms.model_dump().items()
    ]
    array.extend(  # adapt the array to the model's input shape
        [0] * (len(symptoms_list) - len(array))
    )
    len(symptoms_list)
    diseases = ml_model["doctor"].predict([array])
    return {
        "diseases": [disease for disease in diseases]
    }
