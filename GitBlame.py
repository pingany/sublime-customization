# coding: utf-8

import subprocess
import os
import shlex
import tempfile
import re

import sublime_plugin


class GitBlameCommand(sublime_plugin.TextCommand):

    def run(self, edit, see_commit=True):
        window = self.view.window()
        filename = self.view.file_name()
        dirname = os.path.dirname(filename)
        print("filename:", filename)
        os.chdir(dirname)
        proc = subprocess.Popen(
            ["git", "blame", os.path.basename(filename)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        lines, err = proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(
                "run git blame failed: returncode: %s, stderr log: %s" %
                (proc.returncode, err))
        lines = lines.decode("utf-8")
        lines = re.split(r'\r?\n', lines)
        current_lineno, current_columnno = self.view.rowcol(self.view.sel()[0].begin())
        # print(current_lineno)
        # print(current_columnno)
        if current_lineno < len(lines):
            # print(lines[current_lineno])
            if see_commit:
                line = lines[current_lineno]
                commit = re.split(r'\s', line, 1)[0]
                commit_content = subprocess.Popen(shlex.split(
                    "git log -p -n 1 %s" % str(commit)),
                    stdout=subprocess.PIPE).communicate()[0]
                newfile = tempfile.NamedTemporaryFile(suffix=".diff", delete=False)
                newfile.write(commit_content)
                newfile.close()
                newview = window.open_file(newfile.name)
                newview.set_read_only(True)
                newview.set_syntax_file('Packages/Diff/Diff.tmLanguage')
        else:
            print("not found lines")
        # window.run_command("show_panel", {"panel": "console"})
