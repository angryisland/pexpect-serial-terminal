import sys
import pytest
import pexpect
from pexpect.popen_spawn import PopenSpawn


PROMPT = r'\w+@.+:.+[#\$]'

def pytest_addoption(parser):
    parser.addoption("--port", action="store", default=None, help="device serial port")

class SerialDevice():
    process = None

    def __init__(self, port, prompt):
        self.port = port
        self.prompt = prompt

    def open(self):
        self.process = PopenSpawn(f'{sys.executable} -m pexpect_serial_terminal -p {self.port}')
        self.process.logfile_read = open("serial_log.txt", "ab+")
        self.process.sendline('')
        i = self.process.expect([r'.+ login:', self.prompt, pexpect.TIMEOUT])
        if i == 0:
            self.process.sendline('ubuntu')
            self.process.expect('Password:')
            self.process.sendline('ubuntu')
            self.process.expect(self.prompt)
        elif i == 2:
            self.close()
            raise ValueError('cannot log in serial device!')

    def close(self):
        self.process.write('\x03')

    def run(self, command, timeout=3):
        self.process.sendline(command)
        self.process.expect(self.prompt, timeout)
        output = self.process.before.decode('utf-8')
        print('\n<serial output>\ncommand:', output)
        return output


@pytest.fixture()
def serial_device(request):
    port = request.config.getoption("--port")
    handle = SerialDevice(port, PROMPT)
    handle.open()
    yield handle
    handle.close()
