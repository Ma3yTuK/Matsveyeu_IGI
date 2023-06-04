from Ma3yTuKserializer.data_packer.packer import Packer
from .serializer_meta import MetaSerializer

class SerializerShell(MetaSerializer):

    def __init__(self,serializer:MetaSerializer):
        self.packer=Packer()
        self.serializer=serializer


    def dump(self,obj,file):
        self.serializer.dump(self.packer.pack(obj),file)


    def dumps(self,obj):
        return self.serializer.dumps(self.packer.pack(obj))


    def load(self,file):
        return self.packer.unpack(self.serializer.load(file))


    def loads(self,string):
        return self.packer.unpack(self.serializer.loads(string))