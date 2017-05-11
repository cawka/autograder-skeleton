"""
UCLA CS118 17S
Project 1 grading script
Version: 0.x
"""

import unittest
from gradescope_utils.autograder_utils.decorators import weight, tags, visibility
from .fixtures import BasicTest, TestWithSavedData

import subprocess
import signal

class MiscChecks(BasicTest):
    @weight(2.5)
    @visibility("visible")
    def test_1(self):
        """1. At least 3 git commits"""
        (stdout, retcode) = self.runApp('git -C "/autograder/submission" log --pretty=format:"%h - %ai: (%an <%ae>) %s"')
        self.assertGreaterEqual(len(stdout.splitlines()), 3, "At least 3 git commits are expected")

    @weight(1.25)
    @visibility("visible")
    def test_2_1(self):
        """2 (part 1). Client handles incorrect non-existing hostname"""

        process = self.startSubmission('client', ['1wronghost', str(self.PORTNO), self.FILE_1K])
        process.wait()
        self.assertNotEqual(process.retcode, 0, "Client should have returned non-zero exit code")
        self.assertEqual(process.stderr.startswith("ERROR:"), True, "stderr should have started with ERROR: (%s)" % process.stderr)

    @weight(1.25)
    @visibility("visible")
    def test_2_2(self):
        """2 (part 2). Client handles incorrect port"""
        process = self.startSubmission('client', [self.HOSTNAME, "-1", self.FILE_1K])
        process.wait()
        self.assertNotEqual(process.retcode, 0, "Client should have returned non-zero exit code")
        self.assertEqual(process.stderr.startswith("ERROR:"), True, "stderr should have started with ERROR: (%s)" % process.stderr)

    @weight(2.5)
    @visibility("visible")
    def test_3(self):
        """3. Server handles incorrect port"""
        process = self.startSubmission('server', ['-1', '/tmp'])
        process.wait()
        self.assertNotEqual(process.retcode, 0, "Client should have returned non-zero exit code")
        self.assertEqual(process.stderr.startswith("ERROR:"), True, "stderr should have started with ERROR: (%s)" % process.stderr)

    @weight(2.5)
    @visibility("visible")
    def test_4(self):
        """4. Server handles SIGTERM / SIGQUIT signals"""
        process = self.startSubmission('server', [str(self.PORTNO), '/tmp'])
        process.killall([signal.SIGINT, signal.SIGTERM, signal.SIGQUIT])
        process.wait()
        self.assertEqual(process.isAlive(), False, "server process should have nicely exited after catching a signal")
