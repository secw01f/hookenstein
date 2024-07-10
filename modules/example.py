import getpass

class Hook:
    def __init__(self, **kwargs):
        self.self = self
        self.args = kwargs
        secretInput = getpass.getpass("Module Secret Input Example: ")

    def hook(self, input):
        print(self.args)
        print(input)