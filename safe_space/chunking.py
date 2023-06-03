def get_chunks(text, max_length):
    start = 0
    end = 0
    while start + max_length < len(text) and end != -1:
        end = text.rfind(" ", start, start + max_length + 1)
        yield text[start:end]
        start = end + 10
    yield text[start:]


# for text in chunks:
#     print(f"{text}")


