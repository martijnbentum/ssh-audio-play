import subprocess
import shlex
from .ssh_audio_config import get_audio_mode, require, get_optional


def play_audio(path: str, start: float | None = None, end: float | None = None,
    wait: bool = False, verbose: bool = False, show_cmd: bool = False) -> None:
    '''
    Play audio locally or via SSH streaming.
    '''
    mode = get_audio_mode()
    cmd = build_play_command(path, start, end, verbose=verbose)
    if show_cmd: print(f'Executing command: {cmd}')
    p = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE,
        stderr=subprocess.PIPE, text = True)
    if not wait:
        return None
    stdout, stderr = p.communicate()
    if verbose and stdout:
        print(f'Play stdout: {stdout}')
    if verbose and stderr:
        print(f'Play stderr: {stderr}')
    if p.returncode != 0:
        message = 'Audio playback failed'
        if stderr and stderr.strip():
            message += f': {stderr.strip()}'
        raise RuntimeError(message)
    if mode == 'remote' and '__PLAY_DONE__' not in stdout:
        raise RuntimeError('Remote audio playback did not report completion.')
    return None
    


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
        cfg = require(['LOCAL_PLAY'])
        audio_local_play = cfg['LOCAL_PLAY']
        cmd = f'{audio_local_play} {path}'
        if not verbose:
            cmd += ' -q'
        if start is not None and duration is not None:
            cmd += f' trim {start} {duration}'
        elif start is not None and duration is None:
            cmd += f' trim {start} :'
        cmd += f' pad 0 0.15'
        return cmd

    if mode != 'remote':
        m = f'Unsupported SSH_AUDIO_PLAY_MODE: {mode}, should be "local" or "remote"'
        raise RuntimeError(m)

    cfg= require(['LOCAL_USER','REMOTE_SOX','LOCAL_PLAY'])

    audio_local_user = cfg['LOCAL_USER']
    audio_remote_sox = cfg['REMOTE_SOX']
    audio_local_play = cfg['LOCAL_PLAY']

    port = get_optional('SSH_PORT', cast=int, default=22)

    cmd = ''
    cmd += f'{audio_remote_sox} {path} -t wav -'
    if start is not None and duration is not None:
        cmd += f' trim {start} {duration}'
    elif start is not None and duration is None:
        cmd += f' trim {start} :'
    cmd += f' pad 0 0.15'
    cmd += f' | '
    cmd += f'ssh -p {port} '
    cmd += f'{audio_local_user}@localhost '
    cmd += f'"{audio_local_play} '
    if not verbose:
        cmd += ' -q'
    cmd += ' - && echo __PLAY_DONE__"'
    return cmd
