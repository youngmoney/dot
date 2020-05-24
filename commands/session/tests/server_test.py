#!/usr/bin/env python3
import unittest
import subprocess
from multiprocessing import Process
import session.server as server

def shell(command, stdin=None):
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return p.communicate(stdin)[0]

def curl(path, method = 'GET', args = {}):
    base = ['curl', '-sq', 'localhost:7007%s' % path, '-X', method]
    for arg in args:
        base += ['--data-urlencode', '%s=%s' % (arg, args[arg])]
    return shell(base)

class TestBashSession(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.server = Process(target=lambda: server.app.run(port=7007))
        self.server.start()

    @classmethod
    def tearDownClass(self):
        self.server.terminate()
        self.server.join()

    def test_echo(self):
        self.assertEqual(curl('/session/id/echo/start'), '')
        self.assertEqual(curl('/session/id/echo/execute', 'PUT', {'command': 'echo 1'}), '1')
        self.assertEqual(curl('/session/id/echo/execute', 'PUT', {'command': 'THIS="hello world"'}), '')
        self.assertEqual(curl('/session/id/echo/execute', 'PUT', {'command': 'echo $THIS'}), 'hello world')

    def test_stop(self):
        self.assertEqual(curl('/session/id/stop/start'), '')
        self.assertEqual(curl('/session/id/stop/stop'), '')
        self.assertNotEqual(curl('/session/id/stop/execute', 'PUT', {'command': 'echo 1'}), '1')

    def test_kill(self):
        self.assertEqual(curl('/session/id/kill/start'), '')
        self.assertEqual(curl('/session/id/kill/execute', 'PUT', {'command': 'sleep 100 &'}), '')
        self.assertEqual(curl('/session/id/kill/kill', 'GET', {'force': 'true'}), "")
        self.assertNotEqual(curl('/session/id/kill/execute', 'PUT', {'command': 'echo 1'}), '1')
