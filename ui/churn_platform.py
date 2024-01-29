# import necessary libraries
import streamlit as st
import pandas as pd

# Dummy prediction data for demonstration purposes
dummy_prediction_data = {"customer_id": 1, "prediction": "churn", "probability": 0.75}

# Dummy past prediction data for demonstration purposes
dummy_past_predictions = [
    {"customer_id": 1, "prediction": "churn", "actual_result": "non-churn", "risk_level": "high"},
    {"customer_id": 2, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"customer_id": 3, "prediction": "churn", "actual_result": "churn", "risk_level": "high"},
    {"customer_id": 4, "prediction": "non-churn", "actual_result": "non-churn", "risk_level": "low"},
    {"customer_id": 5, "prediction": "churn", "actual_result": "churn", "risk_level": "high"}
]

# Function to simulate fetching predictions from the API
def get_predictions():
    # Return dummy prediction data
    return dummy_prediction_data

# Function to simulate submitting feedback from the CS Team
def submit_feedback(prediction_id, feedback):
    # Dummy logic for submitting feedback (for demonstration purposes)
    pass

# Function to filter customers based on risk level
def filter_customers_by_risk(past_predictions, risk_level):
    return [customer for customer in past_predictions if customer['risk_level'].lower() == risk_level.lower()]

# Streamlit Interactive Dashboard
def interactive_dashboard():
    st.title("Churn Prediction Dashboard")

    # Fetch predictions
    predictions = get_predictions()

    st.subheader("Analyze Returned Predictions:")
    st.write(f"Customer ID: {predictions['customer_id']}")
    st.write(f"Prediction: {predictions['prediction']}")
    st.write(f"Probability: {predictions['probability']}")

    # Recommendation based on prediction
    if predictions['prediction'] == 'churn' and predictions['probability'] > 0.5:
        st.warning("Churn predicted with high probability. Recommend retention strategies.")

    st.subheader("Customer Profiling:")
    # Add customer profiling details here

    st.subheader("CS Team Reports:")
    # Display feedback form here

# Streamlit Past Predictions Page
def past_predictions_page():
    st.title("Past Predictions")

    # Fetch and display past predictions
    past_predictions = dummy_past_predictions

    # Display a table with dummy customer details
    df = pd.DataFrame(past_predictions)
    st.table(df)

    # Filter customers based on risk level
    risk_level_filter = st.selectbox("Filter by Risk Level:", ["All", "High", "Low"])
    if risk_level_filter != "All":
        filtered_customers = filter_customers_by_risk(past_predictions, risk_level_filter)

        # Display a different table for filtered customers
        st.subheader(f"Filtered Customers (Risk Level: {risk_level_filter}):")

        if not filtered_customers:
            st.warning("No customers found for the selected risk level.")
        else:
            filtered_df = pd.DataFrame(filtered_customers)
            st.table(filtered_df)

# Streamlit Feedback Page
def feedback_page():
    st.title("Feedback from Customer Service Team")

    prediction_id = st.text_input("Enter Prediction ID:")
    feedback_text = st.text_area("Provide Feedback:")

    if st.button("Submit Feedback"):
        submit_feedback(prediction_id, feedback_text)
        st.success("Feedback submitted successfully.")

# Main Streamlit App
def main():
    st.set_page_config(page_title="Churn Prediction Platform", page_icon="📊")

    page = st.sidebar.selectbox("Select a page:", ["Interactive Dashboard", "Past Predictions", "Feedback"])

    if page == "Interactive Dashboard":
        interactive_dashboard()
    elif page == "Past Predictions":
        past_predictions_page()
    elif page == "Feedback":
        feedback_page()

# Run the Streamlit app
if __name__ == "__main__":
    main()
