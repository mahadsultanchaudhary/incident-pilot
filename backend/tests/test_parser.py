import unittest
from app.parser import LogParser, RequestCorrelator, StackTraceExtractor
from app.models import LogEvent


class ParserTests(unittest.TestCase):
    def test_json_log_normalizes_context(self):
        event = LogParser().parse('{"level":"error","service":"checkout-api","message":"timeout"}')
        self.assertEqual(event["level"], "ERROR")
        self.assertEqual(event["service"], "checkout-api")

    def test_stack_trace_extracts_terminal_exception(self):
        trace = 'File "worker.py", line 12, in execute\nTimeoutError: payment dependency timed out'
        extracted = StackTraceExtractor().extract(trace)
        self.assertEqual(extracted["exception"], "TimeoutError")
        self.assertEqual(extracted["frames"][0]["line"], 12)

    def test_correlator_groups_by_correlation_id(self):
        first = LogEvent(level="ERROR", service="checkout-api", message="failed", correlation_id="corr-1")
        second = LogEvent(level="INFO", service="checkout-api", message="started", correlation_id="corr-1")
        self.assertEqual(len(RequestCorrelator().group([first, second])["corr-1"]), 2)


if __name__ == "__main__":
    unittest.main()
