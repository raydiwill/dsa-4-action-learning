from chatbot import chatbot_ui
from utils import *
import datetime
import streamlit as st
import pandas as pd


def interactive_dashboard_page():
    st.title("Churn Prediction Dashboard")

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

    dashboard_links = {
        "Model Predictions": "http://localhost:3000/public-dashboards/39717711dbca4123a5ebaeeaffc89633",
        "Customers Profiling": "http://localhost:3000/goto/8---r-pIR?orgId=1",
        "Data Quality": "http://localhost:3000/goto/i9Rn_-pSg?orgId=1",
        "Monitoring Performance": "http://localhost:3000/goto/ceBH6apIg?orgId=1",
    }

    # Selection box for choosing the dashboard
    dashboard = st.selectbox(
        "Which dashboard?",
        (
            "Model Predictions",
            "Customers Profiling",
            "Data Quality",
            "Monitoring Performance",
        ),
    )

    # Display the selected dashboard
    st.write("You selected:", dashboard)
    st.markdown(
        f'<iframe src="{dashboard_links[dashboard]}" width="600" height="600"></iframe>',
        unsafe_allow_html=True,
    )

    if dashboard == "Monitoring Performance":
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        if uploaded_file is not None:
            # Read the uploaded CSV file into a DataFrame
            data = pd.read_csv(uploaded_file)
            database_uri = "postgresql://postgres:khanhduong@localhost:5432/dl"
            table_name = "customers_report"

            save_to_database(data, table_name, database_uri)
            st.success("Data saved to database successfully!")

    # Provide a clickable link to the selected dashboard
    if dashboard in dashboard_links:
        url = dashboard_links[dashboard]
        st.markdown(f"[Go to {dashboard} Dashboard]({url})", unsafe_allow_html=True)

    if dashboard == "Model Predictions":
        if st.button("Generate Retention Recommendations"):
            # Call the function to generate recommendations
            recommendations = generate_recommendations()

            # Display each recommendation
            st.subheader("Recommended Retention Strategies:")
            for rec in recommendations:
                st.write(rec)
        else:
            st.write("Click the button to generate retention strategies.")


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
