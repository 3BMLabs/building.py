
# [!not included in BP singlefile - end]

class Serializable:
    @staticmethod
    def serialize_members(obj) -> dict:
        #return obj.__dict__
        for field_name in obj.__dict__:
            print(getattr(obj, field_name))
    
    def serialize(self) -> dict:
        #for field_name in Serializable.__dict__:
        #    print(getattr(Serializable, field_name))
        #    type(field_name)
        #Serializable.serialize_members(self)
        return {
            'type': self.type
            }