"""
HttpRunner report

- summarize: aggregate test stat data to summary
- stringify: stringify summary, in order to dump json file and generate html report.
- html: render html report
"""

from app.libs.httprunner.report.html import HtmlTestResult, gen_html_report
from app.libs.httprunner.report.stringify import stringify_summary
from app.libs.httprunner.report.summarize import (
    aggregate_stat,
    get_platform,
    get_summary,
)

__all__ = [
    "get_platform",
    "aggregate_stat",
    "get_summary",
    "stringify_summary",
    "HtmlTestResult",
    "gen_html_report",
]
