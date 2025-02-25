# ROS Runtime Assessment 

A tool to perform runtime assessment of industrial robotics applications (ROS Melodic and Noetic).

It combines dynamic verification and real-time assessments to evaluate adherence to functional requirements, focusing on dynamic aspects like sensor data integration and service level agreements. The goal of this tool is to ensure robustness, performance, and reliability when deploying ROS applications on physical robots in real-world scenarios.

## Installation

- Clone this repository into the `/src` folder of your ROS workspace
- Install dependencies with the following command

```bash
rosdep install --from-paths src --ignore-src -r -y
```

- Compile and source your ROS workspace

```bash
catkin_make
source ./devel/setup.bash
```

## Usage

- Start ROS master node

```bash
roscore
```

- On a separate terminal launch the runtime assessment node _prior_ to the ROS node you want to observe

```bash
python3 src/main.py <CONFIGURATION_PATH>
```

- Start the remaining nodes of your application (including the node to observe). The runtime assessment node automatically detects the target node and starts the assessment process. 

- Wait for the assessment process to finalize. 

- Open the generated log files and evaluate the compliance of your ROS application with the specified requirements.

### Example node for controlling TurtleSim

This package provides an auto-pilot node for TurtleSim and a sample YAML configuration file to access different trajectories.

To run this example you'll need to:

- Install [TurtleSim](http://wiki.ros.org/turtlesim):

```bash
sudo apt-get install ros-$(rosversion -d)-turtlesim
```

- Launch the runtime assessment node as explained before. Use the configuration file path `examples/turtlesim/specifications.yaml`

- Start TurtleSim node

```bash
rosrun turtlesim turtlesim_node
```

- Start the auto-pilot node

```bash
python3 examples/turtlesim/test_turtle.py
```

## YAML Configuration File & Schema 

This tool is configured using YAML files (one _for each_ ROS node to be inspected) divided into two main sections: `setup` and `specifications`.

### 1. Setup Section

The `setup` section contains high-level configuration parameters.

#### Fields

- `target_node` (`string`) - **REQUIRED**: 
  - **Description**: Name of the ROS node to be assessed.
  - **Example**: `/ur_manipulator_node`

- `topics` (`map[string, string]`) - **REQUIRED**: 
  - **Description**: A mapping of topic names to their corresponding message types.
  - **Example**:
    ```yaml
    topics:
      turtle1/pose: turtlesim/Pose  
      turtle1/cmd_vel: geometry_msgs/Twist  
      turtle1/checkpoint: std_msgs/String
      tf: tf2_msgs/TFMessage
    ```

- `logger_path` (`string`): 
  - **Description**: The path where output logs will be stored. A new directory `/logs` is automatically created.
  - **Example**: `~/home/user/catkin_ws/assessment_logs`
  - **Default**: `../logs`

- `rate` (`int`): 
  - **Description**: The refresh rate for new events. Value in seconds.
  - **Example**: `60`
  - **Default**: `10`

### 2. Specifications Section

The `specifications` section contains a list of functional requirements associated with the ROS topics defined in the `setup` section. Each specification can have different parameters based on the field `mode` (i.e., the type of functional requirement).

#### Common fields

- `topic` (string) - **REQUIRED**: 
  - **Description**: The name of the topic to monitor.
  - **Example**: `turtle1/pose`

- `mode` (`string`): 
  - **Description**: The mode of operation for the specification. Possible values include:
    - `exists`: Check if all target requirements are true.
    - `absent`: Check if all target requirements are false.
    - `average`: Check if average of received values is within expected values.
    - `max`: Check if maximum value of received values is within expected values.
    - `min`: Check if minimum value of received values is within expected values.
    - `metric`: Check against a metric condition.
  - **Default**: `exists`

- `target` (`list[map]`) - **REQUIRED**: 
  - **Description**: A list of target values or conditions to check against. The structure of the target can vary based on the topic and mode.
  - Example:
    ```yaml
    target:
      - { x: 10, y: 5.5 }
      - { x: 5.5, y: 5.5 }
      # single field validation
      - data: "reached 1"
      - linear.x: 0.1
      # assess topic metrics
      - frequency:
        - min: 55
        - max: 65
    ```

#### Modes `absent` / `exists`

- `temporal_consistency` (`boolean`):
  - **Description**: Indicates whether to check for temporal consistency (i.e, messages should arrive by the specified order).
  - **Default**: `false`

- `tolerance` (`float`):
  - **Description**: The tolerance level for temporal consistency checks.
  - **Example**: `0.0`

- `timein` (`float`):
  - **Description**: The setup time to wait before starting to analyze messages.
  - **Example**: `1.0`

- `timeout` (`float`):
  - **Description**: The maximum time to wait for requirement to be verified.
  - **Example**: `30.0`

#### Mode `average`/ `max` / `metric` / `min`

- `comparator` (`string`): 
  - **Description**: The comparison operator used for metrics. Possible values include:
    - `<`, `>`, `<=`, `>=`, `!=`
