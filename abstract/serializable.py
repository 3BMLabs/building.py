
import json
import importlib

# [!not included in BP singlefile - end]


class Serializable:

    @staticmethod
    def serialize_type(obj) -> dict:
        """Save the type of an object to a dictionary.

        Args:
            obj: the object to get the type of

        Returns:
            dict: a dictionary with keys 'module' and 'type'
        """
        return {
            'module': obj.__module__,
            'type': obj.__class__.__name__
            }
        
    def serialize(self) -> dict:
        """serialize members of this object into a dictionary

        Returns:
            dict: a dictionary of all members. the members will serialize themselves, when necessary.
        """
        return self.__dict__
    
    def toJson(self) -> str:
        """converts a serializable object to json

        Returns:
            str: a json string
        """
        return json.dumps(self, default=lambda x: 
            #when a variable is not compatible with the standard json serialization functions, it's probably one of our classes.
            x.serialize() | self.serialize_type(x)
            )
    
    @staticmethod
    def deserialize_type(data):
        """Creates an new object from the provided data."""
        if isinstance(data, dict):
            if 'type' in data:
                #module_name =  # data.pop('__module__')
                module = importlib.import_module(data.pop('module'))
                type = getattr(module, data.pop('type'))

                if hasattr(type, 'deserialize'):
                    obj = type.deserialize(data)
                else:
                    obj = type.__new__(type)
                    #we assume obj is an instance of Serializable
                    obj.deserialize_members(data)
                #obj.deserialize(data)
                return obj
            #else:
            #    return {key: Serializable.deserialize_type(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [Serializable.deserialize_type(item) for item in data]
        return data
    
    def deserialize_members(self, data : dict):
        """Deserializes the object from the provided data."""
    #    #raise NotImplementedError()
        for key, value in data.items():
            setattr(self, key, self.deserialize_type(value))
    
    def save(self, file_name):
        # we can possibly add an override function we can call on class objects. but for now, this will work fine
        serialized_data = self.toJson()
        with open(file_name, 'w') as file:
            file.write(serialized_data)
            
    def open(self, file_name):
        with open(file_name) as file:
            self.deserialize_members(json.load(file))
            # self.__dict__ = json.load(file)