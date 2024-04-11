# pip install bcrypt
import time
import bcrypt

password = "P@ssword1$"

bytes = password.encode('utf-8')
salt = bcrypt.gensalt(14)

hash = bcrypt.hashpw(bytes, salt)

print(hash)


if bcrypt.checkpw(password.encode('utf-8'), hash):
    print("It Matches!")
else:
    print("It Does not Match :(")


print("*" * 50)

for i in range(12,21):
    print(f"\n{i} rounds")
    salt = bcrypt.gensalt(i)
    start = time.time()
    hash = bcrypt.hashpw(bytes, salt)
    end = time.time()
    print(f"{hash[0:10].decode('utf-8')}...")
    print(f"Hashing time: {(end - start):.2f} s")
    start = time.time()
    match = bcrypt.checkpw(bytes, hash)
    end = time.time()
    print(f"Verify time:  {(end - start):.2f} s => {match}")
