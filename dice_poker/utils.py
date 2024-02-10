from random import randint


def random_code():
    return f"{randint(0, 2**32-1):08x}"


if __name__ == "__main__":
    print(f"{random_code() = }")
