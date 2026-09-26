"""Begin with one concrete object before introducing an abstract parent."""


class Add:
    """Keep the inputs and behavior for one addition together."""

    def __init__(self, a, b):
        
        self.a = a
        self.b = b

    def get_result(self):
        
        return self.a + self.b