def string_reverse(string: str) -> str:
    if string == "":
        return ""
    letter = string[0]
    string = string[1:]
    return string_reverse(string) + letter


def num_mul(number: int) -> int:
    if number < 10:
        return number

    num = number % 10
    number //= 10
    return num_mul(number) * num


def largest_word(string: str) -> str:
    words = string.split()
    return max(words, key=len)


if __name__ == '__main__':
    assert string_reverse("Hello") == "olleH"
    assert num_mul(123) == 6
    assert largest_word("Съешь же ещ этих мягких французских булок, да выпей чаю.") == "французских"
