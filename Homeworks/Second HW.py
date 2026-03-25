class Currency:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate

    def __eq__(self, other):
        return isinstance(other, Currency) and self.name == other.name and self.rate == other.rate


class PoliticalParty:
    def __init__(self, name, motto, members=None, preferred_currency=None):
        self.name = name
        self._motto = motto
        self.members = members if members else []
        self.preferred_currency = preferred_currency

    @property
    def motto(self):
        return self._motto

    def convert_currency_to_voters(self, amount, currency):
        voters = int(amount / currency.rate)
        if self.preferred_currency == currency:
            voters *= 2
        return voters

    def __str__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, PoliticalParty):
            return Coalition(self, other)
        return NotImplemented


class Coalition:
    def __init__(self, *parties):
        self.parties = list(parties)

    @property
    def members(self):
        return {party.name: party.members for party in self.parties}

    def __add__(self, other):
        if isinstance(other, PoliticalParty):
            return Coalition(*self.parties, other)
        if isinstance(other, Coalition):
            return Coalition(*self.parties, *other.parties)
        return NotImplemented

    def __str__(self):
        return "-".join([party.name for party in self.parties])


class Elections:
    _history = {}

    def __init__(self, year):
        self.year = year
        self.result = {}
        Elections._history[year] = self

    def register_party_or_coalition(self, obj):
        name = str(obj)
        if name not in self.result:
            self.result[name] = 0

    def vote(self, obj):
        name = str(obj)
        self.result[name] += 1

    def rig_elections(self, obj, amount, currency):
        name = str(obj)
        voters = 0

        if isinstance(obj, PoliticalParty):
            voters = obj.convert_currency_to_voters(amount, currency)
        elif isinstance(obj, Coalition):
            voters = max(
                party.convert_currency_to_voters(amount, currency)
                for party in obj.parties
            )

        self.result[name] += voters

    def get_results(self):
        return self.result

    @classmethod
    def get_results_by_year(cls, year):
        if year in cls._history:
            return cls._history[year].get_results()
        return None
