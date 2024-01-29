from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from models import Base, CustomerModel, ProblemStats, CustomerReport
from setup_db import *
from schema import CustomerData
from datetime import datetime
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import uvicorn


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    application = FastAPI(title=settings.PROJECT_NAME,
                          version=settings.PROJECT_VERSION)
    create_tables()
    return application


app = start_application()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("../models/ensemble.h5")
preprocessor = joblib.load("../notebooks/preprocessor.joblib")


@app.post("/predict/")
async def predict(data: CustomerData, db: SessionLocal = Depends(get_db)):
    customer = CustomerModel(**data.dict())

    # Convert Pydantic model to DataFrame
    input_data = pd.DataFrame([data.dict()])
    input_data.drop(
        columns=["user_id"], inplace=True, errors="ignore")

    # Perform prediction
    input_data = preprocessor.transform(input_data)
    prediction_result = model.predict([input_data, input_data])
    for lst in prediction_result.tolist():
        i = lst[0]
        customer.pred_probability = i
        if i > 0.75:
            customer.pred_churn = 1
            customer.pred_risk = "High"
        elif i > 0.4:
            customer.pred_churn = 1
            customer.pred_risk = "Low"

        customer.pred_churn = 0
        customer.pred_risk = "No"

    db.add(customer)
    db.commit()
    print(prediction_result)
    return {"prediction": prediction_result.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8050)
