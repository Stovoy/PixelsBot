import os
import sys
import subprocess

from com.android.monkeyrunner import MonkeyRunner



def do_snapshot(device, image_format='png'):
    """Takes a snapshot and prints it to stdout as bytes.

    Args:
        device: MonkeyDevice object.
        image_format: Format for the image.
    """
    os.system('adb pull /sys/devices/virtual/graphics/fb0 image')
    subprocess.call('ffmpeg -vframes 1 -vcodec rawvideo -loglevel quiet -f  rawvideo -pix_fmt rgba -s 480x854 -i image -f image2 -vcodec png image.png')

    #snapshot = device.takeSnapshot()
    print '<output start>'
    #print snapshot.convertToBytes()
    print '<output done>'

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
        raise ValueError()

if __name__ == '__main__':
    device = MonkeyRunner.waitForConnection()

    print device.takeSnapshot()
    print device.takeSnapshot()
    print device.takeSnapshot()
    print device.takeSnapshot()
    sys.exit(0)
    while True:
        command = raw_input('ready> ')
        try:
            do_command(command, device)
        except ValueError:
            print 'Invalid command: %s' % command
            break
        except Exception:
            print 'Exception'
            break
