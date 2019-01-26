#!/usr/bin/env python
# coding: utf-8

import os
import subprocess
import tempfile
import sublime_plugin


class CommandBase(sublime_plugin.TextCommand):

    def _show_temp_file(self, output, suffix=''):
        window = self.view.window()
        newfile = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        newfile.write(output)
        newfile.close()
        newview = window.open_file(newfile.name)
        newview.set_read_only(True)
        if suffix == '.diff':
            newview.set_syntax_file('Packages/Diff/Diff.tmLanguage')
        # window.run_command("show_panel", {"panel": "console"})


class SubporcessCommandBase(CommandBase):
    cmd = ''

    def run(self, edit):
        filename = self.view.file_name()
        if not filename:
            print("no filename")
            return
        print("filename:", filename)
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        status, output = subprocess.getstatusoutput(self.cmd.format(
            filename=filename,
            dirname=dirname,
            basename=basename,
        ))
        print("status, output", status, output)
        self._show_temp_file(output.encode('utf-8'))
