//! Prometheus metrics for AI Product Pipeline

use prometheus::{
    Counter, Encoder, Histogram, HistogramOpts, IntCounterVec, Opts, Registry, TextEncoder,
};
use std::sync::OnceLock;

static REGISTRY: OnceLock<Registry> = OnceLock::new();
static REQUEST_COUNTER: OnceLock<IntCounterVec> = OnceLock::new();
static LATENCY_HISTOGRAM: OnceLock<Histogram> = OnceLock::new();

/// Initialize metrics registry
pub fn init_metrics() {
    let registry = Registry::new();

    // Request counter
    let request_counter = IntCounterVec::new(
        Opts::new("pipeline_requests_total", "Total number of requests"),
        &["endpoint"],
    )
    .expect("Failed to create request counter");

    // Latency histogram
    let latency_histogram = Histogram::with_opts(
        HistogramOpts::new("pipeline_request_duration_seconds", "Request latency in seconds")
            .buckets(vec![0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]),
    )
    .expect("Failed to create latency histogram");

    registry
        .register(Box::new(request_counter.clone()))
        .expect("Failed to register request counter");
    registry
        .register(Box::new(latency_histogram.clone()))
        .expect("Failed to register latency histogram");

    REGISTRY.set(registry).ok();
    REQUEST_COUNTER.set(request_counter).ok();
    LATENCY_HISTOGRAM.set(latency_histogram).ok();
}

/// Increment request counter
pub fn increment_requests(endpoint: &str) {
    if let Some(counter) = REQUEST_COUNTER.get() {
        counter.with_label_values(&[endpoint]).inc();
    }
}

/// Observe request latency
pub fn observe_latency(endpoint: &str, duration: f64) {
    if let Some(histogram) = LATENCY_HISTOGRAM.get() {
        histogram.observe(duration);
    }
}

/// Gather all metrics as Prometheus text format
pub fn gather_metrics() -> String {
    let registry = REGISTRY.get().expect("Metrics not initialized");
    let encoder = TextEncoder::new();
    let metric_families = registry.gather();
    let mut buffer = Vec::new();
    encoder.encode(&metric_families, &mut buffer).unwrap();
    String::from_utf8(buffer).unwrap()
}
