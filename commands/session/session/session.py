import subprocess
import threading

class Locked:
    def __init__(self, l):
        self.lock = l

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self, type, value, traceback):
        self.lock.release()


class Session(object):
    def start(self):
        pass

    def execute(self, lines):
        pass

    def stop(self):
        pass

    def kill(self):
        pass

    def is_running(self):
        return False

class PipeSession(Session):
    def __init__(self):
        self.interpreter = None
        self.lock = threading.Lock()
        self.running = False

    def _command(self):
        """The command to start the interpreter."""
        return ["cat"]

    def _ready(self):
        """Returns a function(string) to match against in the output to verify
        that the interpreter is ready.

        In practice this should send a command to the interpreter to cause a
        line to output and then return a function that will match against that
        line.

        This function should NEVER acquire the lock.
        """
        end = "SESSION_END_OF_COMMAND_REACHED_READY"
        self._sendlines([end])
        return lambda l: l == end

    def _sendlines(self, lines):
        assert self.running
        self.interpreter.stdin.writelines([l+'\n' for l in lines])
        self.interpreter.stdin.flush()

    def _readline(self):
        """Read a line from the output of the program.
        Will block until a line is available.
        """
        assert self.running
        l = ""
        while not l:
            l = self.interpreter.stdout.readline()
        return l.rstrip('\n')

    def _read_until_ready(self):
        r = self._ready()
        lines = []
        while True:
            l = self._readline()
            if r(l):
                return lines
            lines.append(l.rstrip('\n'))

    def start(self):
        with Locked(self.lock):
            assert not self.running
            try:
                self.interpreter = subprocess.Popen(self._command(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True, universal_newlines=True)
            except Exception as e:
                raise ValueError("Error running command %s: %s" % (self.command, str(e)))
            self.running = True
            self._read_until_ready()

    def execute(self, lines):
        with Locked(self.lock):
            assert self.running
            self._sendlines(lines)
            out = self._read_until_ready()
            return out

    def stop(self):
        with Locked(self.lock):
            assert self.running
            self.interpreter.terminate()
            self.interpreter.wait()
            self.interpreter.stdin.close()
            self.interpreter.stdout.close()
            self.running = False

    def kill(self):
        self.interpreter.kill()
        self.interpreter.wait()
        self.interpreter.stdin.close()
        self.interpreter.stdout.close()
        self.running = False

    def is_running(self):
        return self.running

class BashSession(PipeSession):
    def __init__(self):
        PipeSession.__init__(self)

    def _command(self):
        return ["/bin/bash"]

    def _ready(self):
        end = "SESSION_END_OF_COMMAND_REACHED_READY"
        self._sendlines(['echo '+end])
        return lambda l: l == end
