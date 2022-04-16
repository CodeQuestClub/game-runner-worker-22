from glob import glob


dirs = glob('bots/*/')
if len(dirs) != 4:
    with open('command.sh', 'w') as f:
        f.write("echo 'There should be exactly 4 folders in the directory'")
    exit()

dirs = [dir[:-1] if dir[-1] == '/' else dir for dir in dirs]
with open('command.sh', 'w') as f:
    args = ' '.join(dirs)
    f.write(f'codequest22 --no-visual {args}')