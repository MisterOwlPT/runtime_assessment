#!/usr/bin/env python3
import argparse

from RuntimeAssessmentConfig import RuntimeAssessmentConfig
from RuntimeAssessment import RuntimeAssessment


def main(config_path: str) -> None:
    conf = RuntimeAssessmentConfig(config_path=config_path)
    runtime_assessment = RuntimeAssessment(config=conf)
    runtime_assessment.run()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ROS Runtime Assessment Node.")
    parser.add_argument("config", type=str, help="Path to the runtime assessment configuration file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the provided config path
    main(args.config)
