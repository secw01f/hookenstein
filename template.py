# Import any python modules for your hook module
# You must install the dependencies ahead of time before running your module

class Hook: # The Hook class is required
    def __init__(self, **kwargs):
        self.self = self
        self.args = kwargs # Any arguments you want to pass during initialization can be provided here

        # Any initialization you need for the actions in your hook method to work goes here

    def hook(self, input): # The hook method is required
        print('hooktemplate') # Replace this with your integration code