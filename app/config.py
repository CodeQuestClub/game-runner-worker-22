import os

server_url = os.environ.get('server_url', 'http://localhost')
if server_url[-1] == '/':
    server_url = server_url[:-1]

worker_id = os.environ.get('worker_id', 0)

wait_time_before_shutdown = 60  # wait this many minutes for server to become responsive
number_of_threads = 3

game_retries = 3
game_timeout_time = 400  # seconds

aws_access_key_id = os.environ['client_id']
aws_secret_access_key = os.environ['client_key']
