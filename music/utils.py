"""utils
"""


def slugify(text: str) -> str:
    """slugify

    Create a url-safe string from text

    Gotten from https://www.peterbe.com/plog/fastest-python-function-to-slugify-a-string
    on 13/11/2021
    """

    non_url_safe = ['"', '#', '$', '%', '&', '+',
                        ',', '/', ':', ';', '=', '?',
                        '@', '[', '\\', ']', '^', '`',
                        '{', '|', '}', '~', "'"]

    # lowercase text
    text = text.lower()
    # TODO: watch for non-string types!
    non_safe = [c for c in text if c in non_url_safe]
    if non_safe:
        for c in non_safe:
            text = text.replace(c, '')
    text = u'_'.join(text.split())
    return text