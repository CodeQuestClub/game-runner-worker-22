import os
import requests as r
import shutil
import json
import subprocess
import config
from logs import log


def download_match_submissions(match_index, teams):
    match_folder = f'games/match_{match_index}'

    if os.path.isdir(match_folder):
        shutil.rmtree(match_folder)
    os.makedirs(f'{match_folder}/bots')

    with open(f'{match_folder}/info.json', 'w') as f:
        f.write(json.dumps({
            'match_index': match_index,
            'teams': teams
        }))
    
    for team in teams:
        team_directory = f'{match_folder}/bots/{team["name"]}'
        os.makedirs(team_directory, exist_ok=True)
        team_submission = r.get(team['submission'], allow_redirects=True)
        with open(f'{team_directory}/submission.zip', 'wb') as f:
            f.write(team_submission.content)


def unzip_match_submissions(match_index, teams):
    match_folder = f'games/match_{match_index}'
    for team in teams:
        team_directory = f'{match_folder}/bots/{team["name"]}'
        shutil.unpack_archive(f'{team_directory}/submission.zip', f'{team_directory}')
        os.remove(f'{team_directory}/submission.zip')


def run_game(match_folder, map_name, teams):
    teams = [team['name'] for team in teams]
    results = None
    retries_left = config.game_retries + 1
    command = ' '.join(['timeout', str(config.game_timeout_time), 'codequest22', '--no-visual', '-m', map_name] + \
        [f'bots/{team_name}/'.replace(" ", r"\ ") for team_name in teams])
    log(f'Running the game for {str(teams)}')
    while results is None and retries_left > 0:
        retries_left -= 1

        try:
            log(command)
            subprocess.run(command, shell=True, cwd=match_folder)
        except Exception:
            pass
        
        replay_file = f'{match_folder}/replay.txt'
        if os.path.isfile(replay_file):
            result_line = subprocess.check_output(['tail', '-1', replay_file]).strip()
            try:
                raw_results = json.loads(result_line)
                if raw_results['type'] != 'winner':
                    raise Exception('Game failed somewhere')
                results = {teams[i]: raw_results['score'][i] for i in range(len(teams))}
            except:
                log(f'Game between {str(teams)} failed or crashed. Retrying soon...')
    
    return results is not None, results
