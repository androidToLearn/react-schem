
class Like:
    def __init__(self, id_user: int, id_vacation: int):
        """constractor"""
        self.id_user = id_user
        self.id_vacation = id_vacation

    def __str__(self):
        """to string"""
        return f"""id user {self.id_user} , id vacation {self.id_vacation}"""
