import os

def read_env_var():
    value = os.getenv('PYTHON_FRIDAY_COUNTER', '0')
    print(value)
    return int(value)

def write_env_var(value):
    os.environ['PYTHON_FRIDAY_COUNTER'] = str(value)

counter = read_env_var()

counter = counter + 100

write_env_var(counter)

counter_new = read_env_var()