#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import os
import re

import sublime_plugin


class GitOperateCommand(sublime_plugin.TextCommand):

    def run(self, edit, action):
        """ action: add/rm """
        window = self.view.window()
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        print("filename: ", filename)
        os.chdir(dirname)
        basename = os.path.basename(filename)
        cmd = "git %s -f %s " % (action, basename)
        print("run cmd: ", cmd)
        status, output = subprocess.getstatusoutput(
            cmd)
        if status == 0:
            print("run cmd succeed, output:", output)
        else:
            print("run cmd failed, status: ", status, ", output: ", output)

        if re.match(r'rm\b', action):
            print("remove file: ", basename)
            os.remove(filename)
        window.run_command("show_panel", {"panel": "console"})
