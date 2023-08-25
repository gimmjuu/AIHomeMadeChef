class User:
    def __init__(self, user_id, user_pwd, user_name):
        self.user_id = user_id
        self.user_pwd = user_pwd
        self.user_name = user_name

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, User) and \
                self.user_id == other.user_id and \
                self.user_pwd == other.user_pwd and \
                self.user_name == other.user_name:
            return True
        return False

    def __lt__(self, other):
        return self.user_name < other.user_name