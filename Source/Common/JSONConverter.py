import json
from Source.Data.Data import *


class ObjEncoder(json.JSONEncoder):
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        super().__init__()

    def to_JSON_as_binary(self, obj):
        if isinstance(obj, list):
            temp_list = list()

            for o in obj:
                str_obj = self.obj_to_JSON_with_encode(o)
                temp_list.append(str_obj)

            list_json = json.dumps(temp_list, default=lambda o: o.__dict__)
            return list_json

        return self.obj_to_JSON_with_encode(obj)

    def obj_to_JSON_with_encode(self, obj):
        json_string = json.dumps(obj, default=lambda o: o.__dict__)
        encoded_string = self.encode(json_string)
        return encoded_string


class ObjDecoder(json.JSONDecoder):
    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance__, cls):
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self):
        super().__init__()

    def binary_to_obj(self, binary_str):
        if isinstance(binary_str, bytes):  # binary -> utf-8
            binary_str = binary_str.decode('utf-8')

        json_string = json.loads(binary_str)  # utf-8 -> json

        if isinstance(json_string, list):
            result_obj = self.list_mapper(json_string)

        else:
            result_obj = self.object_mapper(json_string)

        if result_obj is not None:
            return result_obj

        return json_string

    def object_mapper(self, dict_obj):
        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)

        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)

        if "user_id" in dict_obj.keys():
            return User(**dict_obj)
        elif "food_id" in dict_obj.keys():
            return Food(**dict_obj)
        elif "recipe_id" in dict_obj.keys():
            return Recipe(**dict_obj)
        elif "true_or_false" in dict_obj.keys():
            return Result(**dict_obj)
        elif "like_user_id" in dict_obj.keys():
            return Like(**dict_obj)

    def list_mapper(self, list_obj):
        result_list = list()

        for obj in list_obj:
            converted_obj = self.object_mapper(obj)
            result_list.append(converted_obj)

        return result_list


if __name__ == '__main__':
    target_ = [User(user_id='admin', user_pwd='1234')]
    encoder = ObjEncoder()
    str_ = encoder.to_JSON_as_binary(target_)
    decoder = ObjDecoder()
    result_ = decoder.binary_to_obj(str_)
    print(result_[0].user_id)
