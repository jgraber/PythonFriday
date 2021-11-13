import subprocess

# run a command
subprocess.run('git shortlog')

# alternative way with a list for params
subprocess.run(['git', 'shortlog', '--max-count=5'])

# capture output as text
git_status = subprocess.run('git shortlog', capture_output=True, text=True)
print(f'stdout: {git_status.stdout}')
print(f'stderr: {git_status.stderr}')
print('***')

# run GUI tool
import os
current = os.getcwd()
subprocess.run(f'explorer {current}')