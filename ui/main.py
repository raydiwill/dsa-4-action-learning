from interactive_dashboard import interactive_dashboard_page
from past_predictions import past_predictions_page
from send_recommendations import send_recommendations_page
from chatbot import chatbot_ui
from utils import *
import streamlit as st


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
