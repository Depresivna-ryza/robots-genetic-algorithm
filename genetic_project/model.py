from __future__ import annotations
from typing import List, Set
from random import random, randint, choices
from genetic_project.constants import *
from math import sin, cos, pi, atan2, sqrt

__author__ = ""  # TODO

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
    def __init__(self, p : Point):
        self.min_x = p.x
        self.min_y = p.y
    
        r = random()
        self.max_x = self.min_x + WALL_SIZE * r
        self.max_y = self.min_y + WALL_SIZE * ( 1 - r )

class Robot:
    acceleration: Point
    location: Point
    speed: Point
    alive_status: bool
    collected_batteries: Set[Battery]
    genome: List[Point]
    genome_index: int
    

    def __init__(self, genome):
        self.genome = genome
        self.acceleration = genome[0]
        self.location = Point(MIN_X + 10, MIN_Y + 10)
        self.speed = genome[0] * INITIAL_SPEED
        self.alive_status = True
        self.collected_batteries = set()
        self.genome_index = 0
    
    def change_direction(self):
        self.genome_index += 1
        if self.genome_index < len(self.genome):
            self.acceleration = self.genome[self.genome_index]
        else:
            self.alive_status = False
    
    def tick(self, walls):
        self.speed = self.speed * (1/2) + (self.acceleration * ACCELERATION_CONSTANT)
        self.location = self.location + (self.speed * SPEED_CONSTANT)
        if not self.location.collides(MIN_X, MAX_X, MIN_Y, MAX_Y):
            self.alive_status = False
            return
        for w in walls:
            if self.location.collides(w.min_x, w.max_x, w.min_y, w.max_y):
                self.alive_status = False
                return
    
    def collect_batteries(self, batteries):
        for b in batteries:
            if (self.location - b.location).size() <= BATTERY_PICKUP_RADIUS \
                and b not in self.collected_batteries:
                self.collected_batteries.add(b)
                # print("collected")

                
    def fitness(self, batteries):
        min_dist = 0
        for b in batteries:
            d = (self.location - b.location).size()
            if d != 0 and 1/d > min_dist and b not in self.collected_batteries:
                min_dist = 1/d

        return len(self.collected_batteries) + min_dist * FITNESS_CONSTANT


class Battery:
    location: Point
    def __init__(self, position):
        self.location = position

def random_point() -> Point:
    return Point(randint(MIN_X, MAX_X), randint(MIN_Y, MAX_Y))

def random_acceleration() -> Point:
    alpha = 2 * pi * random()
    return Point(cos(alpha), sin(alpha))

class Model:
    robots: List[Robot]
    batteries: List[Battery]
    walls: List[Wall]
    time: int
    alive: bool

    def __init__(self, robots = None, batteries = None, walls = None):
        self.robots = robots if robots else [Robot([random_acceleration() for _ in range(GENOME_SIZE)]) for _ in range(ROBOTS_COUNT)]
        self.batteries = batteries if batteries else [Battery( random_point() ) for _ in range(BATTERIES_COUNT)]
        self.walls = walls if walls else [Wall(random_point()) for _ in range(WALL_COUNT)]
        self.time = 0
        self.alive = True

    def tick(self) -> None:
        # print(self.time)
        self.alive = False
        self.time += 1
        if self.time % DIRECTION_CHANGE_TICKS == 0:
            for r in self.robots:
                if r.alive_status:
                    r.change_direction()

        for r in self.robots:
            if r.alive_status:
                self.alive = True
                r.tick(self.walls)
                r.collect_batteries(self.batteries)
    
        if not self.alive:
            print("everything dead")

    def is_finished(self) -> bool:
        return not self.alive

    def next_gen(self):
        self.robots.sort(reverse=True, key=(lambda x: x.fitness(self.batteries)))
        return self.robots[:NEXT_GEN_COUNT]
        # weights = [x.fitness(self.batteries) for x in self.robots]
        # return choices(self.robots,weights=weights, k=NEXT_GEN_COUNT)

    def breed(self):
        candidates = self.next_gen()
        new_gen = []
        for _ in range(ROBOTS_COUNT):
            a, b = choices(candidates, k=2)
            genome = []
            flip = True
            for ag, bg in zip(a.genome, b.genome):
                if randint(0, FLIP_CONSTANT) == 0:
                    flip = not flip
                if randint(0, 20) == 0:
                    genome.append(random_acceleration())
                elif flip:
                    genome.append(ag)
                else:
                    genome.append(bg)
            new_gen.append(Robot(genome))
        return new_gen

    # def breed(self):
    #     candidates = self.next_gen()
    #     new_gen = []
    #     for _ in range(ROBOTS_COUNT):
    #         a = choices(candidates, k=1)
    #         new_gen.append(Robot(a[0].genome))
    #     return new_gen


