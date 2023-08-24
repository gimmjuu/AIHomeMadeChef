import json
from db.class_BusinessAverage import BusinessAverage
from db.class_Infrastructure import Infrastructure
from db.class_Realty import Realty
from db.class_RegionTourist import RegionTourist
from db.class_TouristInfo import TouristInfo
from db.class_YearTourist import YearTourist
from db.class_Infra_scaler import InfraScaler


class ObjEncoder(json.JSONEncoder):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()

    def toJSON_as_binary(self, obj):
        if isinstance(obj, list):
            temp_list = list()
            for o in obj:
                str_obj = self.toJSON_an_object(o)
                temp_list.append(str_obj)
            list_json = json.dumps(temp_list, default=lambda o: o.__dict__)
            return list_json
        return self.toJSON_an_object_with_encode(obj)

    def toJSON_an_object_with_encode(self, obj):
        print(obj)
        json_string = self.toJSON_an_object(obj)
        # return json_string.encode('utf-8')
        return json_string

    def toJSON_an_object(self, obj):
        print(obj.__dict__)
        string_converted_obj = json.dumps(obj, default=lambda o: o.__dict__)
        json_string = self.encode(string_converted_obj)
        return json_string


class ObjDecoder(json.JSONDecoder):
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

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

        # json_to_object = json.loads(json_string)  # json -> dict(default)

    def object_mapper(self, dict_obj):
        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)
        if isinstance(dict_obj, str):
            dict_obj = json.loads(dict_obj)
        assert isinstance(dict_obj, dict)
        if "bus_id" in dict_obj.keys():
            return BusinessAverage(**dict_obj)
        elif "inf_tourist" in dict_obj.keys():
            return Infrastructure(**dict_obj)
        elif "inf_id" in dict_obj.keys():
            return InfraScaler(**dict_obj)
        elif "rea_id" in dict_obj.keys():
            return Realty(**dict_obj)
        elif "reg_id" in dict_obj.keys():
            return RegionTourist(**dict_obj)
        elif "tou_id" in dict_obj.keys():
            return TouristInfo(**dict_obj)
        elif "yea_id" in dict_obj.keys():
            return YearTourist(**dict_obj)

    def list_mapper(self, list_obj):
        assert isinstance(list_obj, list)
        result_list = list()
        for o in list_obj:
            converted_o = self.object_mapper(o)
            result_list.append(converted_o)
        return result_list
