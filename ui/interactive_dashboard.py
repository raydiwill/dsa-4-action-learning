from utils import *
import streamlit as st


dashboard_links = {
    "Model Predictions": "http://localhost:3000/public-dashboards/39717711dbca4123a5ebaeeaffc89633",
    "Customers Profiling": "http://localhost:3000/goto/8---r-pIR?orgId=1",
    "Data Quality": "http://localhost:3000/goto/i9Rn_-pSg?orgId=1",
    "Monitoring Performance": "http://localhost:3000/goto/ceBH6apIg?orgId=1",
}


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
            database_uri = settings.DATABASE_URL
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
