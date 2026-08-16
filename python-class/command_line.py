import argparse

import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Greet one or more people with configurable style."
    )
    parser.add_argument("name", help="Name of the person to greet")
    parser.add_argument("-g", "--greeting", default="Hello", help="Greeting word")
    parser.add_argument("--count", type=int, default=1, help="Repeat count")
    parser.add_argument("--shout", action="store_true", help="Uppercase output")
    parser.add_argument("--lang", choices=["en", "fr", "sw"], default="en")

    args = parser.parse_args()

    message = f"{args.greeting}, {args.name}!"
    if args.shout:
        message = message.upper()

    for _ in range(args.count):
        print(message)

if __name__ == "__main__":
    main()
