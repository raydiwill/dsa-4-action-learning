from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import and_
from models import Base, CustomerModel
from setup_db import *
from schema import CustomerData
from datetime import datetime
from tensorflow.keras.models import load_model
from typing import List
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
async def predict(data: List[CustomerData],
                  db: SessionLocal = Depends(get_db)):
    # Convert the list of Pydantic models to a list of dictionaries
    data_dicts = [item.dict() for item in data]

    # Create a DataFrame from the list of dictionaries
    input_data = pd.DataFrame(data_dicts)
    input_data.drop(columns=["user_id"], inplace=True, errors="ignore")

    # Perform preprocessing on the entire DataFrame
    processed_data = preprocessor.transform(input_data)

    # Perform prediction on the preprocessed data
    prediction_results = model.predict([processed_data, processed_data])

    results = []
    # Process each prediction result and update the database
    for idx, prediction in enumerate(prediction_results):
        pred_prob = float(prediction[0])

        churn = 1 if pred_prob > 0.4 else 0
        risk = "High" if pred_prob > 0.75 \
            else "Low" if pred_prob > 0.4 \
            else "No"
        customer_data = data_dicts[idx]
        customer_data.update({"pred_probability": pred_prob,
                              "pred_churn": churn,
                              "pred_risk": risk})

        # Create and add CustomerModel instance to database
        customer = CustomerModel(**customer_data)
        db.add(customer)
        results.append(customer_data)

    # Commit the changes to the database
    db.commit()

    # Return the prediction results
    return {"predictions": results}


@app.get('/past-predictions/')
def get_predict(data: dict, db: SessionLocal = Depends(get_db)):
    start_date = data["start_date"]
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = data["end_date"]
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    query = db.query(CustomerModel).filter(
        and_(CustomerModel.pred_date >= start_date,
             CustomerModel.pred_date < end_date)
    )
    limit = data["limit"]
    if limit is not None:
        query = query.limit(limit)

    predictions = query.all()
    return predictions


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8050, reload=True)
