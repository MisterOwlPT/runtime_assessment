#!/usr/bin/env python3

from turtle_movement.TurtleShape import TurtleShape

class TurtleSquare(TurtleShape):
    def __init__(self):
        super().__init__()

    def move(self, speed=1, length=5): 
        print("Starting position: ", self.pose.x, self.pose.y)
        c = 1
        for _ in range(2):
            self.move_forward(speed=speed, distance=length)
            print("Position after side", c, ":", self.pose.x, self.pose.y)
            self.pub_checkpoint(c)
            self.publish_transform()  # Publish transform after moving forward
            c += 1

            self.rotate_half_pi(speed=0.5)
            print("Position after rotation", c, ":", self.pose.x, self.pose.y)
            self.publish_transform()  # Publish transform after rotation
            
            self.move_forward(speed=speed, distance=length)
            print("Position after side", c, ":", self.pose.x, self.pose.y)
            self.pub_checkpoint(c)
            self.publish_transform()  # Publish transform after moving forward
            c += 1

            self.rotate_half_pi(speed=0.5)
            print("Position after rotation", c, ":", self.pose.x, self.pose.y)
            self.publish_transform()  # Publish transform after rotation