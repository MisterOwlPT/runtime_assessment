import yaml
import sys


def validate_config(config) -> None:
    """
    Validate the configuration file by checking if required fields are present.
    :param config: dict
    :return: None
    """

    required_keys = ['setup', 'specifications']

    for key in required_keys:
        if key not in config.keys():
            raise ValueError(f"Missing required key '{key}' in configuration")

    for key in config.keys():
        if key not in required_keys:
            raise ValueError(f"Invalid key '{key}' in configuration")

    for specs in config["specifications"]:
        if "topic" not in specs.keys() and "metric" not in specs.keys():
            raise ValueError("Missing 'topic' or 'metric' in specifications")

        if "target" not in specs.keys():
            raise ValueError("Missing 'target' in specifications")


def parse_yaml_config(yaml_file) -> dict:
    """
    Parse the YAML configuration file.
    :param yaml_file: str
    :return: dict
    """
    try:
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)

        # validate the file before returning
        validate_config(config)

        return config

    except FileNotFoundError:
        sys.exit(f"Configuration file not found: {yaml_file}")

    except ValueError as e:
        sys.exit(f"Configuration file error: {e}")

    except Exception as e:
        sys.exit(f"Unexpected Error: {e}")


class RuntimeAssessmentConfig:
    """
    Class to load the configuration file for the runtime assessment.
    """

    def __init__(self, config_path: str = "specifications.yaml"):
        self.rate = None
        self.topics = None
        self.target_node = None
        self.logger_path = None

        self.config_path = config_path

        # execute parsing methods at initialization
        self.config = parse_yaml_config(self.config_path)
        self.parse_setup()
        self.specifications = self.parse_specifications()

    def parse_setup(self) -> None:
        """
        Parse the setup parameters.
        :return: None
        """
        setup = self.config["setup"]

        keys = set(setup.keys())

        # set default values to missing setup parameters
        if "target_node" not in keys:
            raise ValueError("Missing 'target_node' in setup")
        else:
            self.target_node = setup["target_node"]

        if "topics" not in keys:
            raise ValueError("Missing 'topics' in setup")
        else:
            self.topics = setup["topics"]

        if "rate" not in keys:
            self.rate = 10
        else:
            self.rate = setup["rate"]

        if "logger_path" not in keys:
            self.logger_path = "../log"
        else:
            self.logger_path = setup["logger_path"]

    def parse_specifications(self) -> dict:
        """
        Parse the specifications and output the requirements grouped by type of assessment, and for ros_topic assessments, grouped by topic.
        :return: dict
        """
        conf = self.config["specifications"]

        requirements = {"topic": {}, "metric": {}}

        # traverse all specified requirements and restructure for easier handling
        for spec in conf:
            # group requirements by assessment type (topic or metric)
            if "topic" in spec.keys():
                aux_dict = {}
                topic = spec["topic"]

                # group requirements by topic
                if topic not in requirements["topic"].keys():
                    requirements["topic"][topic] = []

                for field, value in spec.items():
                    if field != "topic":
                        aux_dict[field] = value

                requirements["topic"][topic].append(aux_dict)

            elif "metric" in spec.keys():
                aux_dict = {}
                metric = spec["metric"]

                # group requirements bt metric
                if metric not in requirements["metric"].keys():
                    requirements["metric"][metric] = []

                for field, value in spec.items():
                    if field != "metric":
                        aux_dict[field] = value

                requirements["metric"][metric].append(aux_dict)

        return requirements
