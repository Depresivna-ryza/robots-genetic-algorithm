from __future__ import annotations
from typing import List, Set
from random import random, randint, choices, seed, Random
import math
from genetic_project2.constants import *
from math import sin, cos, pi, atan2, sqrt



class Point:
    x: float
    y: float
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def collides(self, min_x, max_x, min_y, max_y):
        return min_x <= self.x <= max_x and min_y <= self.y <= max_y
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    def __mul__(self, k):
        return Point(self.x * k, self.y * k)
    def to_angle(self) -> float:
        return atan2(self.y , self.x) * 180 / pi
    def size(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

class Angle:
    theta: float # angle represented as a number between 0 and 1, where 0 represents 0 radians and 1 represents 2pi radians
    def __init__(self, t: float):
        self.theta = t - math.floor(t)
    def to_x_y(self):
        return cos(self.theta * 2 * pi), sin(self.theta * 2 * pi)
    def __add__(self, other: Angle):
        a = self.theta + other.theta
        return Angle(a - math.floor(a))
    def __sub__(self, other: Angle):
        a = 1 + self.theta - other.theta
        return Angle(a - math.floor(a))
    def to_angle(self):
        return self.theta
    def to_radians(self):
        return self.theta * 2 * pi
    def to_degrees(self):
        return self.theta * 360

class Wall:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    def __init__(self, ix, iy, ax, ay):
        self.min_x = ix
        self.min_y = iy
        self.max_x = ax
        self.max_y = ay
    def contains(self, point: Point):
        return self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y

class Battery:
    def __init__(self, point : Point):
        self.coords: Point = point
    def contains(self, point):
        return (self.coords - point).size() <= BATTERY_RADIUS


def borders():
    res = []
    t = 10
    res.append(Wall(MIN_X - 30*t, MIN_Y - 30*t, MIN_X + t, MAX_Y + 30*t))
    res.append(Wall(MAX_X - t, MIN_Y - 30*t, MAX_X + 30*t, MAX_Y + 30*t))

    res.append(Wall(MIN_X - 30*t, MIN_Y - 30*t, MAX_X + 30*t, MIN_Y + t))
    res.append(Wall(MIN_X - 30*t, MAX_Y - t, MAX_X + 30*t, MAX_Y + 30*t))
    return res

def walls1(): 
    res = borders()
    size = 90
    offy = 180
    offx = offy * 1.5
    mid_x = (MIN_X + MAX_X) / 2
    mid_y = (MIN_Y + MAX_Y) / 2
    for x, y  in [(mid_x + offx, mid_y + offy), (mid_x + offx, mid_y - offy),
                  (mid_x - offx, mid_y + offy), (mid_x - offx, mid_y - offy), 
                  (mid_x, mid_y)]:
        res.append(Wall(x - size, y - size, x + size, y + size))
    
    return res

def batteries1():
    res = []
    offy = 180
    offx = offy * 1.5
    mid_x = (MIN_X + MAX_X) / 2
    mid_y = (MIN_Y + MAX_Y) / 2
    for x, y  in [(mid_x + offx, mid_y), (mid_x - offx, mid_y),
                  (mid_x, mid_y + offy), (mid_x, mid_y - offy),
                  (mid_x + 1.2*offx, mid_y), (mid_x - 1.2*offx, mid_y),
                  (mid_x, mid_y + 1.2*offy), (mid_x, mid_y -1.2*offy)]:
        res.append(Battery(Point(x, y)))
    
    return res

def walls2():
    res = borders()
    step = 100
    size = 50
    for x in range(int(MIN_X) , int(MAX_X), step):
        for y in range(int(MIN_Y) , int(MAX_Y), step):
            res.append(Wall(x, y, x + size, y + size))
    return res

def batteries2():
    res = []
    step = 100
    size = 75
    for x in range(int(MIN_X) + size, int(MAX_X), step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y), step):
            res.append(Battery(Point(x, y)))
    return res

def walls3():
    res = borders()
    step = 100
    size = 50
    for x in range(int(MIN_X) , int(MAX_X), step):
        for y in range(int(MIN_Y) , int(MAX_Y), step):
            if coinflip():
                res.append(Wall(x, y, x + size, y + size))
    return res

def batteries3():
    res = []
    step = 100
    size = 75
    for x in range(int(MIN_X) + size, int(MAX_X), step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y), step):
            if coinflip():
                res.append(Battery(Point(x, y)))
    return res


def walls4():
    res = []
    step = 240
    size = 120
    for x in range(int(MIN_X) , int(MAX_X), step):
        for y in range(int(MIN_Y) , int(MAX_Y), step):
            res.append(Wall(x, y, x + size, y + size))
    return choices(res, k = 3 * len(res) // 4) + borders()

def batteries4():
    res = []
    step = 120
    size = 60
    for x in range(int(MIN_X) + size, int(MAX_X), step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y), step):
            res.append(Battery(Point(x, y)))
    return choices(res, k =  len(res) // 2)


def walls4_constant():
    myrand = Random(1337)
    res = []
    step = 240
    size = 120
    for x in range(int(MIN_X) , int(MAX_X), step):
        for y in range(int(MIN_Y) , int(MAX_Y), step):
            res.append(Wall(x, y, x + size, y + size))
    return myrand.choices(res, k = 3 * len(res) // 4) + borders()

def batteries4_constant():
    myrand = Random(1337)
    res = []
    step = 120
    size = 60
    for x in range(int(MIN_X) + size, int(MAX_X), step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y), step):
            res.append(Battery(Point(x, y)))
    return myrand.choices(res, k =  len(res) // 2)


def walls5():
    res = borders()
    step = 220
    size = 150
    for x in range(int(MIN_X) , int(MAX_X) + step, step):
        for y in range(int(MIN_Y) , int(MAX_Y) + step, step):
            res.append(Wall(x, y, x + size, y + size))
    return res

def batteries5():
    res = []
    step = 110
    size = 75
    for x in range(int(MIN_X) + size, int(MAX_X) + step, step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y) + step, step):
            res.append(Battery(Point(x, y)))
    return res


def walls6():
    res = borders()
    step = 200
    size = 100
    for x in range(int(MIN_X) , int(MAX_X), step):
        for y in range(int(MIN_Y) , int(MAX_Y), step):
            res.append(Wall(x, y, x + size, y + size))
    return res

def batteries6():
    res = []
    step = 100
    size = 50
    for x in range(int(MIN_X) + size, int(MAX_X), step):
        for y in range(int(MIN_Y)+ size, int(MAX_Y), step):
            res.append(Battery(Point(x, y)))
    return res


def coinflip():
    return randint(0,1) == 1

