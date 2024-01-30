import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, update, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password"

def login():
    st.title("Login")
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful! You can now access all pages.")
        else:
            st.error("Invalid username or password. Please try again.")


dummy_prediction_data = {"user_id": 1, "prediction": "churn", "probability": 0.75}

dummy_past_predictions = [
    {"user_id": 1, "prediction": "churn", "actual_result": "non-churn", "risk_level": "high"},
    {"user_id": 2, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"user_id": 3, "prediction": "churn", "actual_result": "churn", "risk_level": "high"},
    {"user_id": 4, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"user_id": 5, "prediction": "churn", "actual_result": "churn", "risk_level": "high"}
]

def get_predictions():
    return dummy_prediction_data

class SessionState:
    def __init__(self):
        self.submitted_feedback = False

# Create a global variable to store session state
session_state = SessionState()

def submit_feedback(selected_customers, feedback):
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "localhost",
        "port": "5432",
        "database": "churn"
    }

    # Connection to the database
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Load table metadata
    metadata = MetaData()
    test_pred_table = Table('churn.test_pred', metadata, autoload_with=engine)

    # Initialize an empty list to store feedback
    feedback_list = []

    # Iterate over selected customers and update feedback in the database
    for user_id in selected_customers:
        feedback_data = {
            "user_id": user_id,
            "feedback": feedback
        }

        try:
            # Build the update statement
            stmt = (
                update(test_pred_table)
                .where(test_pred_table.c.user_id == feedback_data['user_id'])
                .values(feedback=feedback_data['feedback'])
            )

            # Execute the update statement
            result = engine.execute(stmt)

            # Check if the update was successful
            if result.rowcount > 0:
                feedback_list.append(f"Feedback updated for user {user_id}")
            else:
                feedback_list.append(f"No records updated for user {user_id}")

        except SQLAlchemyError as e:
            feedback_list.append(f"Error during update for user {user_id}: {e}")

    # Close the database connection
    engine.dispose()

    # Display feedback messages at the bottom of the Streamlit page
    st.write("Feedback submitted successfully.")
    for feedback_msg in feedback_list:
        st.write(feedback_msg)


def interactive_dashboard():
    st.title("Churn Prediction Dashboard")

    predictions = get_predictions()

    st.subheader("Analyze Returned Predictions:")
    st.write(f"Customer ID: {predictions['user_id']}")
    st.write(f"Prediction: {predictions['prediction']}")
    st.write(f"Probability: {predictions['probability']}")

    if predictions['prediction'] == 'churn' and predictions['probability'] > 0.5:
        st.warning("Churn predicted with high probability. Recommend retention strategies.")

    st.subheader("Customer Profiling:")
    # Add customer profiling details here

    st.subheader("CS Team Reports:")
    # Display feedback form here

def fetch_data_from_database():
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "localhost",
        "port": "5432",
        "database": "churn"
    }

    query = "SELECT * FROM churn.test_pred LIMIT 50"

    # Creating a connection to the database
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    df = pd.read_sql(query, engine)

    engine.dispose()

    return df

def filter_customers_by_risk(past_predictions, risk):
    return past_predictions[past_predictions['risk'].str.lower() == risk.lower()]

def past_predictions_page():
    st.title("Past Predictions")

    # Fetch data from the database
    past_predictions = fetch_data_from_database()

    # Display a table with fetched data
    st.table(past_predictions)

    # Filter customers based on risk level
    risk_level_filter = st.selectbox("Filter by Risk Level:", ["All", "High", "Low"])
    if risk_level_filter != "All":
        filtered_customers = filter_customers_by_risk(past_predictions, risk_level_filter)

        # Display a different table for filtered customers
        st.subheader(f"Filtered Customers (Risk Level: {risk_level_filter}):")
        st.table(filtered_customers)

        # Selection mechanism
        selected_customers = st.multiselect("Select customers to provide feedback:", filtered_customers["user_id"].tolist())

        # Confirm selected choices with a button
        if st.button("Confirm Selected Customers"):
            # Popup for feedback
            feedback_text = st.text_area("Provide Feedback:")

            # Check if feedback has already been submitted
            if not session_state.submitted_feedback:
                if st.button("Submit Feedback"):
                    submit_feedback(selected_customers, feedback_text)
                    session_state.submitted_feedback = True

def main():
    st.set_page_config(page_title="Churn Prediction Platform ", page_icon="📊")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        return

    page = st.sidebar.selectbox("Select a page:", ["Interactive Dashboard", "Past Predictions"])

    if page == "Interactive Dashboard":
        interactive_dashboard()
    elif page == "Past Predictions":
        past_predictions_page()

if __name__ == "__main__":
    main()
