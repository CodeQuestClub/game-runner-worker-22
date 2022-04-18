from datetime import datetime
import boto3
import config
from glob import glob


def log(msg, thread=None):
    if thread is not None:
        msg = f'T#{thread} | {msg}'
    print(msg)
    current_time = datetime.now().strftime("%b %d - %H:%M:%S")
    with open('logs.txt', 'a') as f:
        f.write(f'{current_time} | {msg}\n')


def upload_replay_files(match_index):
    s3 = boto3.client(
        's3',
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key
    )

    match_folder = f'games/match_{match_index}'
    files = glob(f'{match_folder}/replay.*')
    for replay_file in files:
        try:
            s3.upload_file(replay_file, 'codequest-replays', f'match_{match_index}/{replay_file.split("/")[-1]}')
            log("Upload replay file successful")
        except Exception:
            log(f"Could not upload replay file for match {match_index}")


def upload_logs():
    s3 = boto3.client(
        's3',
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key
    )

    try:
        s3.upload_file('logs.txt', 'codequest-worker-logs', f'worker_{config.worker_id}/logs.txt')
        log("Upload log file successful")
    except Exception:
        log(f"Could not upload log file for worker {config.worker_id}")
