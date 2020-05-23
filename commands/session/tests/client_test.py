#!/usr/bin/env python3
import unittest
from multiprocessing import Process
from session.client import RemoteSession
import session.server as server

def remote_session(name):
    return RemoteSession(name, 'localhost', 7007)

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
        b = remote_session('echo')
        b.start()
        self.assertEqual(b.execute(['echo 1']), ['1'])
        self.assertEqual(b.execute(['THIS="hello world"']), [])
        self.assertEqual(b.execute(['echo $THIS']), ['hello world'])
        b.stop()

    def test_multiple_lines(self):
        b = remote_session('multiple')
        b.start()
        self.assertEqual(b.execute(['echo 1', 'echo 2']), ['1', '2'])
        self.assertEqual(b.execute(['(sleep 1; echo 1) &', 'echo 2', 'sleep 2']), ['2','1'])
        b.stop()

    def test_stop(self):
        b = remote_session('stop')
        b.start()
        b.stop()

    def test_kill(self):
        b = remote_session('kill')
        b.start()
        b.execute(['sleep 100 &'])
        b.kill()
