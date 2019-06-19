import logging
from aenum import Enum, auto

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class State(Enum):

    ERROR = -1

    BACK = auto()
    FORWARD = auto()

    LINEAR = auto()
    ROTATIONAL = auto()

    CLOCKWISE = auto()
    ANTICLOCKWISE = auto()

    NO_TURN = auto()
    TURN = auto()
    DOUBLE_TURN = auto()

class Arm:
    def __init__(self, linear_servo, rotational_servo,
                 linear_low, linear_high, rotation_low, rotation_high,
                 current_linear, current_rotational,
                 rotation_speed, command_delay):
        """
        Create an object to represent an arm of the rubik's solver cube.

        :param linear_servo: Index of the linear servo.
        :param rotational_servo: Index of the rotational servo.
        :param linear_low: The low position of the linear servo.
        :param linear_high: The high position of the linear servo.
        :param rotation_low: The low position of the rotational servo.
        :param rotation_high: The high position of the rotational servo.
        :param current_linear: The current position of the linear servo.
        :param current_rotational: The current position of the rotational servo.
        :param rotation_speed: The speed of rotation of a servo in seconds/degree.
        :param command_delay: The amount of delay to add between commands as measured in seconds.
        """
        self.linear_servo = linear_servo
        self.rotational_servo = rotational_servo

        self.linear_low = linear_low
        self.linear_high = linear_high
        self.rotation_low = rotation_low
        self.rotation_high = rotation_high

        self.current_linear = current_linear
        self.current_rotational = current_rotational

        self.rotation_speed = rotation_speed
        self.command_delay = command_delay

        if (self.current_linear != self.linear_low and self.current_linear != self.linear_high) or \
            (self.current_rotational != self.rotation_low and self.current_rotational != self.rotation_high):
            raise RuntimeError('the current values of the servos don\'t match the permitted high/low vals')

    def check_position(self, axis):
        """
        Gets the current position of the arm depending on which axis is referred to.

        This method must be used in conjunction with rotate/move methods to verify if a certain movement can be done.

        :param axis: Can be LINEAR or ROTATIONAL.
        :return: The arms position for the given servo of the arm: BACK or FORWARD. ERROR is returned is the axis argument is bad.
        """

        position = State.ERROR
        if axis == State.LINEAR:
            if self.current_linear == self.linear_low:
                position = State.BACK
            elif self.current_linear == self.linear_high:
                position = State.FORWARD
        elif axis == State.ROTATIONAL:
            if self.current_rotational == self.rotation_low:
                position = State.BACK
            elif self.current_rotational == self.rotation_high:
                position = State.FORWARD

        return position


    def check_dof(self, axis, way):
        """
        Checks if a turn can be done depending on which axis is referred to.
        It's also dependent on the way it's being looked at.

        This method must be used in conjunction with rotate/move methods to verify if a certain movement can be done.

        :param axis: Can be LINEAR or ROTATIONAL.
        :param way: Can be FORWARD/BACK for LINEAR or CLOCKWISE/ANTICLOCKWISE for ROTATIONAL.
        :return: The amount of turns that can be done in the given way: NO_TURN or TURN.
            ERROR is returned is the axis argument is bad.
        """
        dof = State.ERROR
        if axis == State.LINEAR:

            if way == State.BACK:
                if self.current_linear == self.linear_low:
                    dof = State.NO_TURN
                elif self.current_linear == self.linear_high:
                    dof = State.TURN

            elif way == State.FORWARD:
                if self.current_linear == self.linear_low:
                    dof = State.TURN
                elif self.current_linear == self.linear_high:
                    dof = State.NO_TURN

        elif axis == State.ROTATIONAL:

            if way == State.CLOCKWISE:
                if self.current_rotational == self.rotation_low:
                    dof = State.TURN
                elif self.current_rotational == self.rotation_high:
                    dof = State.NO_TURN

            elif way == State.ANTICLOCKWISE:
                if self.current_rotational == self.rotation_low:
                    dof = State.NO_TURN
                elif self.current_rotational == self.rotation_high:
                    dof = State.TURN

        return dof

    def rotate(self, way, add_servo_delay=True, add_command_delay=True):
        """
        Rotate the arm's servo that's designated for rotating the cube.

        :param way: CLOCKWISE or ANTICLOCKWISE.
        :param add_servo_delay: True if it must be waited for the servo's command to finish. False otherwise.
        :param add_command_delay:  True if a delay is to be put between commands. False otherwise.
        :return: A dictionary with the 'servo', 'linear', 'rotational', 'position', 'time' keys that
            specify which servo to rotate, whether it's a rotational servo of the arm or not, what's the
            new position of the servo and the amount of time needed to execute the command. None is returned
            if the action is not accepted.
        """

        turns = self.check_dof(State.ROTATIONAL, way)
        done = False
        time = 0.0

        if turns == State.TURN:

            time += abs(self.rotation_low - self.rotation_high) * self.rotation_speed
            if self.current_rotational == self.rotation_low:
                self.current_rotational = self.rotation_high
            elif self.current_rotational == self.rotation_high:
                self.current_rotational = self.rotation_low
            done = True

        if done:
            if not add_servo_delay:
                time = 0.0
            if add_command_delay:
                time += self.command_delay
            step = {
                'servo': self.rotational_servo,
                'linear': False,
                'rotational': True,
                'position': self.current_rotational,
                'time': time
            }

            return step
        else:
            return None



    def move(self, position, add_servo_delay=True, add_command_delay=True):
        """
        Move the arm's servo that's designated for sliding the arm.

        :param position: Position of the arm to move to. Can be BACK or FORWARD. Use check_dof method to see if that's possible.
        :param add_servo_delay: True if a delay is to be put between commands. False otherwise.
        :param add_command_delay: True if it must be waited for the servo's command to finish. False otherwise.
        :return: A dictionary with the 'servo', 'linear', 'rotational', 'position', 'time' keys that
            specify which servo to rotate, whether it's a rotational servo of the arm or not, what's the
            new position of the servo and the amount of time needed to execute the command. None is returned
            if the action is not accepted.
        """

        turns = self.check_dof(State.LINEAR, position)
        done = False
        time = 0.0

        if turns == State.TURN:

            time += abs(self.linear_low - self.linear_high) * self.rotation_speed
            if self.current_linear == self.linear_low:
                self.current_linear = self.linear_high
            elif self.current_linear == self.linear_high:
                self.current_linear = self.linear_low
            done = True

        if done:
            if not add_servo_delay:
                time = 0.0
            if add_command_delay:
                time += self.command_delay
            step = {
                'servo': self.linear_servo,
                'linear': True,
                'rotational': False,
                'position': self.current_linear,
                'time': time
            }

            return step
        else:
            return None

    def reposition_linear(self, delay=0.0):
        step = {
            'servo': self.linear_servo,
            'linear': True,
            'rotational': False,
            'position': self.current_linear,
            'time': delay
        }
        return step

    def reposition_rotational(self, delay=0.0):
        step = {
            'servo': self.rotational_servo,
            'linear': False,
            'rotational': True,
            'position': self.current_rotational,
            'time': delay
        }
        return step

class ArmSolutionGenerator:
    def __init__(self, down, left, up, right):
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        self.reset_arm_solution()

    def fix(self):
        self.arms_solution += [
                self.up.rotate(State.ANTICLOCKWISE, False, False),
                self.right.rotate(State.ANTICLOCKWISE, False, False),
                self.down.rotate(State.ANTICLOCKWISE, False, False),
                self.left.rotate(State.ANTICLOCKWISE),

                self.up.move(State.FORWARD, False, False),
                self.right.move(State.FORWARD, False, False),
                self.down.move(State.FORWARD, False, False),
                self.left.move(State.FORWARD)
            ]

    def release(self):
        self.arms_solution += [
                self.up.move(State.BACK, False, False),
                self.right.move(State.BACK, False, False),
                self.down.move(State.BACK, False, False),
                self.left.move(State.BACK),

                self.up.rotate(State.ANTICLOCKWISE, False, False),
                self.right.rotate(State.ANTICLOCKWISE, False, False),
                self.down.rotate(State.ANTICLOCKWISE, False, False),
                self.left.rotate(State.ANTICLOCKWISE)
            ]

    def reposition_arms(self, delay):
        self.arms_solution += [
            self.up.reposition_linear(),
            self.up.reposition_rotational(),
            self.right.reposition_linear(),
            self.right.reposition_rotational(),
            self.down.reposition_linear(),
            self.down.reposition_rotational(),
            self.left.reposition_linear(),
            self.left.reposition_rotational(delay)
        ]

    def reset_arm_solution(self):
        self.arms_solution = []

    def __inverse_way(self, way):
        if way == State.CLOCKWISE:
            return State.ANTICLOCKWISE
        else:
            return State.CLOCKWISE

    def rotate(self, action):
        if '2' in action:
            turns = State.DOUBLE_TURN
            way = State.CLOCKWISE
        elif '\'' in action:
            turns = State.TURN
            way = State.ANTICLOCKWISE
        else:
            turns = State.TURN
            way = State.CLOCKWISE

        face = action[0]
        if face == 'F':
            self.rotate_front(turns, way)
        elif face == 'U':
            self.rotate_up(turns, way)
        elif face == 'R':
            self.rotate_right(turns, way)
        elif face == 'L':
            self.rotate_left(turns, way)
        elif face == 'D':
            self.rotate_down(turns, way)
        elif face == 'B':
            self.rotate_back(turns, way)

    def rotate_up(self, turns, way):
        self.arms_solution += [self.down.move(State.FORWARD)]

        if turns == State.TURN:
            if way == State.CLOCKWISE:
                self.arms_solution += [
                        self.up.rotate(way),
                        self.up.move(State.BACK),
                        self.up.rotate(self.__inverse_way(way)),
                        self.up.move(State.FORWARD)
                    ]
            elif way == State.ANTICLOCKWISE:
                self.arms_solution += [
                        self.up.move(State.BACK),
                        self.up.rotate(self.__inverse_way(way)),
                        self.up.move(State.FORWARD),
                        self.up.rotate(way)
                    ]
        elif turns == State.DOUBLE_TURN:
            self.rotate_up(State.TURN, way)
            self.rotate_up(State.TURN, way)

    def rotate_right(self, turns, way):
        if turns == State.TURN:
            if way == State.CLOCKWISE:
                self.arms_solution += [
                        self.right.rotate(way),
                        self.right.move(State.BACK),
                        self.right.rotate(self.__inverse_way(way)),
                        self.right.move(State.FORWARD)
                    ]
            elif way == State.ANTICLOCKWISE:
                self.arms_solution += [
                        self.right.move(State.BACK),
                        self.right.rotate(self.__inverse_way(way)),
                        self.right.move(State.FORWARD),
                        self.right.rotate(way)
                    ]
        elif turns == State.DOUBLE_TURN:
            self.rotate_right(State.TURN, way)
            self.rotate_right(State.TURN, way)

    def rotate_down(self, turns, way):
        if turns == State.TURN:
            if way == State.CLOCKWISE:
                self.arms_solution += [
                        self.right.move(State.BACK, False, False),
                        self.left.move(State.BACK),

                        self.down.move(State.BACK),
                        self.right.move(State.FORWARD, False, False),
                        self.left.move(State.FORWARD),

                        self.down.rotate(way, turns),
                        self.right.move(State.BACK, False, False),
                        self.left.move(State.BACK),
                        self.down.move(State.FORWARD),

                        self.right.move(State.FORWARD, False, False),
                        self.left.move(State.FORWARD),

                        self.down.move(State.BACK),
                        self.down.rotate(self.__inverse_way(way)),
                        self.down.move(State.FORWARD)
                    ]
            elif way == State.ANTICLOCKWISE:
                self.arms_solution += [
                        self.down.move(State.BACK),
                        self.down.rotate(self.__inverse_way(way)),
                        self.down.move(State.FORWARD),

                        self.right.move(State.BACK, False, False),
                        self.left.move(State.BACK),

                        self.down.move(State.BACK),
                        self.right.move(State.FORWARD, False, False),
                        self.left.move(State.FORWARD),

                        self.down.rotate(way),
                        self.right.move(State.BACK, False, False),
                        self.left.move(State.BACK),
                        self.down.move(State.FORWARD),

                        self.right.move(State.FORWARD, False, False),
                        self.left.move(State.FORWARD)
                    ]
        elif turns == State.DOUBLE_TURN:
            self.rotate_down(State.TURN, way)
            self.rotate_down(State.TURN, way)

    def rotate_left(self, turns, way):
        if turns == State.TURN:
            if way == State.CLOCKWISE:
                self.arms_solution += [
                        self.left.rotate(way),
                        self.left.move(State.BACK),
                        self.left.rotate(self.__inverse_way(way)),
                        self.left.move(State.FORWARD)
                    ]
            elif way == State.ANTICLOCKWISE:
                self.arms_solution += [
                        self.left.move(State.BACK),
                        self.left.rotate(self.__inverse_way(way)),
                        self.left.move(State.FORWARD),
                        self.left.rotate(way)
                    ]
        elif turns == State.DOUBLE_TURN:
            self.rotate_left(State.TURN, way)
            self.rotate_left(State.TURN, way)

    def rotate_cube_towards_right(self):
        self.arms_solution += [
                self.down.move(State.BACK),
                self.down.rotate(State.CLOCKWISE),
                self.down.move(State.FORWARD),

                self.right.move(State.BACK, False, False),
                self.left.move(State.BACK),

                self.up.rotate(State.CLOCKWISE, False, False),
                self.down.rotate(State.ANTICLOCKWISE),

                self.right.move(State.FORWARD, False, False),
                self.left.move(State.FORWARD),

                self.up.move(State.BACK),
                self.up.rotate(State.ANTICLOCKWISE),
                self.up.move(State.FORWARD)
            ]

    def rotate_cube_upwards(self):
        self.arms_solution += [
                self.left.move(State.BACK),
                self.left.rotate(State.CLOCKWISE),
                self.left.move(State.FORWARD),

                self.up.move(State.BACK, False, False),
                self.down.move(State.BACK),

                self.right.rotate(State.CLOCKWISE, False, False),
                self.left.rotate(State.ANTICLOCKWISE),

                self.up.move(State.FORWARD, False, False),
                self.down.move(State.FORWARD),

                self.right.move(State.BACK),
                self.right.rotate(State.ANTICLOCKWISE),
                self.right.move(State.FORWARD)
            ]

    def rotate_front(self, turns, way):
        self.rotate_cube_towards_right()
        self.rotate_left(turns, way)

    def rotate_back(self, turns, way):
        self.rotate_cube_towards_right()
        self.rotate_right(turns, way)

    def solution(self, rubik_solution):
        index = 0
        length = len(rubik_solution)

        while index < length:
            move = rubik_solution[index]
            self.rotate(move)

            if 'F' in move or 'B' in move:
                new_faces = {
                    'F': 'L',
                    'R': 'F',
                    'B': 'R',
                    'L': 'B'
                }
                for i in range(index, length):
                    if rubik_solution[i][0] in new_faces.keys():
                        face = new_faces[rubik_solution[i][0]]
                        if len(rubik_solution[i]) == 2:
                            face += rubik_solution[i][1]
                        rubik_solution[i] = face
            index += 1

    def append_command(self, command):
        self.arms_solution.append(command)


if __name__ == "__main__":
    arms = [
        Arm(1, 2, 20, 110, 10, 100, 20, 10, 0.004, 0.05),
        Arm(3, 4, 21, 117, 14, 120, 21, 14, 0.004, 0.05),
        Arm(5, 6, 22, 114, 15, 130, 22, 15, 0.004, 0.05),
        Arm(7, 8, 23, 111, 16, 124, 23, 16, 0.004, 0.05)
    ]

    generator = ArmSolutionGenerator(*arms)

    generator.solution(['F', 'U', 'B\'', 'U2'])

    for step in generator.arms_solution:
        if step:
            print(step)