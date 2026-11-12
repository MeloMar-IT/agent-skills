from prometheus_client import Counter, Histogram

SEARCH_DURATION = Histogram(
    "search_request_duration_seconds",
    "Search request latency",
    ["route"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5),
)
SEARCH_REQUESTS = Counter("search_requests_total", "Search requests", ["route", "code"])
