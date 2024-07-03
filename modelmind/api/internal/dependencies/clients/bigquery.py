from fastapi import Request
from google.cloud import bigquery


def get_bigquery_client(request: Request) -> bigquery.Client:
    return request.app.state.bigquery
