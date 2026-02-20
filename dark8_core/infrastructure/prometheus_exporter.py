"""
Simple Prometheus exporter for DARK8 monitoring (text exposition format)
This is a lightweight exporter using Python stdlib only.
"""
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import request
from typing import Dict
import sys
import os

# Ensure project root is on sys.path when executed as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def _load_monitoring():
    # Try multiple strategies to import the monitoring module without triggering
    # package-level side effects (like dotenv imports in package __init__).
    try:
        import importlib
        mod = importlib.import_module('.monitoring', package='dark8_core.infrastructure')
        return mod
    except Exception:
        pass

    try:
        import importlib
        mod = importlib.import_module('dark8_core.infrastructure.monitoring')
        return mod
    except Exception:
        pass

    # Fallback: load module directly from file path to avoid package imports
    import importlib.util
    mod_path = os.path.join(os.path.dirname(__file__), 'monitoring.py')
    spec = importlib.util.spec_from_file_location('dark8_monitoring', mod_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_monitoring_mod = _load_monitoring()
MetricsCollector = getattr(_monitoring_mod, 'MetricsCollector')
Metric = getattr(_monitoring_mod, 'Metric')
MetricType = getattr(_monitoring_mod, 'MetricType')


class _MetricsHandler(BaseHTTPRequestHandler):
    collector: MetricsCollector = None

    def do_GET(self):
        if self.path != '/metrics':
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return

        output = []
        # Simple exposition: for each metric name, expose the last value
        for name, metrics in list(self.collector.metric_registry.items()):
            if not metrics:
                continue
            latest: Metric = metrics[-1]
            metric_type = 'gauge' if latest.type.name == 'GAUGE' else 'counter'
            # help and type
            output.append(f"# HELP {name} DARK8 metric {name}")
            output.append(f"# TYPE {name} {metric_type}")
            # labels
            if latest.labels:
                labels = ','.join(f'{k}=\"{v}\"' for k, v in latest.labels.items())
                output.append(f"{name}{{{labels}}} {latest.value}")
            else:
                output.append(f"{name} {latest.value}")

        body = "\n".join(output).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; version=0.0.4')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class PrometheusExporter:
    def __init__(self, collector: MetricsCollector = None, host: str = '0.0.0.0', port: int = 9100):
        self.collector = collector or MetricsCollector()
        self.host = host
        self.port = port
        self._server = None

    def start(self):
        handler = _MetricsHandler
        handler.collector = self.collector
        self._server = HTTPServer((self.host, self.port), handler)

        def _run():
            try:
                self._server.serve_forever()
            except Exception:
                pass

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        return t

    def stop(self):
        if self._server:
            self._server.shutdown()


def test_exporter():
    collector = MetricsCollector()
    # populate some metrics
    for i in range(5):
        m = Metric(
            name='http_requests_total',
            type=MetricType.COUNTER,
            value=float(i * 10),
            labels={'job': 'api', 'instance': 'exporter-1'},
            unit='requests'
        )
        collector.record_metric(m)

    exporter = PrometheusExporter(collector=collector, host='127.0.0.1', port=9100)
    exporter.start()
    time.sleep(0.1)

    # fetch metrics
    try:
        resp = request.urlopen('http://127.0.0.1:9100/metrics', timeout=2)
        data = resp.read().decode('utf-8')
        print("---EXPORTER_OUTPUT_START---")
        print(data)
        print("---EXPORTER_OUTPUT_END---")
    except Exception as e:
        print(f"Exporter fetch error: {e}")

    exporter.stop()


if __name__ == '__main__':
    test_exporter()
