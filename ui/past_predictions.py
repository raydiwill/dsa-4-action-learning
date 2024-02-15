from utils import *
import streamlit as st
import datetime


def past_predictions_page(api_url):
    st.title("Past Predictions")

    # Check if the user is logged in
    if not is_user_logged_in():
        st.warning("Please log in to access this page.")
        return

    # Logout button
    if st.button("Logout"):
        # Clear session state to log out the user
        del st.session_state.is_logged_in
        st.success("Logout successful!")
        st.experimental_rerun()

    start_date = st.date_input("Start Date")
    today = datetime.date.today()
    end_date = st.date_input("End Date", max_value=today + datetime.timedelta(days=1))

    data = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "limit": st.number_input("Number of results:", min_value=1, value=25),
    }

    past_predictions = pd.DataFrame(fetch_data_from_api(api_url, data))

    # Display a table with fetched data
    st.table(past_predictions)

    # Filter customers based on risk level
    risk_level_filter = st.selectbox("Filter by Risk Level:", ["All", "High", "Low"])
    if risk_level_filter != "All":
        filtered_customers = past_predictions[
            past_predictions["pred_risk"].str.lower() == risk_level_filter.lower()
        ]

        # Display a different table for filtered customers
        st.subheader(f"Filtered Customers (Risk Level: {risk_level_filter}):")
        st.table(filtered_customers)

        # Selection mechanism
        selected_customers = st.multiselect(
            "Select customers to provide feedback:",
            filtered_customers["user_id"].tolist(),
        )
        st.write(selected_customers)

        feedback_text = st.text_area("Provide Feedback:")

        if st.button("Confirm Selected Customers"):
            st.write(selected_customers)

        if feedback_text and st.button("Submit Feedback"):
            submit_feedback(selected_customers, feedback_text)
            st.toast("Feedbacks sent!", icon="🎉")
