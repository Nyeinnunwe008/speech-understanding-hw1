
def arithmetic(x, y):

    if isinstance(y, str):
        if isinstance(x, str):
            return x + y
        elif isinstance(x, float):
            return str(x) + y

    elif isinstance(y, float):
        if isinstance(x, str):
            return x * int(y)
        elif isinstance(x, float):
            return x * y

    return None


if __name__ == "__main__":
    print(arithmetic("hi", "there"))
    print(arithmetic(2.5, "abc"))
    print(arithmetic("hi", 3.0))
    print(arithmetic(2.0, 3.0))        # 6.0