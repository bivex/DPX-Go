"""Tests for DPX-Go application scanning and formatting services."""

from pattern_detector.adapters.outbound.persistence.html_report_formatter import HtmlReportFormatter
from pattern_detector.adapters.outbound.persistence.json_report_formatter import JsonReportFormatter
from pattern_detector.adapters.outbound.persistence.sarif_report_formatter import SarifReportFormatter
from pattern_detector.bootstrap.container import create_container
from pattern_detector.ports.inbound import ScanOptions


def test_scanning_service_memory():
    container = create_container()
    scanner = container.get_scanner()

    code = """package demo

type WorkerPool struct {
    jobs chan int
}
"""
    report = scanner.scan_sources({"demo.go": code})
    assert report.scanned_files_count == 1
    assert report.total_detections_count >= 1

    # Test Formatters
    json_fmt = JsonReportFormatter()
    json_str = json_fmt.format(report)
    assert '"scanned_files_count": 1' in json_str

    sarif_fmt = SarifReportFormatter()
    sarif_str = sarif_fmt.format(report)
    assert "DPX-Go" in sarif_str

    html_fmt = HtmlReportFormatter()
    html_str = html_fmt.format(report)
    assert "<!DOCTYPE html>" in html_str
    assert "Copy Architecture Map for LLM" in html_str
