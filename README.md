# Issue

PySerial does not have POSIX fileno attribute on Windows platform. If you want to use pexpect and serial device on Windows platform, you must use something like this:

```python
import os
import pexpect.fdpexpect

device = pexpect.fdpexpect.fdspawn(os.open("COM3", os.O_RDWR))
```

But using this method cannot change the baud rate or data bits or etc. And you have to deal with the serial device's input/output buffered stuff. It's very annoying.

# Main Idea

Create a simple terminal `pexpect-serial-terminal` for serial device. And we can use it with pexpect package. The `pexpect-serial-terminal`  will send input to the device and get output from the device continuously.

![flow-chart](https://i.imgur.com/dCyYL3q.png)

# Installation

Install from PyPI:

    pip install pexpect-serial-terminal

Install directly. Clone this repository, and then:

    pip install .

# Verify Serial Device With Module

Use the help command to find out the parameters.

```
> python -m pexpect_serial_terminal -h

The option and option's parameter list below:
Ex:
        __main__.py -p COM3 -b 115200

-c
        Add CR before LF when you change a new line.
-p | --port
        [ default value: None ]
        Serial port name.
-b | --baud-rate
        [ default value: 115200 ]
        Baud rate.
-w | --data-bits
        [ default value: 8 ]
        < 8 | 7 >
        Data bits.
-r | --parity
        [ default value: None ]
        < None | Even | Odd | Space | Mark >
        Parity.
-s | --stop-bits
        [ default value: 1 ]
        < 1 | 2 | 1.5 >
        Stop bits.
-x | --soft-flow-ctl
        [ default value: off ]
        < on | off >
        Software flow control switch.
-f | --hard-flow-ctl
        [ default value: off ]
        < on | off >
        Hardware flow control switch.
```

Use this terminal to verify the serial device. This terminal is too simple to do the terminal well. It doesn't have input buffer to manipulate the content, so it doesn't support dos key function. I strongly suggest you should only use this terminal for testing or automatic script, don't use it as pure terminal.

    python -m pexpect_serial_terminal -p COM3

Exit the terminal

    Ctl+C

# How To Use It With Pexpect?

You can also see the tests folder for the `pytest example` with this module.

start the child process on Windows:

    import sys
    from pexpect.popen_spawn import PopenSpawn

    process = PopenSpawn('cmd.exe', timeout=3)
    command = f'{sys.executable} -m pexpect_serial_terminal -p COM3'
    process.sendline(command)

start the child process on Linux:

    import sys
    from pexpect.popen_spawn import PopenSpawn

    process = PopenSpawn('/bin/bash', timeout=3)
    command = f'{sys.executable} -m pexpect_serial_terminal -p /dev/ttyUSB0'
    process.sendline(command)

do your own pexpect stuff:

    prompt = r'\w+@.+:.+[#\$]'
    process.sendline('date')
    process.expect(prompt, 3)
    process.before
    process.after

exit the terminal:

    process.write('\x03')
