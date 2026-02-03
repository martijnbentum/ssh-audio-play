import subprocess
import shlex
from .ssh_audio_config import get_audio_mode, require, get_optional


def play_audio(path: str, start: float | None = None, end: float | None = None,
    wait: bool = False, verbose: bool = False, show_cmd: bool = False):
    '''
    Play audio locally or via SSH streaming.
    '''
    cmd = build_play_command(path, start, end, verbose=verbose)
    if show_cmd: print(f'Executing command: {cmd}')
    p = subprocess.Popen(cmd, shell=True, stdout - subprocess.PIPE,
        stderr=subprocess.PIPE, text = True)
    if not wait: return
    stdout, stderr = p.communicate()
    if verbose and stdout:
        print(f'Play stdout: {stdout}')
    if stderr:
        print(f'Play stderr: {stderr}')
    


def build_play_command(path: str, start = None, end = None, duration = None, 
    verbose: bool = False) -> str:
    '''
    Load configuration from env and construct the playback command.
    '''
    mode = get_audio_mode()
    path = shlex.quote(path)
    if start is not None and end is not None:
        duration = round(end - start, 3)
    elif start is not None and duration is not None:
        end = start + duration

    if mode == 'local':  
        cfg = require(['AUDIO_LOCAL_PLAY'])
        audio_local_play = cfg['AUDIO_LOCAL_PLAY']
        cmd = f'{audio_local_play} {path}'
        if not verbose:
            cmd += ' -q'
        if start is not None and duration is not None:
            cmd += f' trim {start} {duration}'
        elif start and not duration:
            cmd += f' trim {start} :'
        cmd += f' pad 0 0.15'
        return cmd

    if mode != 'remote':
        m = f'Unsupported AUDIO_MODE: {mode}, should be "local" or "remote"'
        raise RuntimeError(m)

    cfg= require(['AUDIO_LOCAL_USER','AUDIO_REMOTE_SOX','AUDIO_LOCAL_PLAY'])

    audio_local_user = cfg['AUDIO_LOCAL_USER']
    audio_remote_sox = cfg['AUDIO_REMOTE_SOX']
    audio_local_play = cfg['AUDIO_LOCAL_PLAY']

    port = get_optional('AUDIO_SSH_PORT', cast=int, default=22)

    cmd = ''
    cmd += f'{audio_remote_sox} {path} -t wav -'
    if start is not None and duration not None:
        cmd += f' trim {start} {duration}'
    elif start and not duration:
        cmd += f' trim {start} :'
    cmd += f' pad 0 0.15'
    cmd += f' | '
    cmd += f'ssh -p {port} '
    cmd += f'{audio_local_user}@localhost '
    cmd += f'"{audio_local_play} '
    if not verbose:
        cmd += ' -q'
    cmd += ' -; echo __PLAY_DONE__"'
    return cmd
