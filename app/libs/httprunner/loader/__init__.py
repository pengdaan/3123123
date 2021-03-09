"""
HttpRunner loader

- check: validate api/testcase/testsuite data structure with JSON schema
- locate: locate debugtalk.py, make it's dir as project root path
- load: load testcase files and relevant data, including debugtalk.py, .env, yaml/json api/testcases, csv, etc.
- buildup: assemble loaded content to httprunner testcase/testsuite data structure

"""

from app.libs.httprunner.loader.buildup import load_cases, load_project_data
from app.libs.httprunner.loader.check import (
    JsonSchemaChecker,
    is_test_content,
    is_test_path,
)
from app.libs.httprunner.loader.load import load_builtin_functions, load_csv_file
from app.libs.httprunner.loader.locate import get_project_working_directory as get_pwd
from app.libs.httprunner.loader.locate import init_project_working_directory as init_pwd

__all__ = [
    "is_test_path",
    "is_test_content",
    "JsonSchemaChecker",
    "get_pwd",
    "init_pwd",
    "load_csv_file",
    "load_builtin_functions",
    "load_project_data",
    "load_cases",
]
