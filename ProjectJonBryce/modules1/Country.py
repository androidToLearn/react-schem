
class Country:
    def __init__(self, id: int, name_country: str):
        """constractor"""
        self.id = id
        self.name_country = name_country

    def todict(self):
        """cast object to dict"""
        return {'id': self.id, 'name_country': self.name_country}
