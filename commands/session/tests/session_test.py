#!/usr/bin/env python3
import unittest
from session.session import BashSession

class TestBashSession(unittest.TestCase):
    def test_echo(self):
        b = BashSession()
        b.start()
        self.assertEqual(b.execute(['echo 1']), ['1'])
        self.assertEqual(b.execute(['THIS="hello world"']), [])
        self.assertEqual(b.execute(['echo $THIS']), ['hello world'])
        b.stop()

    def test_multiple_lines(self):
        b = BashSession()
        b.start()
        self.assertEqual(b.execute(['echo 1', 'echo 2']), ['1', '2'])
        self.assertEqual(b.execute(['(sleep 1; echo 1) &', 'echo 2', 'sleep 1']), ['2','1'])
        b.stop()

    def test_stop(self):
        b = BashSession()
        b.start()
        b.stop()
        self.assertRaises(AssertionError, b.execute, ['echo 1'])

    def test_kill(self):
        b = BashSession()
        b.start()
        b.execute(['sleep 100 &'])
        b.kill()
        self.assertRaises(AssertionError, b.execute, ['echo 1'])
