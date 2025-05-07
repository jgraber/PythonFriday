import tempfile
import os

with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
    print(f"temp file created at: {tmp.name}")
    tmp.write("Hello, world!")
    tmp.seek(0)
    print(tmp.read())

print("*" * 50)

tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False)
tmp.write("Attention!")

print(f"File created at: {tmp.name}")
print("\t\t--> delete file by hand")

print("*" * 50)

with tempfile.TemporaryDirectory() as tmpdirname:
    print(f"Temporary directory created at {tmpdirname}")
    filepath = os.path.join(tmpdirname, "example.txt")
    with open(filepath, 'w') as f:
        f.write("Some temporary content.")
    with open(filepath, 'r') as f:
        print(f.readlines())
