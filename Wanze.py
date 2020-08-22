#!/usr/bin/env python
import sys, argparse
import os
import toml
import pyaudio
import subprocess

from recordAudio import Recorder
from sendMail import send_audio_data

# ToDo: add Format
configs = {
    'audio': [
        ('device_index', 'Choose a device, by entering the index-number', int, None),
        ('format', 'The format in which the audio will be recorded. You must give in a number. The number corresponds to the formats listed here https://people.csail.mit.edu/hubert/pyaudio/docs/#class-pyaudio', int, 8),
        ('channels', 'samples per frame', int, 1), 
        ('rate', 'frames per second that should be recorded', int, 44100), 
        ('chunk', 'number of frames in the buffer', int, 4096), 
        ('threshold', 'if the volume exceed the threshold, the recording will start', int, 1000),
        ('silence_limit', 'if there is n seconds of silence, the recording will end', int, 5), 
        ('recordings', 'max number of recordings that should be taken', int, 3)
    ],
    'mail': [
        ('subject', 'title for the email', str, 'Wanze'),
        ('sender', 'the email, from where you send the audios', str, None),
        ('receiver', 'the email that receives the audios', str, None),
        ('password', 'the password of the sender-email', str, None)
    ]
}


def config(args):
    if args.create:
        data = {}

        for (namespace, items) in configs.items():
            data[namespace] = {}
            for (key, info, _type, default) in items:
                print(f'{key}: {info} (default: {default}, {type(_type)}')
                if key == 'device_index':
                    audio = pyaudio.PyAudio()
                    for i in range(audio.get_device_count()):
                        print(str(i) + ': ' + audio.get_device_info_by_index(i).get('name'))
                inp = input()
                while not inp and not default:
                    print('this variable need to be specified. It has no default')
                    inp = input()
                data[namespace][key] = _type(inp or default) if _type is not str else inp or default

        with open('config.toml', 'w+') as f:
            toml.dump(data, f)
    elif args.read:
        if os.path.exists('config.toml'):
            with open('config.toml', 'r') as f:
                print(f.read())
        else:
            print('There is no config.toml file existing in the current directory')
    elif args.open:
        if os.path.exists('config.toml'):
            if sys.platform == 'linux' or sys.platform == 'linux2':
                editor = 'nano'
            elif sys.platform == 'win32' or sys.platform == 'win64':
                editor = 'notepad.exe'
            subprocess.call([editor, 'config.toml'])
        else:
            print('There is no config.toml file existing in the current directory')
    else:
        print('You must specify if you want to read (-r, --read), open (-o, --open) or create (-c, --create) the config')


def start(args):
    if not os.path.exists('config.toml'):
        print('You must first create a config file with "python Wanze.py config -c"')
        exit()
    config = toml.load('config.toml')
    
    for (opt, val) in vars(args).items():
        if opt == 'func':
            continue
        (namespace, key) = opt.split('_', 1)
        if val:
            config[namespace][key] = val

    print('Press CTRL + C to close the programm')
    try:
        for _ in Recorder(config['audio']):
            send_audio_data(config['mail'])

    except (KeyboardInterrupt, SystemExit):
        print('Stop listening')
        exit()


def main():
    description = '''
A programm that records an audio, if a voice gets detected and then send it via email to a receiver.
If you need help to start this programm. Please read the README on GitHub
    '''
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers(help='sub-command help')
    
    parser_config = subparsers.add_parser('config', help='config help')
    group = parser_config.add_mutually_exclusive_group()
    group.add_argument('-c', '--create', action="store_true", help='creates a config file')
    group.add_argument('-r', '--read', action="store_true", help="displays the config file")
    group.add_argument('-o', '--open', action="store_true", help="opnes the config file for editing with nano on linux and notepad on windows")
    parser_config.set_defaults(func=config)

    parser_start = subparsers.add_parser('start', help='start help')
    for (namespace, items) in configs.items():
        for (name, info, _type, _) in items:
            arg_name = f'--{namespace}_{name}'
            parser_start.add_argument(arg_name, help=info, type=_type)
    parser_start.set_defaults(func=start)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()