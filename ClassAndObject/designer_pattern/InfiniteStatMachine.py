

from enum import Enum

class State(Enum):#纵轴
    SMALL = 0
    SUPER = 1
    FIRE = 2
    CAPE = 3

class Event(Enum):# 横轴
    GOT_MUSHROOM = 0
    GOT_CAPE = 1
    GOT_FIRE_FLOWER = 2
    GOT_MEET_MONSTER =3

class MarioStateMachine2Dmode:


    transitionTable = [#新状态表
        [State.SUPER,State.CAPE,State.FIRE,State.SMALL],
        [State.SUPER,State.CAPE,State.FIRE,State.SMALL],
        [State.CAPE,State.CAPE,State.CAPE,State.SMALL],
        [State.FIRE,State.FIRE,State.FIRE,State.SMALL]
    ]

    actionTable =[#动作表  保存简单的加减法元素，若复杂的一系列操作呢？咋存储
        [100,200,500,0],
        [0,200,500,-100],
        [0,0,0,-200],
        [0,0,0,-300]
    ]

    def __init__(self):#初始状态
        self.currentState = State.SMALL
        self.score = 0

    def obtainMushRoom(self):
        self.executeEvent(Event.GOT_MUSHROOM)

    def obtainCape(self):
        self.executeEvent(Event.GOT_CAPE)

    def obtainFireFlower(self):
        self.executeEvent(Event.GOT_FIRE_FLOWER)

    def meetMonster(self):
        self.executeEvent(Event.GOT_MEET_MONSTER)

    def executeEvent(self,event):#每个事件 必须基于 当前状态 + 当前发生的事件 2个因素 才能定位 下一个状态 和 动作
        stateValue = self.currentState.value#当前状态
        eventValue = event.value#发生的事件   从而确定了 x,y坐标再从 二维数组中提取经转化的状态与动作
        newState = MarioStateMachine2Dmode.transitionTable[stateValue][eventValue]
        tempScore = MarioStateMachine2Dmode.actionTable[stateValue][eventValue]
        self.currentState = newState
        self.score += tempScore

    def getScore(self):
        return self.score

    def getCurrentState(self):
        return self.currentState




class MarioStateMachineEasyMode:

    def __init__(self):
        self.currentState = State.SMALL
        self.score = 0

    def obtainMushRoom(self):
        if self.currentState == State.SMALL:
            self.currentState = State.SUPER
            self.score += 100

    def obtainFireFlower(self):
        if self.currentState == State.SMALL or self.currentState == State.SUPER:
            self.currentState = State.FIRE
            self.score += 300

    def obtainCape(self):
        if self.currentState == State.SMALL or self.currentState == State.SUPER:
            self.currentState = State.CAPE
            self.score += 200

    def meetMonster(self):
        if self.currentState == State.SUPER:
            self.currentState = State.SMALL
            self.score -= 100
        elif self.currentState == State.CAPE:
            self.currentState = State.SMALL
            self.score -= 200
        elif self.currentState == State.FIRE:
            self.currentState = State.SMALL
            self.score -= 300

    def getScore(self):
        return self.score

    def getCurrentState(self):
        return self.currentState

if __name__ == '__main__':
    mario = MarioStateMachine2Dmode()
    print("当前状态: ",mario.getCurrentState(),"  ",mario.getScore())
    mario.obtainMushRoom()
    print("当前状态: ", mario.getCurrentState(), "  ", mario.getScore())
    mario.obtainCape()
    print("当前状态: ", mario.getCurrentState(), "  ", mario.getScore())
    mario.meetMonster()
    print("当前状态: ", mario.getCurrentState(), "  ", mario.getScore())
    mario.obtainFireFlower()
    print("当前状态: ", mario.getCurrentState(), "  ", mario.getScore())
    mario.meetMonster()
    print("当前状态: ", mario.getCurrentState(), "  ", mario.getScore())