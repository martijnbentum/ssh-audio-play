import subprocess
import shlex
from .ssh_audio_config import get_audio_mode, require, get_optional


def play_audio(path: str, verbose: bool = False, show_cmd: bool = False):
    '''
    Play audio locally or via SSH streaming.
    '''
    cmd = build_play_command(path, verbose=verbose)
    if show_cmd: print(f'Executing command: {cmd}')
    subprocess.Popen(cmd, shell=True)


def build_play_command(path: str, verbose: bool = False) -> str:
    '''
    Load configuration from env and construct the playback command.
    '''
    mode = get_audio_mode()
    path = shlex.quote(path)

    if mode == 'local':  
        cfg = require(['AUDIO_LOCAL_PLAY'])
        audio_local_play = cfg['AUDIO_LOCAL_PLAY']
        cmd = f'{audio_local_play} {path}'
    if not verbose:
        cmd += ' -q'
    return cmd

    if mode != 'remote':
        m = f'Unsupported AUDIO_MODE: {mode}, should be "local" or "remote"'
        raise RuntimeError(m)

    cfg= require(['AUDIO_LOCAL_USER','AUDIO_REMOTE_SOX','AUDIO_LOCAL_PLAY'])

    audio_local_user = cfg['AUDIO_LOCAL_USER']
    audio_remote_sox = cfg['AUDIO_REMOTE_SOX']
    audio_local_play = cfg['AUDIO_LOCAL_PLAY']

    port = get_optional('AUDIO_SSH_PORT', cast=int, default=22)

    cmd = (
        f'{audio_remote_sox} {path} -t wav - | '
        f'ssh -p {port} '
        f'{audio_local_user}@localhost '
        f'"{audio_local_play} -"'
    )
    if not verbose:
        cmd += ' -q'
    return cmd
