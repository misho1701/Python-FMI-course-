#dict comprehension for flex
def курс_в_лева(exchange_rates):
    return {curr: round(1 / exchange_rates[curr], 4) for curr in exchange_rates}

def валута_към_левчета(*args, **kwargs):
    all = {}

    for curr, value in args:
        all[curr] = all.get(curr, 0) + value

    result = []
    for curr in all:
        all_values = all[curr]

        lev = round(all_values if curr == 'BGN' else all_values / kwargs[curr], 4)

        result.append((curr, lev))
    return result

def е_патриотична(amount, exchange_rates):
    leva = 0

    for curr, value in amount:
        if curr == 'BGN':
            leva += round(value, 2)
        else:
            leva += round(value / exchange_rates[curr], 2)

    return 'ПАТРИОТИЧНА!' if leva == int(leva) else 'НЕПАТРИОТИЧНА!' #ternary operator for flex
