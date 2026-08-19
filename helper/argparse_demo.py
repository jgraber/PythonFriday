import argparse

parser = argparse.ArgumentParser(description="A friendly greeting tool")
parser.add_argument("name", help="the person we want to greet")

parser.add_argument("--times", type=int, default=1,
                    help="how often we repeat the greeting")

parser.add_argument("--shout", action="store_true",
                    help="print the greeting in upper case")

args = parser.parse_args()
for _ in range(args.times):
    greeting = f"Hello {args.name}!"
    if args.shout:
        greeting = greeting.upper()
    print(greeting)