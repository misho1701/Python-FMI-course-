class Egg:
    def __init__(self):
        self._segments = []
        self._filled = 0.0
        self._broken_top = False
        self._broken_bottom = False
        self._tournament = None

    def paint(self, *args):
        total_new = sum(p for _, p in args)

        if self._filled + total_new > 100.0:
            raise ValueError("Too much paint")

        current = self._filled

        for hex_color, percentage in args:
            pigment = self._pigment(hex_color)

            start = current
            end = current + percentage

            if start < 50 < end:
                self._segments.append((start, 50, pigment))
                self._segments.append((50, end, pigment))
            else:
                self._segments.append((start, end, pigment))

            current = end

        self._filled += total_new

    def _pigment(self, hex_color):
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return r + g + b

    def _strength(self, top):
        if top and self._broken_top:
            raise TypeError("Top side is broken")
        if not top and self._broken_bottom:
            raise TypeError("Bottom side is broken")

        low, high = (0, 50) if top else (50, 100)
        total = 0.0

        for start, end, pigment in self._segments:
            overlap_start = max(start, low)
            overlap_end = min(end, high)

            if overlap_start < overlap_end:
                portion = (overlap_end - overlap_start) / 50
                total += portion * pigment

        return total

    def _battle(self, other, top):
        s1 = self._strength(top)
        s2 = other._strength(top)

        if s1 > s2:
            winner, loser = self, other
        else:
            winner, loser = other, self

        if top:
            loser._broken_top = True
        else:
            loser._broken_bottom = True

        if self._tournament and self._tournament is other._tournament:
            self._tournament.record(self, other, "top" if top else "bottom", winner)

        return winner

    def __mul__(self, other):
        return self._battle(other, True)

    def __matmul__(self, other):
        return self._battle(other, False)


class EggTournament:
    def __init__(self):
        self._eggs = {}
        self._names = {}
        self._history = {}
        self._wins = {}

    def register(self, egg, name):
        if not name.isidentifier():
            raise ValueError("Invalid registration name")

        if name in self._eggs:
            raise ValueError(f"Egg with name {name} has already been registered")

        if egg._tournament is not None:
            raise ValueError("An egg cannot be registered in multiple tournaments")

        self._eggs[name] = egg
        self._names[egg] = name
        self._wins[egg] = 0
        egg._tournament = self

    def _pair_key(self, egg1, egg2):
        return (egg1, egg2) if id(egg1) < id(egg2) else (egg2, egg1)

    def record(self, egg1, egg2, side, winner):
        if egg1 not in self._names or egg2 not in self._names:
            return

        key = self._pair_key(egg1, egg2), side
        self._history[key] = winner
        self._wins[winner] += 1

    def __getitem__(self, item):
        if isinstance(item, tuple):
            egg1, egg2, side = item
        elif isinstance(item, slice):
            egg1, egg2, side = item.start, item.stop, item.step
        else:
            raise KeyError

        key = self._pair_key(egg1, egg2), side

        if key not in self._history:
            raise KeyError

        return self._history[key]

    def __contains__(self, egg):
        return egg in self._names

    def __getattr__(self, name):
        if name not in self._eggs:
            raise AttributeError("Apologies, there is no such egg registered")

        egg = self._eggs[name]
        return {
            "position": self._position(egg),
            "victories": self._wins[egg]
        }

    @property
    def ranking(self):
        sorted_eggs = sorted(self._wins.items(), key=lambda x: -x[1])

        ranking = {}
        current_pos = 1
        last_wins = None

        for i, (egg, wins) in enumerate(sorted_eggs):
            if wins != last_wins:
                current_pos = i + 1

            if current_pos not in ranking:
                ranking[current_pos] = set()

            ranking[current_pos].add(egg)
            last_wins = wins

        return ranking

    def _position(self, egg):
        for pos, eggs in self.ranking.items():
            if egg in eggs:
                return pos

    def __rmatmul__(self, position):
        if position not in self.ranking:
            raise IndexError

        eggs = self.ranking[position]

        if len(eggs) == 1:
            return list(eggs)[0]

        return eggs