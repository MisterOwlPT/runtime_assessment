#!/usr/bin/env python3
import argparse

from rospy.exceptions import ROSInterruptException

from turtle_movement.TurtleShape import TurtleShape
from turtle_movement.TurtleSquare import TurtleSquare
from turtle_movement.TurtleRectangle import TurtleRectangle

TRAJECTORY_RECTANGLE = "rectangle"
TRAJECTORY_SQUARE    = "square"


def main(trajectory: str) -> None:

    try:
        turtle: TurtleShape = {
            TRAJECTORY_RECTANGLE: TurtleRectangle,
            TRAJECTORY_SQUARE: TurtleSquare,
        }[trajectory]()
    except KeyError:
        # NOTE: argparse should avoid this point to be reached
        print(f"Invalid trajectory {trajectory}")
        exit(1)

    try:
        turtle.move()
    except ROSInterruptException:
        print("Interrupting execution...")
        raise


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="TurtleSim trajectory selector")
    parser.add_argument(
        "trajectory",
        type=str,
        help='Type of trajectory (must be "square" or "rectangle")',
        choices=[
            "square",
            "rectangle",
        ],
    )
    args = parser.parse_args()

    main(args.trajectory)
