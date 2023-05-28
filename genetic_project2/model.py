from __future__ import annotations
from typing import List, Set
from random import random, randint, choices, seed
import math
from genetic_project2.constants import *
from math import sin, cos, pi, atan2, sqrt
from genetic_project2.utilities import *

seed(2)

class DNA:
    _DNA: dict
    def __init__(self):
        self._DNA = dict()
    def get_from_rays(self, speed, distances):
        # key = 0
        # for obj, dist in distances:
        #     key *= RAY_MAX_DISTANCE // RAY_DISTANCE_INCEMENT
        #     key += dist // RAY_DISTANCE_INCEMENT
        #     key *= 2
        #     key += obj
        
        # key *= SPEED_MAX
        # key += speed

        key = (speed, *distances)

        if key not in self._DNA.keys():
            self._DNA[key] = randint(0, 3)

        return self._DNA[key]
        

    def get_from_fixed(self, speed, detected_values):
        key = (speed, *detected_values)

        if key not in self._DNA.keys():
            self._DNA[key] = randint(0, 3)

        return self._DNA[key]
    

class Robot:
    location: Point
    speed: int
    direction: Angle
    alive_status: bool
    DNA: DNA
    distances: list[int]
    picked_up_batteries: set[Battery]
    time_of_death: int

    def __init__(self, _DNA = None):
        self.DNA = DNA() if _DNA is None else _DNA
        self.location = None # model class sets this attribute
        self.speed = SPEED_MIN
        self.direction = Angle(random())
        self.alive_status = True
        self.picked_up_batteries = set()
        self.time_of_death = MAX_TICKS
        self.direction_change = Angle(0) # helper variable for printing accurate oriantation angle

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
        self.direction += self.direction_change
        self.direction_change = Angle(0)
        self.location = Point(self.speed * cos(self.direction.to_radians()),
                              self.speed * sin(self.direction.to_radians())) + self.location

         
        self.distances = self.get_ray_distances(walls, batteries)
        new_direction = self.DNA.get_from_rays(self.speed, self.distances)

        # self.detected_values = self.get_fixed_distances(walls, batteries)
        # new_direction = self.DNA.get_fixed(self.speed, self.detected_values)

        if new_direction == UP:
            self.speed = min(SPEED_MAX, self.speed + SPEED_INCREMENT)
        elif new_direction == DOWN:
            self.speed = max( self.speed - SPEED_INCREMENT, SPEED_MIN)
        else:
            self.direction_change = Angle(ONE_ROTATION_ANGLE) if new_direction == RIGHT else Angle(-ONE_ROTATION_ANGLE)


    def tick(self, walls: List[Wall], batteries: List[Battery]):
        self.move(walls, batteries)
        self.collide_with_walls(walls)
        if self.alive_status:
            self.pick_up_batteries(batteries)


    def get_ray_distances(self, walls: List[Wall], batteries: List[Battery]):
        res = []
        for angle, max_dist in ROBOT_RAY_ANGLES:
            angle = (angle + self.direction.to_angle()) * 2 * pi
            dist = RAY_DISTANCE_INCEMENT // 2 # starting at 0 would be pointless, hence this arbitrary value
            found = False
            while not found:
                if dist > max_dist:
                    res.append((NOTHING, max_dist))
                    found = True
                    continue

                point = Point(dist*cos(angle), dist*sin(angle)) + self.location
                for w in walls:
                    if w.contains(point):
                        res.append((WALL, dist))
                        found = True
                        break
                else:
                    for b in batteries:
                        if b.contains(point) and b not in self.picked_up_batteries:
                            res.append((BATTERY, dist))
                            found = True
                            break
        
                dist += RAY_DISTANCE_INCEMENT

        return res

    def get_fixed_distances(self, walls: List[Wall], batteries: List[Battery]):
        res = []
        for angle in ROBOT_FIXED_ANGLES:
            angle = (angle + self.direction.to_angle()) * 2 * pi
            for dist in ROBOT_FIXED_DISTANCES:
                point = Point(dist*cos(angle), dist*sin(angle)) + self.location
                found = False
                for w in walls:
                    if w.contains(point):
                        res.append(WALL)
                        found = True
                        break
                if found:
                    continue
                for b in batteries:
                    if b.contains(point) and b not in self.picked_up_batteries:
                        res.append(BATTERY)
                        found = True
                        break
                if found:
                    continue
                res.append(NOTHING)
        return res

    def fitness(self, batteries): # returns fitness value between 0 and 1
        return (len(self.picked_up_batteries) / len(batteries)) * (self.time_of_death / MAX_TICKS) * (1 if self.alive_status else 0.1)
    
    def fitness2(self, batteries):
        return self.fitness(batteries) ** 2

    def fitness3(self, batteries):
        return self.fitness(batteries) ** 3
    
    def exp_fitness(self, batteries):
        return (2 ** self.fitness(batteries)) - 1

    
    def make_children(parentA: Robot, parentB: Robot, mutation_prob):
        child_DNA = DNA()
        dna_cutoff_prob = random()
        # print(parentA.DNA._DNA)
        child_DNA._DNA = parentA.DNA._DNA.copy()

        for key, value in parentB.DNA._DNA.items():
            if key not in child_DNA._DNA or random() < dna_cutoff_prob:
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

def random_point_outside_walls(walls: list[Wall]):
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
        walls_random, batteries_random = choices([(borders, batteries4),(walls2, batteries2), (walls3, batteries3), (walls4, batteries4), (walls5, batteries5)])[0]
        
        # change this values as needed
        self.walls = walls4() # walls_random()
        self.batteries = batteries4() # make_random()

        self.ticks = 0
        self.alive = True
        self.mutation_prob = MUTATION_PROBABILITY
        for r in self.robots:
            r.location = random_point_outside_walls(self.walls)
        
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
        fits = [x.fitness(self.batteries) for x in self.robots]
        if ELITISM_SELECTION:   
            max_i = max(range(len(self.robots)), key= (lambda i: fits[i]))
            best = self.robots[max_i]
            res.append( best.make_children(best, 0))
        best_fitness = max(fits)

        for _ in range(ROBOTS_COUNT if not ELITISM_SELECTION else ROBOTS_COUNT - 1):
            parentA, parentB = choices(self.robots, weights=fits, k=2)
            res.append(parentA.make_children(parentB, self.mutation_prob))

        if RETURN_BEST_FITNESS:
            return res, best_fitness
        return res, (sum(fits)/ len(fits))    

