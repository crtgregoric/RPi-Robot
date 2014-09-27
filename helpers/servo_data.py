#!/usr/bin/python

from motor_position import MotorPosition


class ServoData():

    LOW_VALUE = 0
    MID_VALUE = 0
    HIGH_VALUE = 0

    ABS_MAX_UNIT = 0.0

    CONTINUOUS = False

    MOTOR_POSITION = MotorPosition.NONE

    def __init__(self):
        return


class TowerProSG5010Data(ServoData):

    ABS_MAX_UNIT = 100.0

    CONTINUOUS = True


class TowerProSG5010RightData(TowerProSG5010Data):

    LOW_VALUE = 300
    MID_VALUE = 340
    HIGH_VALUE = 390

    MOTOR_POSITION = MotorPosition.RIGHT


class TowerProSG5010LeftData(TowerProSG5010Data):

    LOW_VALUE = 290
    MID_VALUE = 330
    HIGH_VALUE = 380

    MOTOR_POSITION = MotorPosition.LEFT


class TowerProSG90Data(ServoData):

    LOW_VALUE = 120
    MID_VALUE = 307
    HIGH_VALUE = 550

    ABS_MAX_UNIT = 90.0

    CONTINUOUS = False

    MOTOR_POSITION = MotorPosition.NONE