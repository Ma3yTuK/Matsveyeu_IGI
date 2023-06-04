from abc import ABCMeta,abstractmethod

class MetaSerializer(metaclass=ABCMeta):
    @abstractmethod
    def dump(self,obj,file):
        pass
    @abstractmethod
    def dumps(self,obj):
        pass
    @abstractmethod
    def load(self,file):
        pass
    @abstractmethod
    def loads(self,string):
        pass