#!/usr/bin/env python3

from turtle_movement.TurtleShape import TurtleShape

class TurtleRectangle(TurtleShape):
    def __init__(self):
        super().__init__()
        
    
    def move(self, speed=0.5, length=2): 
        print("Starting position: ", self.pose.x, self.pose.y)
        for _ in range(2):
            self.move_forward(speed=speed, distance=length)
            print("Position after side", _ + 1, ":", self.pose.x, self.pose.y)
            self.pub_checkpoint(_+1)
            self.rotate_half_pi(speed=0.5)
            print("Position after rotation", _ + 1, ":", self.pose.x, self.pose.y)
            self.move_forward(speed=speed, distance=2*length)
            print("Position after side", _ + 2, ":", self.pose.x, self.pose.y)
            self.rotate_half_pi(speed=0.5)
            print("Position after rotation", _ + 2, ":", self.pose.x, self.pose.y)
            self.pub_checkpoint(_ + 2)