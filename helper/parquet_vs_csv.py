import csv
from faker import Faker
import pyarrow.csv as pv
import pyarrow.parquet as pq

def generate_user_data(num_users, chunk_size=100000):
    fake = Faker()
    fieldnames = ['id', 'name', 'email', 'address', 'phone_number', 'birthdate']
    user_id = 1

    with open('users.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while user_id <= num_users:
            users = []
            for _ in range(min(chunk_size, num_users - user_id + 1)):
                user = {
                    'id': user_id,
                    'name': fake.name(),
                    'email': fake.email(),
                    'address': fake.address().replace('\n', ', '),
                    'phone_number': fake.phone_number(),
                    'birthdate': fake.date_of_birth().isoformat()
                }
                users.append(user)
                user_id += 1

            writer.writerows(users)
            print(f'Generated {user_id - 1} of {num_users} users')

def convert_csv_to_parquet(csv_file, parquet_file):
    table = pv.read_csv(csv_file)
    pq.write_table(table, parquet_file, compression='GZIP')
    print(f'Converted {csv_file} to {parquet_file}')

if __name__ == '__main__':
    num_users = 1000000
    generate_user_data(num_users)
    convert_csv_to_parquet('users.csv', 'users.parquet')
