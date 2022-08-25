
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading,yaml

yamlPath = "config.yaml"


class SqlSession:

    def __init__(self,dbInfo):
        self.dbInfo = dbInfo

    def getSqlSession(self):
        engine = create_engine(self.dbInfo)
        DBsession = sessionmaker(bind=engine)
        return DBsession()



class ConfigYaml:

    _instance_local = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'instance'):
            with cls._instance_local:
                if not hasattr(cls,'instance'):
                    cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self,content):
        self.content = content

    @classmethod
    def read(cls,path):
        with open(path,"r") as file:
            data = file.read()
            result = yaml.load(data,Loader=yaml.FullLoader)
            return result


    @classmethod
    def getInstance(cls):
        if not hasattr(cls,'instance'):
            content = cls.read(yamlPath)
            cls.instance = ConfigYaml(content)#防止新建实例时，多线程导致多次新建，故配合__new__方法用锁保证线程安全
        return cls.instance









if __name__ == '__main__':
    result = ConfigYaml.getInstance().content
    print(result)