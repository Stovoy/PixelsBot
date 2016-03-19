import sys

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


def do_snapshot(device, image_format='png'):
    """Takes a snapshot and prints it to stdout as bytes.

    Args:
        device: MonkeyDevice object.
        image_format: Format for the image.
    """
    snapshot = device.takeSnapshot()
    print snapshot.convertToBytes(image_format)

# Define the commands.
commands = {
    'snapshot': do_snapshot
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
        raise ValueError('Unknown command %s' % command)

if __name__ == '__main__':
    print 'Connecting to device...'
    device = MonkeyRunner.waitForConnection()
    print 'Connected.'

    command = raw_input()
    do_command(command, device)
