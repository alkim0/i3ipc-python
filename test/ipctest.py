from subprocess import Popen
import pytest
import i3ipc
import math
from random import random


class IpcTest:
    timeout_thread = None
    i3_conn = None

    @pytest.fixture(scope='class')
    def i3(self):
        process = Popen(['i3', '-c', 'test/i3.config'])
        # wait for i3 to start up
        tries = 0

        while True:
            try:
                IpcTest.i3_conn = i3ipc.Connection()
                break
            except Exception:
                tries += 1

                if tries > 100:
                    raise Exception('could not start i3')
        yield IpcTest.i3_conn
        process.kill()
        IpcTest.i3_conn = None

    def open_window(self):
        i3 = IpcTest.i3_conn
        assert i3

        result = i3.command('open')
        return result[0].id

    def fresh_workspace(self):
        i3 = IpcTest.i3_conn
        assert i3

        workspaces = i3.get_workspaces()
        while True:
            new_name = str(math.floor(random() * 100000))
            if not any(w for w in workspaces if w['name'] == new_name):
                i3.command('workspace %s' % new_name)
                return new_name
