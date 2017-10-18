import re

# Hashtags
hash_regex = re.compile(r"#(\w+)")


def process_hash_tags(match):
    return '__HASH_' + match.group(1).upper()


# Handels
handles_regex = re.compile(r"@(\w+)")


def process_handles(match):
    return '__HNDL'# _'+match.group(1).upper()


# URLs
url_regex = re.compile(r"(http|https|ftp)://[a-zA-Z0-9./]+")


def process_text(text):
    # text = re.sub(hash_regex, " ", text)
    # text = re.sub(handles_regex, " ", text)
    # text = re.sub(url_regex, ' __URL ', text)

    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(http|https|ftp)://[a-zA-Z0-9./]+|#(\w+)", " ", text).split())
    return text.lower()
