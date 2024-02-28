FROM python:3.10-slim

RUN mkdir -p /opt/dagster/dagster_home /opt/dagster/app
WORKDIR /opt/dagster/app

# COPY repo.py workspace.yaml /opt/dagster/app/

ENV DAGSTER_HOME=/opt/dagster/dagster_home/

# COPY dagster.yaml /opt/dagster/dagster_home/

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
