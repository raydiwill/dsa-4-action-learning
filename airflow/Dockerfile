# Parent image
FROM apache/airflow:2.8.0

# Set config variables
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

# Install dependencies
COPY ../requirements.txt ./

# Install packages
RUN pip install --no-cache-dir apache-airflow==${AIRFLOW_VERSION} -r requirements.txt