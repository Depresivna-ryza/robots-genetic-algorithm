from turtle import Turtle, Screen, done, onclick, write, bgcolor, width
from genetic_project2.model import Model
from genetic_project2.constants import *
from genetic_project2.utilities import *
from typing import Any
from time import time_ns
import pickle


best_fitness = -1
class ViewController:
    screen: Any
    pen: Turtle
    model: Model

    def __init__(self, model: Model):
        self.model = model
        self.screen = Screen()
        self.screen.setup(VIEW_WIDTH, VIEW_HEIGHT)
        self.screen.tracer(0, 0)
        self.screen.delay(0)
        self.screen.title("stale som najlepsi")
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        bgcolor(0.1,0.1,0.1)

    def start_simulation(self) -> None:
        input("Press Enter to start simulation:")
        print("Press Ctrl+C to stop simulation: (duh)" )
        global best_fitness
        try:
            for generation in range(GENERATIONS_MAX):
                if generation % GENERATION_PRINT_RATE == 0 or generation <= PRINT_FIRST_N_GENERATIONS:
                    while not self.model.is_finished():
                        self.tick(generation)
                else:
                    while not self.model.is_finished():
                        self.model.tick()
                next_gen , best_fitness = self.model.next_generation()
                self.model = Model(next_gen)
        except KeyboardInterrupt:
            if SAVE_ROBOTS:
                with open('data2.pkl', 'wb') as outp:
                    pickle.dump(self.model, outp, pickle.HIGHEST_PROTOCOL)


    def tick(self, generation) -> None:

        for _ in range(TICKS_PER_SCREEN_UPDATE):
            self.model.tick()
        self.pen.clear()

        for battery in self.model.batteries:
            self.pen.penup()
            self.pen.goto(battery.coords.x, battery.coords.y)
            self.pen.pendown()
            self.pen.color("cyan")
            self.pen.dot(2*BATTERY_RADIUS)
            self.pen.penup()

        for w in self.model.walls:
            draw_rec(self.pen, w.min_x, w.max_x, w.min_y, w.max_y)

        for robot in self.model.robots[:PRINT_ROBOTS_MAX]:
            self.pen.penup()
            self.pen.goto(robot.location.x, robot.location.y)
            self.pen.pendown()

            if not PRINT_DEAD_ROBOTS and not robot.alive_status:
                self.pen.color(ROBOT_COLOR if robot.alive_status else DEAD_ROBOT_COLOR)
                self.pen.dot(ROBOT_RADIUS / 3)
                continue
            
            self.pen.width(4)
            self.pen.color(ROBOT_SPEED_COLOR)
            self.pen.setheading(robot.direction.to_degrees())
            self.pen.forward(robot.speed * TURTLE_SPEED_INDICATOR_CONSTANT)
            self.pen.backward(robot.speed * TURTLE_SPEED_INDICATOR_CONSTANT)
            self.pen.width(1)

            self.pen.color(ROBOT_COLOR if robot.alive_status else DEAD_ROBOT_COLOR)
            self.pen.dot(ROBOT_RADIUS)

            for (obj, dist), (angle, _) in zip(robot.distances, ROBOT_RAY_ANGLES):
                if obj == NOTHING:
                    continue
                self.pen.setheading((robot.direction + Angle(angle)).to_degrees())
                self.pen.color("cyan" if obj == BATTERY else "red")
                self.pen.forward(dist)
                self.pen.backward(dist)
            # count = -1
            # for angle in ROBOT_FIXED_ANGLES:
            #     angle = (angle + robot.direction.to_angle()) * 2 * pi
            #     for dist in ROBOT_FIXED_DISTANCES:
            #         count += 1
            #         val = robot.detected_values[count]
            #         # if val == NOTHING:
            #         #     continue

            #         point = Point(dist*cos(angle), dist*sin(angle)) + robot.location
            #         self.pen.penup()
            #         self.pen.goto(point.x, point.y)
            #         self.pen.pendown()
            #         self.pen.color("blue" if val == BATTERY else "red" if val == WALL else "gray")
            #         self.pen.dot(4)

        self.pen.penup()
        self.pen.goto(MIN_X + 20, MAX_Y - 20)
        self.pen.pendown()
        self.pen.color("white")
        self.pen.write(f"tick: #{self.model.ticks}", font=("Arial", 20, "normal"))
        self.pen.penup()
        self.pen.goto(MIN_X + 200, MAX_Y - 20)
        self.pen.pendown()
        self.pen.color("white")
        self.pen.write(f"generation: #{generation}", font=("Arial", 20, "normal"))
        self.pen.penup()
        self.pen.goto(MIN_X + 500, MAX_Y - 20)
        self.pen.pendown()
        self.pen.color("white")
        self.pen.write(f"best fitness: {best_fitness}", font=("Arial", 20, "normal"))

        self.screen.update()

        if self.model.is_finished():
            return
        

def draw_rec(turtle, min_x, max_x, min_y, max_y):
    turtle.penup()
    turtle.begin_fill()
    turtle.color("gray")
    turtle.goto(min_x, min_y)
    turtle.pendown()
    turtle.goto(max_x, min_y)
    turtle.goto(max_x, max_y)
    turtle.goto(min_x, max_y)
    turtle.goto(min_x, min_y)
    turtle.end_fill()
    turtle.penup()