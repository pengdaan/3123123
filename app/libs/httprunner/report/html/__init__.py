"""
HttpRunner html report

- result: define resultclass for unittest TextTestRunner
- gen_report: render html report with jinja2 template

"""

from app.libs.httprunner.report.html.gen_report import gen_html_report
from app.libs.httprunner.report.html.result import HtmlTestResult

__all__ = ["HtmlTestResult", "gen_html_report"]
