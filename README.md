# ssh-audio-play

Small utility to play audio either locally or streamed from a remote
machine over SSH.

you should ssh into the remote machine with reverse SSH tunneling enabled ssh -R

ssh -R 127.0.0.1:222:localhost:22 user@remote_machine

Then you can use ssh-audio-play to stream audio from the remote machine to your local machine.

in your python interpreter of the remote machine you can do:

```python
from ssh_audio_play import play_audio
play_audio("/path/to/remote/audio/file.wav")
```

## Installation

### pip
pip install git+ssh://git@github.com/martijnbentum/ssh-audio-play.git#egg=ssh-audio-play

### uv pip
uv pip install git+ssh://git@github.com/martijnbentum/ssh-audio-play.git



# create an environment file for setting remote and local audio players

#### Mode: "remote" or "local"
AUDIO\_MODE=remote

# --- Remote mode ---
AUDIO\_LOCAL\_USER=
AUDIO\_SSH\_PORT=22 # Port on which to connect to remote machine in the example above this would be 222
AUDIO\_REMOTE\_SOX=/usr/bin/sox
AUDIO\_LOCAL\_PLAY=/usr/bin/play

# --- Local mode ---
# Only AUDIO\_MODE (set to local) and AUDIO\_LOCAL\_PLAY is required

