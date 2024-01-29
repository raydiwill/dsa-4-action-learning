# import necessary libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Function to fetch data from PostgreSQL
def fetch_data_from_postgresql():
    # Replace these values with your PostgreSQL database connection details
    db_config = {
        "user": "postgres",
        "password": "0",
        "host": "your_host",
        "port": "your_port",
        "database": "your_database"
    }

    # Create a connection to the PostgreSQL database
    engine = create_engine(f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

    # Query to fetch data from the table (replace 'your_table_name' with your actual table name)
    query = "SELECT * FROM your_table_name"

    # Fetch data into a DataFrame
    df = pd.read_sql(query, engine)

    # Close the database connection
    engine.dispose()

    return df

# Function to simulate submitting feedback from the CS Team
def submit_feedback(selected_customers, feedback):
    # Dummy logic for submitting feedback (for demonstration purposes)
    for customer_id in selected_customers:
        st.success(f"Feedback submitted for Customer ID: {customer_id}")

# Function to filter customers based on risk level
def filter_customers_by_risk(past_predictions, risk_level):
    return [customer for customer in past_predictions if customer['risk_level'].lower() == risk_level.lower()]

# Streamlit Past Predictions Page
def past_predictions_page():
    st.title("Past Predictions")

    # Fetch data from PostgreSQL instead of using dummy data
    past_predictions = fetch_data_from_postgresql()

    # Display a table with fetched data
    st.table(past_predictions)

    # Filter customers based on risk level
    risk_level_filter = st.selectbox("Filter by Risk Level:", ["All", "High", "Low"])
    if risk_level_filter != "All":
        filtered_customers = filter_customers_by_risk(past_predictions, risk_level_filter)

        # Display a different table for filtered customers
        st.subheader(f"Filtered Customers (Risk Level: {risk_level_filter}):")
        filtered_df = pd.DataFrame(filtered_customers)
        st.table(filtered_df)

        # Selection mechanism
        selected_customers = st.multiselect("Select customers to provide feedback:", filtered_df["customer_id"].tolist())

        # Confirm selected choices with a button
        if st.button("Confirm Selected Customers"):
            # Popup for feedback
            feedback_text = st.text_area("Provide Feedback:")
            if st.button("Submit Feedback"):
                submit_feedback(selected_customers, feedback_text)

# Main Streamlit App
def main():
    st.set_page_config(page_title="Churn Prediction Platform", page_icon="📊")

    page = st.sidebar.selectbox("Select a page:", ["Past Predictions"])

    if page == "Past Predictions":
        past_predictions_page()

# Run the Streamlit app
if __name__ == "__main__":
    main()
