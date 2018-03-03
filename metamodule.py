from abc import ABCMeta, abstractmethod

# This is the meta class for generating new modules
# each module must inherit this class
# see modules.template for a template on how to use the methods

class Meta(metaclass=ABCMeta):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def get_command(self):
        pass


    @abstractmethod
    async def execute(self, command, message):
        pass


    @abstractmethod
    async def help(self, message):
        pass

    def get_max_parameters(self):
        return None
