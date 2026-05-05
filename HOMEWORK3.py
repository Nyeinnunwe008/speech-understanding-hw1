"""
Homework 3

This file defines the function 'words2characters'.

To see documentation, use:
help(homework3.words2characters)
"""

def words2characters(words):
    """
    This function converts a list of words into a list of characters.

    @param:
    words - a list of words

    @return:
    characters - a list of characters

    Every element of "words" is converted to a string, then split into
    characters, each of which is appended to the result list.

    Example:
    words = ['hello', 1.234, True]
    returns:
    ['h', 'e', 'l', 'l', 'o', '1', '.', '2', '3', '4', 'T', 'r', 'u', 'e']
    """

    characters = []

    for word in words:
        for ch in str(word):
            characters.append(ch)

    return characters


# Optional test (remove if your teacher doesn't want extra output)
if __name__ == "__main__":
    sample = ['hello', 1.234, True]
    print(words2characters(sample))