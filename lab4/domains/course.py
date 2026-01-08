class Course:
    def __init__(self, cid, name, credit):
        self.__cid = cid
        self.__name = name
        self.__credit = credit

    def set_cid(self, cid): 
        self.__cid = cid
    def get_cid(self): 
        return self.__cid

    def set_name(self, name): 
        self.__name = name
    def get_name(self): 
        return self.__name

    def set_credit(self, credit): 
        self.__credit = credit
    def get_credit(self): 
        return self.__credit