from abc import abstractmethod
from designMQ.同步的业务逻辑.services import UserService
from designMQ.同步的业务逻辑.utils import SqlSession,ConfigYaml

import sys



class UserController:

    def __init__(self,userService,abservers):
        self.abservers = abservers
        self.userService = userService


    def register(self,name,nation):
        userId = self.userService.register(name,nation)
        for service in self.abservers:
            service.handleRegSucess(userId)



class RegObserver:

    @abstractmethod
    def handleRegSucess(self,userId):
        pass


class RegPromotionObserver(RegObserver):

    def handleRegSucess(self,userId):
        print("RegPromotionObserver",userId)

class RegNotificationObserver(RegObserver):

    def handleRegSucess(self,userId):
        print("RegNotificationObserver",userId)


if __name__ == '__main__':
    abservers = []
    abservers.append(RegNotificationObserver())
    abservers.append(RegPromotionObserver())

    yamlConfig = ConfigYaml.getInstance().content
    dbInfo = yamlConfig["datasource"]["mysql"]["url"]


    sql_session = SqlSession(dbInfo)
    dbSession = sql_session.getSqlSession()
    user_service = UserService(dbSession)
    user_controller = UserController(user_service,abservers)
    user_controller.register("xss","japan")
