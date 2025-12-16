# ssh-audio-play

Small utility to play audio either locally or streamed from a remote
machine over SSH.

you should ssh into the remote machine with reverse SSH tunneling enabled ssh -R

ssh -R 127.0.0.1:222:localhost:22 user@remote_machine

Then you can use ssh-audio-play to stream audio from the remote machine to your local machine.

in your python interpreter on the remote machine you can do:

```python
from ssh_audio_play import play_audio
play_audio("/path/to/remote/audio/file.wav")
```

### Installation

#### pip
pip install git+ssh://git@github.com/martijnbentum/ssh-audio-play.git#egg=ssh-audio-play

#### uv pip
uv pip install git+ssh://git@github.com/martijnbentum/ssh-audio-play.git



### create an environment file for setting remote and local audio players
save the following as `.env` in your working directory on the remote machine:

```env
#### Mode: "remote" or "local"
AUDIO_MODE=remote

# --- Remote mode ---
AUDIO_LOCAL_USER=#your_local_username
AUDIO_SSH_PORT=22 # Port on which to connect to remote machine in the example above this would be 222
AUDIO_REMOTE_SOX=/usr/bin/sox # path to sox on the remote machine
AUDIO_LOCAL_PLAY=/usr/bin/play # path to play on the local machine (play is part of sox)

# --- Local mode ---
# Only AUDIO_MODE (set to local) and AUDIO_LOCAL_PLAY is required
```

