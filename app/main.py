import os
import shutil
import json
from time import sleep
import requests as r
import threading
import config
from logs import log, upload_replay_files, upload_logs
from game import download_match_submissions, unzip_match_submissions, run_game


def be_patient_and(func):
    sleep_time = 10
    total_time_slept = 0
    func_res = func()
    while not func_res:
        sleep(sleep_time)
        total_time_slept += sleep_time
        sleep_time *= 1.5
        if total_time_slept >= config.wait_time_before_shutdown:
            # Server is constantly failing us, time to die now.
            return False, tuple()
        func_res = func()
    return func_res


def get_new_match():
    request_url = f'{config.server_url}/get-match'
    response = r.post(request_url, json={'worker_id': config.worker_id})
    if response.status_code != 200:
        log('Server returned non-200 status code. Don\'t know what to do...')
        return False
    data = response.json()
    if not data['ok']:
        log(f'Server error: {data["message"]}')
        if 'shutdown' in data and data['shutdown']:
            return False, tuple()
        return False
    
    match_index = data['match_index']
    map_name = data['map_name']
    teams = data['teams']

    return True, (match_index, map_name, teams)


def return_match_results(match_index, results):
    log(f'Sending results of match #{match_index} back')
    sent = False
    retries = 5
    while not sent and retries > 0:
        retries -= 1
        response = r.post(f'{config.server_url}/match-results', json={
            'match_index': match_index,
            'results': results
        })
        if response.status_code != 200 or not response.json()['ok']:
            log(f'Results of match #{match_index} failed, retrying...')
        else:
            sent = True
    if sent:
        log(f'Results of match #{match_index} sent back')
    else:
        log(f'Results of match #{match_index} failed. No more retries.')


def thread_entrypoint(thread_id):
    should_continue, data = be_patient_and(get_new_match)
    while should_continue:
        match_index, map_name, teams = data
        download_match_submissions(match_index, teams)
        unzip_match_submissions(match_index, teams)
        successful_run, results = run_game(f'games/match_{match_index}', map_name, teams)
        if not successful_run:
            results = {team['name']: 0 for team in teams}
        upload_replay_files(match_index)
        return_match_results(match_index, results)
        should_continue, data = be_patient_and(get_new_match)


if config.number_of_threads > 1:
    threads = []
    for i in range(config.number_of_threads):
        threads.append(threading.Thread(target=thread_entrypoint, args=(i,)))
        threads[-1].start()

    for thread in threads:
        thread.join()
else:
    thread_entrypoint(0)

upload_logs()
exit()
