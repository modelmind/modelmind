from google.cloud import bigquery


class BigqueryClient(bigquery.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
