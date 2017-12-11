class NameCounter:
    def __init__(self):
        self.rep = {}

    def get_count(self, name):
        return self.rep.get(name, 0)

    def set_count(self, name, count):
        self.rep[name] = count

    def count(self, name):
        self.rep[name] = self.rep.get(name, 0) + 1
        return self.rep[name] 

    def reset(self):
        self.rep.clear()

    def __str__(self):
        return repr(self.rep)