from __future__ import annotations
from typing import List, Set
from random import random, randint, choices, seed
import math
from genetic_project.constants import *
from math import sin, cos, pi, atan2, sqrt
from genetic_project2.utilities import *

seed(1)

class DNA:
    _DNA: dict
    def __init__(self):
        self._DNA = dict()
    def get(self, speed, distances):
        key = 0
        for obj, dist in distances:
            key *= RAY_MAX_DISTANCE // RAY_DISTANCE_INCEMENT
            key += dist // RAY_DISTANCE_INCEMENT
            key *= 2
            key += obj
        
        key *= SPEED_MAX
        key += speed

        if key not in self._DNA.keys():
            self._DNA[key] = randint(0, 3)

        return self._DNA[key]
    

class Robot:
    location: Point
    speed: int
    direction: Angle
    alive_status: bool
    DNA: DNA
    distances: list
    picked_up_batteries: set[Battery]
    time_of_death: int

    def __init__(self, _DNA = None):
        self.DNA = DNA() if _DNA is None else _DNA
        self.location = random_point()
        self.speed = 1
        self.direction = Angle(random())
        self.alive_status = True
        self.picked_up_batteries = set()
        self.time_of_death = MAX_TICKS
    
    def collide_with_walls(self, walls: list[Wall]):
        for w in walls:
            if w.contains(self.location):
                self.alive_status = False
                break

    def pick_up_batteries(self, batteries: list[Battery]):
        for b in batteries:
            if b not in self.picked_up_batteries and b.contains(self.location):
                self.picked_up_batteries.add(b)
                break

    def move(self, walls: List[Wall], batteries: List[Battery]):
        self.distances = self.get_ray_distances(walls, batteries)
        new_direction = self.DNA.get(self.speed, self.distances)
        if new_direction == UP:
            self.speed = min(SPEED_MAX, self.speed + 1)
        elif new_direction == DOWN:
            if self.speed == SPEED_MIN:
                self.direction += Angle(0.5 + (random() - 0.5) * 0.1)
            else:
                self.speed -= 1
        else:
            self.direction += Angle(ONE_ROTATION_ANGLE) if new_direction == RIGHT else Angle(-ONE_ROTATION_ANGLE)


        newpoint = Point(self.speed * cos(self.direction.to_radians()),
                         self.speed * sin(self.direction.to_radians())) + self.location
        self.location = newpoint

    def tick(self, walls: List[Wall], batteries: List[Battery]):
        self.move(walls, batteries)
        self.collide_with_walls(walls)
        if self.alive_status:
            self.pick_up_batteries(batteries)


    def get_ray_distances(self, walls: List[Wall], batteries: List[Battery]):
        res = []
        for angle in ROBOT_RAY_ANGLES:
            angle = (angle + self.direction.to_angle()) * 2 * pi
            dist = 0
            found = False
            while not found:
                dist += RAY_DISTANCE_INCEMENT
                if dist >= RAY_MAX_DISTANCE:
                    res.append((WALL, RAY_MAX_DISTANCE))
                    found = True

                point = Point(dist*cos(angle), dist*sin(angle)) + self.location
                for w in walls:
                    if w.contains(point):
                        res.append((WALL, dist))
                        found = True
                        break

                for b in batteries:
                    if b.contains(point) and b not in self.picked_up_batteries:
                        res.append((BATTERY, dist))
                        found = True
                        break

        return res
    
    def fitness(self):
        return (len(self.picked_up_batteries)) ** 3 * (10 if self.alive_status else 1) * (self.time_of_death / MAX_TICKS )

    
    def make_children(parentA: Robot, parentB: Robot, mutation_prob):
        child_DNA = DNA()
        # print(parentA.DNA._DNA)
        for key, value in parentA.DNA._DNA.items():
            child_DNA._DNA[key] = value
        for key, value in parentB.DNA._DNA.items():
            if key not in child_DNA._DNA or randint(0,1):
                child_DNA._DNA[key] = value
        
        for key, value in child_DNA._DNA.items():
            if random() < mutation_prob:
                child_DNA._DNA[key] = randint(0,3)
        return Robot(child_DNA)


def random_point() -> Point:
    return Point(randint(MIN_X, MAX_X), randint(MIN_Y, MAX_Y))

def random_acceleration() -> Point:
    alpha = 2 * pi * random()
    return Point(cos(alpha), sin(alpha))

def random_point_outside_walls(walls):
    ok = False
    while not ok:
        ok = True
        point = random_point()
        for w in walls:
            if w.contains(point):
                ok = False
                break
    return point


class Model:
    robots: List[Robot]
    walls: List[Wall]
    batteries: List[Battery]
    ticks: int
    alive: bool
    best_fitness: float

    def __init__(self, robots = None):
        self.robots = robots if robots else [Robot() for _ in range(ROBOTS_COUNT)]
        self.walls = walls3()
        self.batteries = batteries3()
        self.ticks = 0
        self.alive = True
        self.mutation_prob = MUTATION_PROBABILITY
        
    def tick(self) -> None:

        self.alive = False

        for r in self.robots:
            if r.alive_status:
                self.alive = True
                r.tick(self.walls, self.batteries)
                if not r.alive_status:
                    r.time_of_death = self.ticks
    
        self.ticks += 1

    def is_finished(self) -> bool:
        return not self.alive or self.ticks >= MAX_TICKS

 
    def next_generation(self):
        res: list[Robot] = []
        fits = [x.fitness() for x in self.robots]

        max_i = max(range(len(self.robots)), key= (lambda i: fits[i]))
        best_fitness = fits[max_i]

        # best = Robot(self.robots[max_i].DNA)
        for _ in range(ROBOTS_COUNT):
            parentA, parentB = choices(self.robots, weights=fits, k=2)
            res.append(parentA.make_children(parentB, self.mutation_prob))

        return res, best_fitness
    

