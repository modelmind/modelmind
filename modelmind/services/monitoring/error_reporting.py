from google.api_core.exceptions import InvalidArgument
from google.cloud import error_reporting
from google.cloud.error_reporting import HTTPContext


class ErrorReporting:
    def __init__(self, service: str):
        self.client = error_reporting.Client(service=service)

    def report_exception(self, context: HTTPContext) -> None:
        try:
            self.client.report_exception(http_context=context)
        except InvalidArgument as e:
            print(f"Error reporting failed: {e}")
