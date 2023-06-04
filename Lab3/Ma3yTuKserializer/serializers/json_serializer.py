from Ma3yTuKserializer.data_packer.packer import Packer
from .serializer_meta import MetaSerializer

class Json(MetaSerializer):
    data_packer = Packer()


    def dump(self,obj,file):
        file.write(self.dumps(obj))
    

    def dumps(self,obj):
        packed = self.data_packer.pack(obj)

        if isinstance(packed,(list,tuple)):
            return self.__list_n_tuple_to_string_util(packed)
        
        if isinstance(packed,dict):
            return self.__dict_to_string_util(packed)
        
        return self.__ser_primitive(obj)

    def __ser_primitive(self,obj):
        if isinstance(obj,str):
            obj= f"'{obj}'" 
        return f'"{str(obj)}"'

    def __dict_to_string_util(self,dictionary):
        if not dictionary:
            return '{}'
        
        result='{'

        for key,value in dictionary.items():
            if isinstance(value,dict):
                result+=f'"{key}": {self.__dict_to_string_util(value)},'
            elif isinstance(value,(list,tuple)):
                result+=f'"{key}": {self.__list_n_tuple_to_string_util(value)},'
            else:

                result+=f'"{key}": {self.__ser_primitive(value)},'

        return result[:-1]+'}'


    def __list_n_tuple_to_string_util(self,collection):
        if not collection:
            return '[]'
        
        result='['

        for item in collection:
            if isinstance(item,dict):
                result+=f'{self.__dict_to_string_util(item)},'
            elif isinstance(item,(list,tuple)):
                result+=f'{self.__list_n_tuple_to_string_util(item)},'
            else:
                result+=f'{self.__ser_primitive(item)},'

        return result[:-1]+']'



    def load(self,file):
        data = file.read()
        return self.loads(data)
    
    def loads(self,string):
        result,ind=self.__loads_with_index(string,0)
        return self.data_packer.unpack(result)


    def __loads_with_index(self,string,index):
        match string[index]:
            case '"':
                if string[index+1]=="'":
                    return self.__deser_string(string,index+2)
                else:
                    return self.__deser_primitive(string,index)
            case '[':
                return self.__deser_list(string,index)
            case '{':
                return self.__deser_dict(string,index)


    def __deser_dict(self,string,index):
        #on start string fragment {......}
        end_index=index
        bracket_count=1

        #related element
        while bracket_count>0 and end_index+1<len(string):
            end_index+=1
            if string[end_index]=='{':
                bracket_count+=1
            if string[end_index]=='}':
                bracket_count-=1
        index+=1
        #from here string fragment ......}
        result={}
        while index<end_index:
            if string[index] in (',',' '):
                index+=1
                continue
            key,index = self.__loads_with_index(string,index)
            while string[index] in (':',' '):
                index+=1
            value,index=self.__loads_with_index(string,index)
            result[key]=value

        return result,end_index+1


    def __deser_list(self,string,index):
        #on start string fragment [.....]
        end_index=index+1
        bracket_count=1
        
        #related element
        while bracket_count>0 and end_index<len(string):
            if string[end_index]=='[':
                bracket_count+=1
            if string[end_index]==']':
                bracket_count-=1
            end_index+=1
        index+=1
        #from here string fragment is .....]


        #extracted data
        result=[]
        while index<end_index:
            if string[index] in (',',' '):
                index+=1
                continue
            if end_index-index<2:
                break
            element,index=self.__loads_with_index(string,index)  
            result.append(element)

        return result,end_index+1


    def __deser_string(self,string,index):
        #on start string fragment: '.....'"
        end_index=index

        #related element
        while string[end_index]!="'" and end_index<len(string):
            end_index+=1
        data_slice=string[index:end_index]
        
        return data_slice,end_index+3


    def __string_catcher(self,string,index):
        #on start string fragment: '.....'"
        end_index=index

        #related element
        while string[end_index]!='"' and end_index<len(string):
            end_index+=1
        data_slice=string[index:end_index]
        
        return data_slice,end_index+3



    def __deser_number(self,string,index):
        #on start string fragment: ....."
        end_index = index

        #related element
        while string[end_index]!='"' and end_index<len(string):
            end_index+=1
        data_slice=string[index:end_index]
        
        try:
            if '.' in data_slice:
                return float(data_slice),end_index+1
            else:
                return int(data_slice),end_index+1
        except:
            return self.__string_catcher(string,index)


    def __deser_primitive(self,string,index):
        #on start string fragment: "....."
        #cases: bool,None,number
        index+=1
        if string[index]=='N':
            return None,index+5
        elif string[index]=='T':
            return True,index+5
        elif string[index]=='F':
            return False,index+6
        else:
            return self.__deser_number(string,index)



