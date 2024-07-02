from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

tracer_provider = TracerProvider()
tracer_provider = BatchSpanProcessor(CloudTraceSpanExporter())  # type: ignore
trace.set_tracer_provider(TracerProvider())
