
from .dao import User
import uuid

class  UserService:

    def __init__(self,session):
        self.session = session


    def register(self,name,nation):
        uid = str(uuid.uuid4())
        newUser = User(name=name,nation=nation,uid = uid)
        self.session.add(newUser)
        self.session.commit()
        self.session.close()
        return uid