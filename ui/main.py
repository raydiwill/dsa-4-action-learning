from chatbot import chatbot_ui
from interactive_dashboard import interactive_dashboard_page
from utils import *
import datetime
import streamlit as st
import pandas as pd


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
        "limit": 25,
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


def send_recommendations_page():
    st.title("Send Recommendation to Customer Service")

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

    to_address = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    if st.button("Send Email"):
        if send_email(user_email, to_address, subject, message):
            print("Sent!")
        st.toast("Email sent successfully.", icon="🎉")


def main():
    st.set_page_config(page_title="Churn Prediction Platform", page_icon="📊")

    # Check if the user is logged in
    if not is_user_logged_in():
        # Display login page if not logged in
        display_login_page()
        return

    # Define the chatbot toggle state in the session
    if "show_chatbot" not in st.session_state:
        st.session_state["show_chatbot"] = False

    page = st.sidebar.selectbox(
        "Select a page:",
        ["Interactive Dashboard", "Past Predictions", "Send Recommendations"],
    )

    if page == "Interactive Dashboard":
        interactive_dashboard_page()
    elif page == "Past Predictions":
        past_predictions_page(GET_URL)
    elif page == "Send Recommendations":
        send_recommendations_page()

    if st.session_state["show_chatbot"]:
        chatbot_ui()

    # Place an empty container at the bottom of the page
    chat_button_container = st.empty()

    # Inside the container, create the toggle chat button
    chat_button_container.button(
        "Toggle Chat",
        key="toggle_chat",
        on_click=lambda: st.session_state.update(
            show_chatbot=not st.session_state["show_chatbot"]
        ),
    )


if __name__ == "__main__":
    main()
