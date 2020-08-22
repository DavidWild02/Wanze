# Wanze
A programm that records an audio, if a voice gets detected and then send it via email to a receiver

##Setup

install necessary modules:

```
pip3 install toml
pip3 install pyaudio
```

crate a config file, that saves your desired settings
```
python Wanze.py config --create
```

if you want to modify the config later, use:
```
nano config.toml
```
or
```
python Wanze.py config --open
```

to start the programm use:
```
 python Wanze.py start
```

##Further Help

If you desire a list about the available command-line options use:
```
python Wanze.py --help
python Wanze.py config --help
python Wanze.py start --help
```

##Turning the programm into an executable
If you wish to start the programm without ````python``` preeceded, you must turn it into an executable.
[StackOverflow](https://stackoverflow.com/questions/304883/what-do-i-use-on-linux-to-make-a-python-program-executable):
```
chmod +x Wanze.py
```
then you can execute it with:
```
./Wanze.py
```
