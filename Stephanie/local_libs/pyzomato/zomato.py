from Stephanie.local_libs.pyzomato.base import Base


class Zomato(Base):
    def __init__(self, API_KEY):
        super().__init__(API_KEY)
