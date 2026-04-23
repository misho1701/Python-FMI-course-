class RunewordsCalculator:
    def __init__(self, runewords):
        self.runewords = list(runewords.items())
        self.runes = []
        self.used = set()

    def add_runes(self, runes):
        self.runes.extend(runes)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.used) == len(self.runewords):
            raise StopIteration

        for name, recipe in self.runewords:
            if name in self.used:
                continue

            if self._can_build(recipe):
                self.used.add(name)
                return name

        return None

    def _can_build(self, recipe):
        i = 0
        for rune in self.runes:
            if rune == recipe[i]:
                i += 1
                if i == len(recipe):
                    return True
        return False

