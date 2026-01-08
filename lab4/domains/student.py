class Student:
    def __init__(self, sid, name, dob):
        self.__sid = sid
        self.__name = name
        self.__dob = dob

    def set_sid(self, sid): 
        self.__sid = sid
    def get_sid(self): 
        return self.__sid

    def set_name(self, name): 
        self.__name = name
    def get_name(self): 
        return self.__name

    def set_dob(self, dob): 
        self.__dob = dob
    def get_dob(self): 
        return self.__dob