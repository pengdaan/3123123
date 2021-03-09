#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@文件        :runCode.py
@说明        :
@时间        :2020/08/17 11:13:06
@作者        :Leo
@版本        :1.0
"""

import os
import shutil
import subprocess
import sys
import tempfile

from app.libs import run

EXEC = sys.executable

if "uwsgi" in EXEC:
    EXEC = "/usr/bin/python3"


class DebugCode(object):
    def __init__(self, code):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix="FasterRunner")

    def run(self):
        """dumps debugtalk.py and run"""
        try:
            file_path = os.path.join(self.temp, "debugtalk.py")
            run.FileLoader.dump_python_file(file_path, self.__code)
            self.resp = decode(
                subprocess.check_output(
                    [EXEC, file_path], stderr=subprocess.STDOUT, timeout=60
                )
            )

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = "RunnerTimeOut"

        shutil.rmtree(self.temp)


def decode(s):
    try:
        return s.decode("utf-8")

    except UnicodeDecodeError:
        return s.decode("gbk")
