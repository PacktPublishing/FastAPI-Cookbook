from huggingface_hub import hf_hub_download
import joblib
from typing import Annotated
from pydantic import create_model
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.utils import symptoms as symptoms_list

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


app = FastAPI(title="Doctor AI", lifespan=lifespan)


query_params = {
    symp: (bool, False) for symp in symptoms_list[:2]
}

symptoms_model = create_model(
    "Symptoms", **query_params
)


@app.get("/diagnosis")
async def get_diagnosis(
    symptoms: Annotated[symptoms_model, Depends()],
):
    array = [
        int(value)
        for key, value in symptoms.model_dump().items()
    ]
    print("stop here")
    desease = ml_model["doctor"].predict([array])
    return {"disease": desease[0]}
