
class User:
    ID_ADMIN = 0
    ID_USER = 1

    def __init__(self, id: int, name: str, second_name: str, password: str, email: str, id_role: int):
        """constractor"""
        self.id = id
        self.name = name
        self.second_name = second_name
        self.password = password
        self.email = email
        self.id_role = id_role

    def __str__(self):
        return f"""id: {self.id} , name: {self.name} ,second_name: {self.second_name} ,password: {self.password} ,email: {self.email} ,id_role: {self.id_role}"""
