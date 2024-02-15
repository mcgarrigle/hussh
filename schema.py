class Schema:

    def __init__(self, **schema):
        self.schema = schema

    def __eq__(self, other):
        return self.validate(other)

    def __ne__(self, other):
        return not self == other

    def validate(self, subject):
        if len(subject) != len(self.schema):
            return False
        checks  = [ isinstance(subject.get(k), T) for k,T in self.schema.items() ]
        return all(checks)
