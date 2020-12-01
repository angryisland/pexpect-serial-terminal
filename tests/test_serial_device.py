import sys
import pytest

def test_uname(serial_device):
    output = serial_device.run('uname')
    assert 'Linux' in output

def test_interactive(serial_device):
    serial_device.process.sendline('man whoami')
    serial_device.process.expect('q to quit', 3)
    serial_device.process.write('q')
    serial_device.process.expect(serial_device.prompt, 3)
