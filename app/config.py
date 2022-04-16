import os

server_url = os.environ.get('server_url', 'http://localhost')
if server_url[-1] == '/':
    server_url = server_url[:-1]

worker_id = os.environ.get('worker_id', 1)

wait_time_before_shutdown = 60  # wait this many minutes for server to become responsive
number_of_threads = 1

game_retries = 5
game_timeout_time = 500  # seconds
