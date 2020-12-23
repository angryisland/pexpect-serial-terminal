#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import serial
import threading
import time
import signal
import builtins


def print(*args):
    builtins.print(*args, sep=' ', end='', file=None, flush=True)

exit_terminal = False

def exit_sig_handler(sig, frame):
    print('Got signal to exit')
    global exit_terminal
    exit_terminal = True

def serial_handler(option):
    while not exit_terminal:
        operation = False
        line = option['port'].readline().decode('utf-8')
        if len(line) > 0:
            # pexpect will change the LF to CRLF.
            # If the original string is CRLF, it will become CRCRLF in pexpect.
            if os.name == 'nt':
                if len(line) > 2 and line[-1] == '\n' and line[-2] == '\r':
                    line = line[:-2] + '\n'
            print(line)
            operation = True
        if operation == False:
            time.sleep(0.1)

class SerialTerminal():
    """This module provides a simple terminal which can communicate with serial device.
    """
    option = {
        'port'              : None
    }

    def __init__(self, port):
        """[ parameters ]
        port : pyserial's instance
        """
        if not port.is_open:
            raise ValueError('serial port doesn\'t open')
        self.option['port'] = port
        global exit_terminal
        exit_terminal = False
        signal.signal(signal.SIGINT, exit_sig_handler)

    def start(self):
        self.serial_thread = threading.Thread(target = serial_handler, args = (self.option,))
        self.serial_thread.start()

    def write(self, data):
        self.option['port'].write(data.encode('utf-8'))

    def abort(self):
        global exit_terminal
        exit_terminal = True
        self.serial_thread.join()

    def is_alive(self):
        return not exit_terminal

if __name__ == '__main__':
    port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)
    terminal = SerialTerminal(port)
    terminal.start()

    while terminal.is_alive():
        char = sys.stdin.read(1)
        if char == '\x03': # Ctl-C
            break
        if char == '\n':
            terminal.write('\r')
        else:
            terminal.write(char)

    terminal.abort()
    port.close()
