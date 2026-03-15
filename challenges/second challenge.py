memory = []
seen_phrases = set()

def name_format(name):
    result = ''
    upper_next = True

    for letter in name:
        if letter == '_':
            result += ' '
            upper_next = True
        else:
            if upper_next:
                result += letter.upper()
                upper_next = False
            else:
                result += letter

    return result

def memnick(*funcs):
    if not funcs:
        def decorator(func):
            def wrapper(*args, **kwargs):
                phrase = func(*args, **kwargs)

                if phrase not in seen_phrases:
                    seen_phrases.add(phrase)

                    i = 0
                    while i < len(phrase) and phrase[i] != ',':
                        i += 1

                    addressed = phrase[:i]
                    memory.append((func.__name__, addressed, phrase))

                return phrase

            wrapper.__name__ = func.__name__
            return wrapper
        return decorator

    final_result = []

    for func in funcs:
        aim = name_format(func.__name__)

        for speaker, address, phrase in memory:
            if name_format(address) == aim:
                final_result.append(
                    'С гласа на {}: {}'.format(name_format(speaker), phrase)
                )

    return final_result