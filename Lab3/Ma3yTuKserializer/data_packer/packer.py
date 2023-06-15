import inspect
import types
from .consts import PRIMITIVE_TYPES,IGNORE_CODE,IGNORE_DUNDER,IGNORE_TYPES

class Packer:

    processed_class_obj=None 

    def __is_iter(self,obj):
        return hasattr(obj,'__iter__') and hasattr(obj,'__next__')


    def __is_func(self,obj):
        return isinstance(obj,types.MethodType) or isinstance(obj,types.FunctionType)


    def __extract_class(self,obj):
        cls = getattr(inspect.getmodule(obj),obj.__qualname__.split(".<locals>",1)[0].rsplit(".", 1)[0],None)
        if isinstance (cls,type):
            return cls


    def __make_cell_skeleton(self,value):#stackoverflow
        x = value
        def closure():
            return x
        return closure.__closure__[0]


    def pack(self,obj):
        if isinstance(obj,PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj,bytes):
            return self._pack_bytes(obj)
        elif isinstance(obj,(list,tuple,set,dict)):
            return self._pack_collection(obj)
        elif self.__is_iter(obj):
            return self._pack_iterator(obj)
        elif self.__is_func(obj):
            return self._pack_function(obj)
        elif isinstance(obj,types.CodeType):
            return self._pack_code(obj)
        elif isinstance(obj,types.CellType):
            return self._pack_cell(obj)
        elif isinstance(obj,types.ModuleType):
            return self._pack_module(obj)
        elif inspect.isclass(obj):
            return self._pack_class(obj)
        #elif isinstance(obj,property):
        #    return self._pack_property(obj)
        elif isinstance(obj,object):
            return self._pack_object(obj)
        else:
            raise Exception('unprocessed type')
        

    def _pack_bytes(self,obj):
        return {
            '__type__':'bytes',
            '__packer_storage__':obj.hex()
            }  


    def _pack_collection(self,obj):
        if isinstance(obj,dict):
            return {key:self.pack(value) for key,value in obj.items()} 
        elif isinstance(obj,list):
            return [self.pack(item) for item in obj]
        else:
            return {
                '__type__':type(obj).__name__,
                '__packer_storage__':[self.pack(item) for item in obj]
                }
        

    def _pack_iterator(self,obj):
        return{
            '__type__':'iterator',
            '__packer_storage__':[self.pack(item) for item in obj]
        }


    def _pack_function(self,obj):
        #types.FunctionType(code, globals, name, argdefs, closure) <- for unpacking
        cls = self.__extract_class(obj)

        globs={}
        for key,value in obj.__globals__.items():
            if key in obj.__code__.co_names and key!= obj.__code__.co_name and value is not cls:
                globs[key] = self.pack(value)

        closure=tuple()
        if obj.__closure__ is not None:
            closure = tuple(cell for cell in obj.__closure__ if cell.cell_contents is not cls)

        return{
            '__type__':'function',
            '__packer_storage__':self.pack(
            dict(
                code=obj.__code__,
                globals=globs, 
                name=obj.__name__,
                argdefs=obj.__defaults__,
                closure = closure,
                dictionary = obj.__dict__
                )
            ),
            '__method__':inspect.ismethod(obj)
        }


    def _pack_code(self,obj):
        primary_code = [code for code in dir(obj) if code.startswith('co_')]
        return {
            '__type__':'code',
            '__packer_storage__':{code:self.pack(getattr(obj,code)) for code in primary_code if code not in IGNORE_CODE}
            }


    def _pack_cell(self,obj):
        return {
            '__type__':'cell',
            '__packer_storage__':self.pack(obj.cell_contents)
            }


    def _pack_module(self,obj):
        return {
            '__type__':'module',
            '__packer_storage__':obj.__name__
            }
    

    def _pack_class(self,obj):
        stored = {'__name__':obj.__name__}
        stored['__bases__']=[self.pack(base) for base in obj.__bases__ if base != object]
        
        for key,value in inspect.getmembers(obj):
            if key not in IGNORE_DUNDER and type(value) not in IGNORE_TYPES:
                stored[key]=self.pack(value)

        return{
            '__type__':'class',
            '__packer_storage__':stored
        }

    
    def _pack_property(self,obj):
        print('fuck1')
        stored = dict()
        stored["fget"] = self.pack(obj.fget)
        stored["fset"] = self.pack(obj.fset)
        stored["fdel"] = self.pack(obj.fdel)
        return{
            '__type__':'property',
            '__packer_storage__':stored
        }


    def _pack_object(self,obj):
        stored={
            '__class__':self.pack(obj.__class__),
            'attrs':{}
        }
        
        for attr,value in inspect.getmembers(obj):
            if not attr.startswith('__') and not self.__is_func(value):
                stored['attrs'][attr]=self.pack(value)
        return{
            '__type__':'object',
            '__packer_storage__':stored
        }


    def unpack(self,obj):
        if isinstance(obj,PRIMITIVE_TYPES):
            return obj
        elif isinstance(obj,list):
            return [self.unpack(item) for item in obj]
        elif isinstance(obj, dict):
            if '__type__' in obj.keys():
                match obj['__type__']:
                    case 'bytes':
                        return self._unpack_bytes(obj)
                    case 'iterator':
                        return self._unpack_iterator(obj)
                    case 'function':
                        return self._unpack_function(obj)
                    case 'code':
                        return self._unpack_code(obj)
                    case 'cell':
                        return self._unpack_cell(obj)
                    case 'module':
                        return self._unpack_module(obj)
                    case 'class':
                        return self._unpack_class(obj)
                    case 'property':
                        print("fuck")
                        return self._unpack_property(obj)
                    case 'object':
                        print("fuck")
                        return self._unpack_object(obj)
                    case 'tuple':
                        return tuple(self.unpack(item) for item in obj['__packer_storage__'])
                    case 'set':
                        return set(self.unpack(item) for item in obj['__packer_storage__'])
            else:
                return {key:self.unpack(value) for key,value in obj.items()}
        else:
            return obj
        

    def _unpack_bytes(self,obj):
        return bytes.fromhex(obj['__packer_storage__'])


    def _unpack_iterator(self,obj):
        return iter(self.unpack(item) for item in obj['__packer_storage__'])
    

    def _unpack_function(self,obj):
        unpacked = self.unpack(obj['__packer_storage__'])
        dictionary = unpacked.pop('dictionary')
        skeleton_func = types.FunctionType(**unpacked)

        if obj['__method__'] and self.processed_class_obj!=None:
            skeleton_func = types.MethodType(skeleton_func,self.processed_class_obj)

        skeleton_func.__dict__.update(dictionary)
        skeleton_func.__globals__.update({skeleton_func.__name__:skeleton_func})  
        return skeleton_func

    
    def _unpack_code(self,obj):
        temp = lambda x:x
        return temp.__code__.replace(**(self.unpack(obj['__packer_storage__'])))


    def _unpack_cell(self,obj):
        return self.__make_cell_skeleton(self.unpack(obj['__packer_storage__']))


    def _unpack_module(self,obj):
        return __import__(obj['__packer_storage__'])


    def _unpack_class(self,obj):
        stored = obj['__packer_storage__']
        bases = tuple(self.unpack(base) for base in stored.pop('__bases__'))

        innards = {}
        for key,value in stored.items():
            if not self.__is_func(value):
                innards[key] = self.unpack(value)

        new_class = type(stored['__name__'],bases,innards)

        for key,value in stored.items():
            if isinstance(value,dict) and '__type__' in value.keys() and value['__type__'] == 'function':
                func = self.unpack(value)
                func.__globals__.update({new_class.__name__:new_class})

                if value['__method__']:
                    func = types.MethodType(func,new_class)   

                setattr(new_class,key,func)

        return new_class


    def _unpack_property(self,obj):
        stored = obj['__packer_storage__']
        return property(self.unpack(stored['fget']), self.unpack(stored['fset']), self.unpack(stored['fdel']))


    def _unpack_object(self,obj):
        stored = obj['__packer_storage__']
        related_class = self.unpack(stored['__class__'])
        new_obj = object.__new__(related_class)
        self.processed_class_obj=new_obj
        new_obj.__dict__ = {key : self.unpack(value) for key,value in stored['attrs'].items()}
        self.processed_class_obj=None
        return new_obj