

def words2characters(words):

    characters = []

    for word in words:
        for ch in str(word):
            characters.append(ch)

    return characters
if __name__ == "__main__":
    sample = ['hello', 1.234, True]
    print(words2characters(sample))