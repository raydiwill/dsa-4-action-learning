EPITA 2023-2024 Action Learning project
=====

### Collaborators
* Khanh Duong Tran
* Johnfredrick Owotorufa
* Shashank Vaidya

Welcome to our EPITA Action Learning project! In this project, we delve into the dynamic landscape of Telecommunication Churn Prediction, combining the prowess of Deep Learning (DL) with cutting-edge technologies to empower companies in anticipating and mitigating customer attrition.

## Project Overview

In the dynamic landscape of the Telecommunication industry, understanding and predicting customer behavior are crucial. The power to anticipate when a customer might consider leaving a service provider opens doors to proactive engagement and retention strategies. Our project centers around the development of a sophisticated DL-driven application, acting as a predictive model for telecom company to identify potential churn factors and take decisive actions.

## Minimum Viable Product

Our MVP delivers real-time dashboards for monitoring key performance metrics and customer segmentation. It includes a recommendation engine for personalized retention strategies and an automation task to streamline monthly predictions. Additionally, it facilitates collaboration between analysts and customer support teams. While this MVP offers powerful retention tools, we have exciting plans for future development, including AI-driven personalized recommendations and an internal chatbot for enhanced insights.

## Dataset

The dataset can be found here: [Zindi Hackthon](https://zindi.africa/competitions/expresso-churn-prediction/data)

* The dataset contains data on 2.5 million Expresso clients from Senegal.
* It includes 19 columns, 17 features and 1 target variable called CHURN. 
* This is our foundation for the Exploratory Data Analysis step and DL model building phase.

## Main Technologies

Our project includes these core components designated for the Data Analysts in a telecom company:

* __User Interface (UI)__: Streamlit: A user-friendly interface where users are able to access for analysis purposes. Our UI offer:
  * Interactive Dashboard, monitoring model predictions, data quality issues, model monitoring performance, and customers profiling. It also has the option to show potential retention plans recommendation.
  * View Past Prediction, allow users to view past prediction made by the models, as well as enabling users to give feedbacks on the predictions.
  * Send Recommendation emails, where users can send recommendation emails advising potential retention strategies for the customer service teams as an example.
  
* __Model Service (API)__: FastAPI: An API serving the model, handling predictions, and querying data from a database.
  
* __Database__: PostgreSQL, SQLAlchemy: Store past predictions, data quality issues, customers reports from Customer Service teams and received feedbacks for the model.
  
* __Data Ingestion Job__: Airflow, Great Expectations: An ETL process that handle data validation, ensuring its quality and reliability for our predictive model.
  
* __Prediction Job__: Airflow: The automaton of predictions, scanning for new data and orchestrating the forecasting process.

## Installation and Setup

1. __Initial Installation__: Install project dependencies:

```bash
pip install -r requirements.txt
```

2. __Install Docker and Docker Compose__ (Docker Desktop is additional)

2. __Install Postgres database__
   
3. __Build Docker image and start services__:

It is needed to type the name of the image and modifying it in the yaml file.

```commandline
cd airflow
docker build -f Dockerfile -t {name_of_the_image}:latest . 
docker-compose -f "docker-compose.yml" up -d --build
```

4. __Create database, retrieve the password for user postgres__
5. __Download the Train and Test files from the above links__.

## Running Steps

   1. __Modify myenv.env the used user, password, and database.
   
   2. __Run the FastAPI main.py for the API__:
   
   ```commandline
   cd main
   uvicorn main:app --port 8050
   ```

   3. __Run the Streamlit app.py file for the webapp__:
   
   ```commandline
   cd interface
   streamlit run app.py
   ```

   4. __Generate csv files for the DAG jobs__:

   To run the scripts for data generation, create three folders *good*, *bad* and *default*. Put the csv files in the *data* folder.

   * For testing without data problems:

   ```commandline
   cd data
   python generate_sample.py
   ```

   * For testing with data problems:

   ```commandline
   cd data
   python generate_errors.py
   ```

## Accessing Front-end

For the streamlit webapp, go to localhost:8501. The login username and password is *admin*

The streamlit UI includes the dashboard widgets, however, if needed, Grafana UI can be accessed via localhost:3000.

![](https://github.com/raydiwill/dsa-4-action-learning/assets/97393390/0cf45fa1-397e-44f7-bcd8-26f62fd6bb01)

## Accessing Airflow:

* Go to localhost:8080.
* Retrieve the Airflow admin password from the standalone_admin_password file, and use the username admin.
* To run the jobs, it is needed to generate some dummy files from the previous step.


![](https://github.com/raydiwill/dsa-4-action-learning/assets/97393390/3fd0b789-c7ad-40a5-95ae-2b00eceef62a)