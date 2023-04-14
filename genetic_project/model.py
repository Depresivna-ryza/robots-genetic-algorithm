from __future__ import annotations
from typing import List, Set
from random import random, randint, choices
from genetic_project.constants import *
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
    


class Wall:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    def __init__(self, a,b,c,d):
        self.min_x = a
        self.min_y = b
        self.max_x = c
        self.max_y = d

class Robot:
    acceleration: Point
    location: Point
    speed: Point
    alive_status: bool
    genome: List[int]
    genome_index: int
    finished: None|int
    

    def __init__(self, genome):
        self.genome = genome
        self.acceleration = Point(0,0)
        self.location = Point(MIN_X , (MIN_Y + MAX_Y)/2)
        self.speed = Point(0, 0)
        self.alive_status = True
        self.genome_index = 0
        self.finished = None
        #TODO: add finish time 
    
    def change_acceleration(self):
        self.genome_index += 1
        if self.genome_index < len(self.genome):
            self.acceleration = self.genome[self.genome_index]
        else:
            self.alive_status = False
    
    def tick(self, walls, target):
        self.speed = self.speed + self.acceleration * ACCELERATION_CONSTANT
        self.location += self.speed * SPEED_CONSTANT
        if not self.location.collides(MIN_X, MAX_X, MIN_Y, MAX_Y):
            self.alive_status = False
            return
        for w in walls:
            if self.location.collides(w.min_x, w.max_x, w.min_y, w.max_y):
                self.alive_status = False
                return
        if (self.location - target).size() <= TARGET_RADIUS:
            self.finished = self.genome_index
            self.alive_status = False

   
    def fitness(self, target):
        return (len(self.genome) - self.finished + 5 if self.finished else 1) / (self.location - target).size()
    
    def make_children(parentA, parentB, mutation_prob):
        mid = randint(0, GENOME_SIZE - 1)
        child_genome = parentA.genome[:mid] + parentB.genome[mid:]
        for i in range(len(child_genome)):
            if random() <= mutation_prob:
                child_genome[i] = random_acceleration()
    
        return Robot(child_genome)

def random_point() -> Point:
    return Point(randint(MIN_X, MAX_X), randint(MIN_Y, MAX_Y))

def random_acceleration() -> Point:
    alpha = 2 * pi * random()
    return Point(cos(alpha), sin(alpha))


class Model:
    robots: List[Robot]
    walls: List[Wall]
    target: Point
    ticks: int
    alive: bool

    def __init__(self, robots = None, no_mutation = False):
        self.robots = robots if robots else [Robot([random_acceleration() for _ in range(GENOME_SIZE)]) for _ in range(ROBOTS_COUNT)]
        self.walls = walls2()
        self.ticks = 0
        self.alive = True
        self.target = Point(MAX_X, ( MAX_Y + MIN_Y ) / 2)
        self.mutation_prob = MUTATION_PROBABILITY * random()**3 if not no_mutation else 0

    def tick(self) -> None:
        self.alive = False
        if self.ticks % DIRECTION_CHANGE_TICKS == 0:
            for r in self.robots:
                if r.alive_status:
                    r.change_acceleration()

        for r in self.robots:
            if r.alive_status:
                self.alive = True
                r.tick(self.walls, self.target)
    
        if not self.alive:
            pass
            # print("everything dead")
        self.ticks += 1

    def is_finished(self) -> bool:
        return not self.alive

    
    def next_generation(self):
        res = []
        fits = [x.fitness(self.target) for x in self.robots]
        max_i = max(range(len(self.robots)), key= (lambda i: fits[i]))
        print(f"max fitness value: {fits[max_i]} ", end="")
        res.append(Robot(self.robots[max_i].genome))
        for _ in range(ROBOTS_COUNT - 1):
            parentA, parentB = choices(self.robots, weights=fits, k=2)
            res.append(parentA.make_children(parentB, self.mutation_prob))
        return res
            


def walls0():
    return []

def walls1():
    res = []
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, 300):
        res.append(Wall(min_x, MIN_Y, min_x + 10, (MIN_Y + MAX_Y) / 2 + 30))
    
    for min_x in range(int(MIN_X) + 100 + 150, int(MAX_X) - 100, 300):
        res.append(Wall(min_x, (MIN_Y + MAX_Y) / 2 - 30, min_x + 10, MAX_Y))
    return res


def walls2():
    res = []
    step = 300
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, step):
        res.append(Wall(min_x, MIN_Y, min_x + 10, (MIN_Y + MAX_Y) / 2 + 30))
    
    for min_x in range(int(MIN_X) + 100 + step// 2, int(MAX_X) - 100, step):
        res.append(Wall(min_x, (MIN_Y + MAX_Y) / 2 - 30, min_x + 10, MAX_Y))
    return res

def walls3():
    return [Wall((MIN_X + MAX_X)/2 - 20, MIN_Y + 100 ,(MIN_X + MAX_X)/2 + 50, MAX_Y - 100)]

def walls4():
    res = []
    step = 300
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, step):
        res.append(Wall(min_x, MIN_Y + 100 , min_x + 20, MAX_Y - 100))

    for min_x in range(int(MIN_X) + 100 + step // 2, int(MAX_X) - 100, step):
        res.append(Wall(min_x, (MIN_X + MAX_X)/2 + 50 , min_x + 20, MAX_Y))
        res.append(Wall(min_x, MIN_Y , min_x + 20, (MIN_X + MAX_X)/2 - 50))



