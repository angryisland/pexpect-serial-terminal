#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, getopt
import serial
from .serial_terminal import SerialTerminal
from ._version import __version__ as version

help_string = 'Usage: %s [option] <parameter>\nThe option and option\'s parameter list below:\n' \
    'Ex:\n' \
    '\t%s -p COM3 -b 115200\n\n' \
    '-c\n' \
    '\tAdd CR before LF when you change a new line.\n' \
    \
    '-p | --port\n' \
    '\t[ default value: None ]\n' \
    '\tSerial port name.\n' \
    \
    '-b | --baud-rate\n' \
    '\t[ default value: 115200 ]\n' \
    '\tBaud rate.\n' \
    \
    '-w | --data-bits\n' \
    '\t[ default value: 8 ]\n' \
    '\t< 8 | 7 >\n' \
    '\tData bits.\n' \
    \
    '-r | --parity\n' \
    '\t[ default value: None ]\n' \
    '\t< None | Even | Odd | Space | Mark >\n' \
    '\tParity.\n' \
    \
    '-s | --stop-bits\n' \
    '\t[ default value: 1 ]\n' \
    '\t< 1 | 2 | 1.5 >\n' \
    '\tStop bits.\n' \
    \
    '-x | --soft-flow-ctl\n' \
    '\t[ default value: off ]\n' \
    '\t< on | off >\n' \
    '\tSoftware flow control switch.\n' \
    \
    '-f | --hard-flow-ctl\n' \
    '\t[ default value: off ]\n' \
    '\t< on | off >\n' \
    '\tHardware flow control switch.\n' \
    \
    '\nversion %s'

def usage():
    print(help_string % (sys.argv[0], sys.argv[0], version))

valid_parity = {
    'NONE'  : serial.PARITY_NONE,
    'EVEN'  : serial.PARITY_EVEN,
    'ODD'   : serial.PARITY_ODD,
    'MARK'  : serial.PARITY_MARK,
    'SPACE' : serial.PARITY_SPACE
}

valid_stop_bits = {
    '1'     : serial.STOPBITS_ONE,
    '1.5'   : serial.STOPBITS_ONE_POINT_FIVE,
    '2'     : serial.STOPBITS_TWO
}

def open_serial_port(config):
    if config['data-bits'] == 7:
        bytesize = serial.SEVENBITS
    else:
        bytesize = serial.EIGHTBITS
    parity = valid_parity[config['parity']]
    stopbits = valid_stop_bits[config['stop-bits']]
    if config['soft-flow-ctl']:
        xonxoff = True
    else:
        xonxoff = False
    if config['hard-flow-ctl']:
        rtscts = True
    else:
        rtscts = False
    return serial.Serial(port=config['port'], baudrate=config['baud-rate'],\
        bytesize=bytesize, parity=parity, stopbits=stopbits,\
        xonxoff=xonxoff, rtscts=rtscts, timeout=0)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    config = {}
    try:
        opts, _ = getopt.getopt(argv, "hcp:b:w:r:s:x:f:", \
            ["port=","baud-rate=","data-bits=","parity=","stop-bits=","soft-flow-ctl=","hard-flow-ctl="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    config['port'] = None
    config['baud-rate'] = 115200
    config['data-bits'] = 8
    config['parity'] = 'NONE'
    config['stop-bits'] = '1'
    config['soft-flow-ctl'] = False
    config['hard-flow-ctl'] = False
    addcr = False

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-c':
            addcr = True
        elif opt in ("-p", "--port"):
            config['port'] = arg
        elif opt in ("-b", "--baud-rate"):
            config['baud-rate'] = int(arg)
        elif opt in ("-w", "--data-bits"):
            if int(arg) == 7:
                bits = 7
            else:
                bits = 8
            config['data-bits'] = bits
        elif opt in ("-r", "--parity"):
            parity = 'NONE'
            for item in valid_parity.keys():
                if item == arg.upper():
                    parity = arg.upper()
            config['parity'] = parity
        elif opt in ("-s", "--stop-bits"):
            stop_bits = '1'
            for item in valid_stop_bits.keys():
                if item == arg:
                    stop_bits = arg
            config['stop-bits'] = stop_bits
        elif opt in ("-x", "--soft-flow-ctl"):
            if arg.lower() == 'on':
                config['soft-flow-ctl'] = True
            else:
                config['soft-flow-ctl'] = False
        elif opt in ("-f", "--hard-flow-ctl"):
            if arg.lower() == 'on':
                config['hard-flow-ctl'] = True
            else:
                config['hard-flow-ctl'] = False

    for key in config:
        print('key:', key)
        print('value: %s' % str(config[key]))
    port = open_serial_port(config)
    if not port.is_open:
        print('serial port cannot open, please check your port settings!')
        sys.exit(1)
    terminal = SerialTerminal(port)
    terminal.start()

    while terminal.is_alive():
        char = sys.stdin.read(1)
        if char == '\x03': # Ctl-C
            break
        if addcr and char == '\n':
            terminal.write('\r')
        terminal.write(char)

    terminal.abort()
    port.close()

if __name__ == "__main__":
    main(sys.argv[1:])
