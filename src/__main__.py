import sys


def main() -> None:
    if len(sys.argv) < 3:
        raise ValueError("\033[1;31m[ERROR] Missing functions definition file")
    print("\033[1;32mOK\033[0m")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
