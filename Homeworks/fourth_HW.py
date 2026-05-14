import importlib
import re


class BridgeKeeper:
    def __init__(self, module_name):
        self.module_name = module_name

    def __enter__(self):
        module = importlib.import_module(self.module_name)
        allowed = {}

        for name in dir(module):
            obj = getattr(module, name)

            if (
                self._passes_name(obj)
                and self._passes_callable(obj)
                and self._passes_third_question(obj)
            ):
                allowed[name] = obj

        return FilteredModule(allowed)

    def __exit__(self, exc_type, exc, tb):
        return False

    def _passes_name(self, obj):
        if not hasattr(obj, "__name__"):
            return False
        name = obj.__name__
        return isinstance(name, str) and name[:1].isupper()

    def _passes_callable(self, obj):
        if not callable(obj):
            return False

        params = self._parse_docstring(obj)

        try:
            args = [self._dummy_value(t) for t in params]
            obj(*args)
            return True
        except Exception:
            return False

    def _parse_docstring(self, obj):
        doc = obj.__doc__
        if not doc:
            return []

        match = re.search(r"Parameters\s*-+\s*((?:.+\n)+?)(?:\n\s*\n|$)", doc)
        if not match:
            return []

        params_block = match.group(1)
        types = re.findall(r"\w+\s*:\s*([^\n]+)", params_block)

        return [t.strip() for t in types]

    def _dummy_value(self, type_str):
        # union
        if "|" in type_str:
            type_str = type_str.split("|")[0].strip()

        if type_str.startswith("list["):
            inner = type_str[5:-1]
            return [self._dummy_value(inner)]

        if type_str.startswith("tuple["):
            inner = type_str[6:-1]
            return (self._dummy_value(inner),)

        if type_str.startswith("set["):
            inner = type_str[4:-1]
            return {self._dummy_value(inner)}

        if type_str.startswith("dict["):
            inner = type_str[5:-1]
            k, v = map(str.strip, inner.split(","))
            return {self._dummy_value(k): self._dummy_value(v)}

        mapping = {
            "int": 1,
            "float": 1.0,
            "str": "a",
            "bool": True,
        }

        return mapping.get(type_str, None)

    def _passes_third_question(self, obj):
        for attr in dir(obj):
            if attr.startswith("__") and attr.endswith("__"):
                continue

            if self._valid_attribute_name(attr):
                return True

        return False

    def _valid_attribute_name(self, name):
        if re.search(r"[aeiou]{4,}", name):
            return False

        letters = [c for c in name if c.isalpha()]
        if not letters:
            return False

        return letters[-1].isupper()


class FilteredModule:
    def __init__(self, allowed):
        self._allowed = allowed

    def __getattr__(self, name):
        if name in self._allowed:
            return self._allowed[name]
        raise AttributeError(f"{name} is not allowed")

    def __dir__(self):
        return list(self._allowed.keys())