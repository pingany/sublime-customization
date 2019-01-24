# coding: utf-8

from .common import SubporcessCommandBase


class GitkCommand(SubporcessCommandBase):
    cmd = 'cd {dirname} && gitk {basename}'
