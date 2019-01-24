# coding: utf-8

from .common import SubporcessCommandBase


class GitkCommand(SubporcessCommandBase):
    cmd = 'cd {dirname} && git log -n 20 {basename}'
