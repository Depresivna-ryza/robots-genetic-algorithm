from __future__ import annotations
from typing import List, Set
from random import random, randint, choices, seed
from genetic_project.constants import *
from math import sin, cos, pi, atan2, sqrt
# from genetic_project.ViewController import best_fitness


seed(1)
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
    def __init__(self, ix,iy,ax,ay):
        self.min_x = ix
        self.min_y = iy
        self.max_x = ax
        self.max_y = ay

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
        self.location = Point(MIN_X + 10 , (MIN_Y + MAX_Y)/2)
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
    
    def tick(self, walls, target, ticks):
        self.speed = self.speed + self.acceleration * ACCELERATION_CONSTANT
        self.location += self.speed * SPEED_CONSTANT
        if not self.location.collides(MIN_X, MAX_X, MIN_Y, MAX_Y):
            self.alive_status = False
            # self.speed = self.speed * -1
            return
        for w in walls:
            if self.location.collides(w.min_x, w.max_x, w.min_y, w.max_y):
                # self.speed = self.speed * -1
                self.alive_status = False
                return
        if (self.location - target).size() <= TARGET_RADIUS // 2:
            self.finished = ticks
            self.alive_status = False

   
    def fitness_inverse(self, target):
        if self.finished is None:
            return 1 / (self.location - target).size()
        else:
            return (len(self.genome)*DIRECTION_CHANGE_TICKS - self.finished) / (self.location - target).size()
    
    def fitness_linear(self, target):
        max_len = sqrt((MAX_X - MIN_X)** 2 + (MAX_Y - MIN_Y)** 2)
        if self.finished is None:
            return max_len - (self.location - target).size()
        else:
            return max_len - (self.location - target).size() + 10*(len(self.genome)*DIRECTION_CHANGE_TICKS - self.finished) 

    def fitness_quadratic(self, target):
        return (self.fitness_linear(target) ** 2) 
    
    def fitness_exponential(self, target):
        return 2 ** (self.fitness_linear(target) / 500) 

    
    def make_children(parentA, parentB, mutation_prob):
        mid = randint(0, GENOME_SIZE - 1)
        child_genome = parentA.genome[:mid] + parentB.genome[mid:]

        for i in range(len(child_genome)):
            if random() <= mutation_prob:
                child_genome[i] = random_acceleration()
    
        return Robot(child_genome)
    
    def make_children2(parentA, parentB, mutation_prob):
        mid = randint(0, GENOME_SIZE - 1)
        child_genome = parentA.genome[:mid] + parentB.genome[mid:]

        for i in range(len(child_genome)):
            if random() <= mutation_prob:
                x = 0 #randint(0,2)
                if x == 0:
                    child_genome[i] = random_acceleration() #rand
                if x == 1:
                    child_genome[i] = child_genome[i-1] #duplicate
                if x == 2:
                    child_genome[i], child_genome[i-1] = child_genome[i-1], child_genome[i] # swap
    
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
    best_fitness: float

    def __init__(self, robots = None, no_mutation = False):
        self.robots = robots if robots else [Robot([random_acceleration() for _ in range(GENOME_SIZE)]) for _ in range(ROBOTS_COUNT)]
        self.walls = walls5()
        self.ticks = 0
        self.alive = True
        self.target = Point(MAX_X, ( MAX_Y + MIN_Y ) / 2)
        self.mutation_prob = MUTATION_PROBABILITY * (random()*2)**3  if not no_mutation else LOW_MUTATION_PROBABILITY
        # self.mutation_prob = MUTATION_PROBABILITY
    def tick(self) -> None:
        self.alive = False
        if self.ticks % DIRECTION_CHANGE_TICKS == 0:
            for r in self.robots:
                if r.alive_status:
                    r.change_acceleration()

        for r in self.robots:
            if r.alive_status:
                self.alive = True
                r.tick(self.walls, self.target, self.ticks)
    
        self.ticks += 1

    def is_finished(self) -> bool:
        return not self.alive

    
    def next_generation(self):
        res = []
        # fits = [x.fitness_inverse(self.target) for x in self.robots]
        # fits = [x.fitness_linear(self.target) for x in self.robots]
        fits = [x.fitness_quadratic(self.target) for x in self.robots]
        # fits = [x.fitness_exponential(self.target) for x in self.robots]
        max_i = max(range(len(self.robots)), key= (lambda i: fits[i]))
        # print(f"max fitness value: {fits[max_i]} ", end="")
        best_fitness = fits[max_i]

        best = Robot(self.robots[max_i].genome)
        if KEEP_BEST:
            res.append(best.make_children(best, self.mutation_prob))
        for _ in range(ROBOTS_COUNT - int(KEEP_BEST)):
            parentA, parentB = choices(self.robots, weights=fits, k=2)
            res.append(parentA.make_children2(parentB, self.mutation_prob))
        return res, best_fitness
            


def walls0():
    return []

def walls1():
    res = []
    step = 350
    for min_x in range(int(MIN_X) + 100, int(MAX_X//2), step):
        res.append(Wall(min_x, MIN_Y, min_x + 30, (MIN_Y + MAX_Y) / 2 + 60))
    
    for min_x in range(int(MIN_X) + 100 + step// 2, int(MAX_X//2), step):
        res.append(Wall(min_x, (MIN_Y + MAX_Y) / 2 - 60, min_x + 30, MAX_Y))
    return res

def walls2():
    res = []
    step = 300
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, step):
        res.append(Wall(min_x, MIN_Y, min_x + 20, (MIN_Y + MAX_Y) / 2 + 30))
    
    for min_x in range(int(MIN_X) + 100 + step// 2, int(MAX_X) - 100, step):
        res.append(Wall(min_x, (MIN_Y + MAX_Y) / 2 - 30, min_x + 20, MAX_Y))
    return res

def walls3():
    return [Wall(MIN_X + 100, MIN_Y + 100 ,MAX_X - 100, MAX_Y - 100)]

def walls4():
    res = []
    step = 400
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, step):
        res.append(Wall(min_x, MIN_Y + 50 , min_x + 20, MAX_Y - 50))

    for min_x in range(int(MIN_X) + 100 + step // 2, int(MAX_X) - 100, step):
        res.append(Wall(min_x, (MIN_X + MAX_X)/2 + 25 , min_x + 20, MAX_Y))
        res.append(Wall(min_x, MIN_Y , min_x + 20, (MIN_X + MAX_X)/2 - 25))

    return res

def walls5():
    res = []
    step = 170
    off = 150
    for min_x in range(int(MIN_X) + 100, int(MAX_X) - 100, step):
        res.append(Wall(min_x, MAX_Y - off ,       min_x + 20, MAX_Y))
        res.append(Wall(min_x, MIN_Y + off + 50 ,  min_x + 20, MAX_Y - off - 50))
        res.append(Wall(min_x, MIN_Y ,             min_x + 20, MIN_Y + off))

    for min_x in range(int(MIN_X) + 100 + step // 2, int(MAX_X) - 100, step):
        res.append(Wall(min_x, (MIN_X + MAX_X)/2 + 25 , min_x + 20, MAX_Y))
        res.append(Wall(min_x, MIN_Y , min_x + 20, (MIN_X + MAX_X)/2 - 25))

    return res



