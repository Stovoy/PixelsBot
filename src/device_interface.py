import os
import sys
import subprocess

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


def do_click(device):
    device.touch(200, 200, MonkeyDevice.DOWN_AND_UP)

# Define the commands.
commands = {
    'click': do_click
}


def do_command(command, device):
    """Executes a given command on the bot.

    Args:
        command: Command to execute.
        device: MonkeyDevice object.
    """
    if command in commands:
        commands[command](device)
    else:
        raise ValueError()


class Unbuffered(object):

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


if __name__ == '__main__':
    # sys.stdout = Unbuffered(sys.stdout)

    device = MonkeyRunner.waitForConnection()

    while True:
        command = raw_input('ready> ')
        if command == 'stop':
            break
        try:
            do_command(command, device)
        except ValueError:
            print 'Invalid command: %s' % command
            break
