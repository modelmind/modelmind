import uuid

from opentelemetry import metrics, trace
from opentelemetry.exporter.cloud_monitoring import CloudMonitoringMetricsExporter
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.cloud_trace_propagator import CloudTraceFormatPropagator
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics._internal.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from modelmind.config import PACKAGE_NAME, settings

set_global_textmap(CloudTraceFormatPropagator())

resource = Resource.create(
    {
        "service.name": PACKAGE_NAME,
        "service.namespace": settings.environment.value,
        "service.instance.id": uuid.uuid4().hex,
    }
)

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(CloudTraceSpanExporter()))  # type: ignore
meter_provider = MeterProvider(
    metric_readers=[
        PeriodicExportingMetricReader(
            CloudMonitoringMetricsExporter(),
            export_interval_millis=5000,
        )
    ],
    resource=resource,
)

trace.set_tracer_provider(tracer_provider)
metrics.set_meter_provider(meter_provider)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)
