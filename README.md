EPITA 2023-2024 Action Learning project
=====

### Collaborators
* Khanh Duong Tran
* Johnfredrick Owotorufa
* Shashank Vaidya

Welcome to our immersive journey in Data Science! In this project, we delve into the dynamic landscape of Telecommunication Churn Prediction, combining the prowess of Machine Learning (ML) with cutting-edge technologies to empower companies in anticipating and mitigating customer attrition.

## Project Overview
In today's competitive Telecommunication industry, understanding and predicting customer behavior are paramount. The ability to foresee when a customer might decide to part ways with a company provides an invaluable opportunity for proactive engagement and retention strategies. Our project centers around the development of a sophisticated ML-driven application, acting as a predictive model for banks to identify potential churn factors and take preemptive actions.

## Dataset Exploration
The dataset can be found here: 

*
*
*
* Further details regarding each column can be found in the description section on Kaggle.

## Main Technologies
Embark on a journey through the core components of our project:

* __User Interface (UI)__: Streamlit: Experience a user-friendly interface where predictions are made effortlessly.
  
* __Model Service (API)__: FastAPI: Our go-to solution for exposing the ML model, handling predictions, and seamlessly interacting with the web application.
  
* __Database__: PostgreSQL, SQLAlchemy: The reliable keeper of records, storing past predictions and diligently tracking data quality issues.
  
* __Data Ingestion Job__: Airflow, Great Expectations: A continuous process that hungers for fresh data, ensuring its quality and reliability for our predictive model.
  
* __Prediction Job__: Airflow: The automaton of predictions, scanning for new data and orchestrating the forecasting process every two minutes.
  
* __Monitoring Dashboard__: Grafana: A vigilant guardian, monitoring data quality and model prediction issues through insightful charts.

## Installation and Setup
1. __Initial Installation__: Install project dependencies:<br>
   `pip install -r requirements.txt`

2. __Install Docker and Docker Compose__ (Docker Desktop is additional)

3. __Build Docker image and start services__:<br>
   `cd airflow`<br>
   `docker build -f Dockerfile -t {name_of_the_image}:latest .`<br>
   `docker-compose -f "docker-compose.yml" up -d --build `

## Running Steps
   1. __Run the FastAPI main.py for the API__:<br>
     `cd main`<br>
     `uvicorn main:app --reload`

   2. __Run the Streamlit app.py file for the webapp__:<br>
      `cd interface`<br>
      `streamlit run app.py`

   3. __Generate csv files for the DAG jobs__:<br>
      `# Root directory`<br>
      `python generate_files.py`

## Accessing Front-end:
For the webapp, go to localhost:8501.

## Accessing Airflow:

* Go to localhost:8080
* Retrieve the Airflow admin password from the standalone_admin_password file, and use the username admin.
