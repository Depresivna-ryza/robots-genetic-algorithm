from turtle import Turtle, Screen, done, onclick, write, bgcolor, width
from genetic_project.model import Model
from genetic_project.constants import *
from typing import Any
from time import time_ns


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
        self.screen.title("Najlepsi som")
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        bgcolor(0.1,0.1,0.1)

    def start_simulation(self) -> None:
        input("Press Enter to continue...")
        global best_fitness
        for generation in range(GENERATIONS_MAX):
            print(f"generation: {generation}")
            if generation % GENERATION_PRINT_RATE == 0 or generation <= PRINT_FIRST_N_GENERATIONS:
                while not self.model.is_finished():
                    if PRINT_BEST_ONLY:
                        self.tick_best_only(generation)
                    else:
                        self.tick(generation)
                
                next_gen , best_fitness = self.model.next_generation()
                self.model = Model(next_gen)
            else:
                while not self.model.is_finished():
                    self.model.tick()
                next_gen , best_fitness = self.model.next_generation()
                if generation % GENERATION_PRINT_RATE >= (GENERATION_PRINT_RATE*3) // 4:
                    self.model = Model(next_gen, NO_MUTATION_ON_PRINTED_GENERATION)
                else:
                    self.model = Model(next_gen)

        done()

    def tick(self, generation) -> None:

        for _ in range(TICKS_PER_SCREEN_UPDATE):
            self.model.tick()
        self.pen.clear()

        for w in self.model.walls:
            draw_rec(self.pen, w.min_x, w.max_x, w.min_y, w.max_y)

        for robot in self.model.robots:
            self.pen.penup()
            self.pen.goto(robot.location.x, robot.location.y)

            self.pen.pendown()
            self.pen.color(ROBOT_SPEED_COLOR)
            self.pen.setheading(robot.speed.to_angle())
            self.pen.forward(robot.speed.size() * TURTLE_SPEED_INDICATOR_CONSTANT)
            self.pen.backward(robot.speed.size() * TURTLE_SPEED_INDICATOR_CONSTANT)

            self.pen.color(ROBOT_COLOR if robot.alive_status else DEAD_ROBOT_COLOR)
            self.pen.width(8)
            self.pen.setheading(robot.acceleration.to_angle())
            self.pen.forward(robot.acceleration.size() * TURTLE_ACCELERATION_INDICATOR_CONSTANT)
            self.pen.backward(robot.acceleration.size() * TURTLE_ACCELERATION_INDICATOR_CONSTANT)
            self.pen.width(1)

            self.pen.color(ROBOT_COLOR if robot.alive_status else DEAD_ROBOT_COLOR)
            self.pen.dot(ROBOT_RADIUS)

        self.pen.penup()
        self.pen.goto(self.model.target.x, self.model.target.y)
        self.pen.pendown()
        self.pen.color("blue")
        self.pen.dot(TARGET_RADIUS)
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
        

    def tick_best_only(self, generation) -> None:

        self.model.tick()
        self.pen.clear()

        for w in self.model.walls:
            draw_rec(self.pen, w.min_x, w.max_x, w.min_y, w.max_y)

        robot = self.model.robots[0]
        self.pen.penup()
        self.pen.goto(robot.location.x, robot.location.y)

        self.pen.pendown()
        self.pen.color("green")
        self.pen.setheading(robot.speed.to_angle())
        self.pen.forward(robot.speed.size() * TURTLE_SPEED_INDICATOR_CONSTANT)
        self.pen.backward(robot.speed.size() * TURTLE_SPEED_INDICATOR_CONSTANT)

        self.pen.color("red")
        self.pen.setheading(robot.acceleration.to_angle())
        self.pen.forward(robot.acceleration.size() * TURTLE_ACCELERATION_INDICATOR_CONSTANT)
        self.pen.backward(robot.acceleration.size() * TURTLE_ACCELERATION_INDICATOR_CONSTANT)

        self.pen.color("green" if robot.alive_status else "red")
        self.pen.dot(ROBOT_RADIUS)

        self.pen.penup()
        self.pen.goto(self.model.target.x, self.model.target.y)
        self.pen.pendown()
        self.pen.color("blue")
        self.pen.dot(TARGET_RADIUS)
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

        self.screen.update()

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