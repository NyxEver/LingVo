from abc import ABC
class Recognizer(ABC):
    def __init__(self,config):
        self.config = config
