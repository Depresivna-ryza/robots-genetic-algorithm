from turtle import Turtle, Screen, done, onclick, write, bgcolor
from genetic_project.model import Model
from genetic_project.constants import *
from typing import Any
from time import time_ns

NS_TO_MS: int = 1000000

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
        for generation in range(GENERATIONS_MAX):
            print(f"generation: {generation}")
            if generation % GENERATION_PRINT_RATE == 0:
                while not self.model.is_finished():
                    self.tick()
                self.model = Model(self.model.next_generation())
            else:
                while not self.model.is_finished():
                    self.model.tick()
                if generation % GENERATION_PRINT_RATE >= (GENERATION_PRINT_RATE*3) // 4:
                    self.model = Model(self.model.next_generation(), NO_MUTATION_ON_PRINTED_GENERATION)
                else:
                    self.model = Model(self.model.next_generation())
        
        
        done()

    def tick(self) -> None:

        for _ in range(TICKS_PER_SCREEN_UPDATE):
            self.model.tick()
        self.pen.clear()

        for w in self.model.walls:
            draw_rec(self.pen, w.min_x, w.max_x, w.min_y, w.max_y)

        for robot in self.model.robots:
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

        # self.pen.penup()
        # self.pen.begin_fill()
        # self.pen.color("blue")
        # self.pen.goto(MAX_X - 8, MIN_Y - 100)
        # self.pen.pendown()
        # self.pen.goto(MAX_X - 8, MAX_Y + 100)
        # self.pen.goto(MAX_X + 8, MAX_Y + 100)
        # self.pen.goto(MAX_X + 8, MIN_Y - 100)
        # self.pen.goto(MAX_X - 8, MIN_Y - 100)
        # self.pen.end_fill()
        # self.pen.penup()

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