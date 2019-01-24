# coding: utf-8

import subprocess
import os
import tempfile

import sublime_plugin


class GitLogCommand(sublime_plugin.TextCommand):

    def run(self, edit, see_commit=True):
        filename = self.view.file_name()
        if not filename:
            print("no filename")
            return
        dirname = os.path.dirname(filename)
        print("filename:", filename)
        os.chdir(dirname)
        basename = os.path.basename(filename)
        status, output = subprocess.getstatusoutput('git log -n 20 ' + basename)
        self._show_temp_file(output.encode('utf-8'))

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
