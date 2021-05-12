import os
import time
import signal
import subprocess


def get_indexes():
    out = set()
    sinks = list(map(lambda x: x.strip(), subprocess.check_output(['pacmd', 'list-sink-inputs']).split(b'\n')))

    for s in sinks:
        if not s:
            continue

        s = s.split()
        if s[0] == b'index:':
            index = s[-1]
        elif s[0] == b'application.name' and s[-1] == b'"spotify"':
            try:
                out.add(index)
            except NameError:
                pass

    return out


indexes = get_indexes()

# The set of panel items that are considered ads
ads = set(map(lambda s: bytes(s.strip(), 'UTF-8'), open(os.path.dirname(__file__) + '/ads_list.txt', 'r')))


def mute(value):
    with open(os.devnull, 'wb') as devnull:
        for i in indexes:
            subprocess.call(['pacmd', 'set-sink-input-mute', i, str(value)], stdout=devnull)


def __on_exit(sig, func):
    # Unmute when exiting
    mute(False)
    exit()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, __on_exit)
    signal.signal(signal.SIGINT, __on_exit)

    mute(False)

    while True:
        # Get names of all the panel items
        apps = subprocess.check_output('wmctrl -l|awk \'{$3=""; $2=""; $1=""; print $0}\'', shell=True).split(b'\n')
        apps = set(map(lambda x: x.strip(), apps))  # Remove leading and trailing spaces from strings

        if apps.intersection(ads):
            mute(True)
        else:
            mute(False)

        time.sleep(1)
