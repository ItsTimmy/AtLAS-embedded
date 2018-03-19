import serial
import threading
import time
from config import SERIAL_BAUD_RATE, SERIAL_PORT, THROTTLE_CHANNEL, PITCH_CHANNEL, YAW_CHANNEL, ROLL_CHANNEL, \
    UAV_CONTROL_UPDATE_PERIOD


MIN_DIR = 1000
MAX_DIR = 2000
DEFAULT_DIR = (MAX_DIR-MIN_DIR)/2 + MIN_DIR


class __UavControlThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.throttle = 1000
        self.pitch = 1500
        self.yaw = 1500
        self.roll = 1500
        self.serial_port = serial.Serial(SERIAL_PORT, baudrate=SERIAL_BAUD_RATE, write_timeout=0.01)
        self.running = True

    def run(self):
        while self.running:
            self.__send_control_signal()
            time.sleep(UAV_CONTROL_UPDATE_PERIOD)

    def __send_control_signal(self):
        # This snippet orders the signals so they match the order the arduino expects
        signals = [x for _, x in sorted(zip(
            [THROTTLE_CHANNEL, PITCH_CHANNEL, ROLL_CHANNEL, YAW_CHANNEL],
            [self.throttle, self.pitch, self.roll, self.yaw]
        ))]
        signal_bytes = []
        for sig in signals:
            signal_bytes.append((sig >> 8) & 255)
            signal_bytes.append(sig & 255)
        self.serial_port.write(bytes(signal_bytes))


__uavControlThread = __UavControlThread()
__uavControlThread.start()


def set_throttle(throttle):
    """
    Sets the throttle of the drone.
    :param throttle: A number between 0 and 1, where 0 is off, and 1 is full throttle
    :return: None
    :raise: ValueError is throttle is not between 0 and 1
    """
    if throttle < 0 or throttle > 1:
        raise ValueError("Throttle must be between 0 and 1, inclusive")
    __uavControlThread.throttle = int(throttle * (MAX_DIR - MIN_DIR) + MIN_DIR)


def set_pitch(pitch):
    """
    Sets the pitch of the drone.
    :param pitch: A number between -1 and 1, where 0 is neutral, 1 is full forward, and -1 is full backward
    :return: None
    :raise: ValueError if pitch is not between -1 and 1
    """
    if pitch < -1 or pitch > 1:
        raise ValueError("Pitch must be between -1 and 1, inclusive")
    __uavControlThread.pitch = int((pitch/2 + 0.5) * (MAX_DIR - MIN_DIR) + MIN_DIR)


def set_yaw(yaw):
    """
    Sets the yaw of the drone.
    :param yaw: A number between -1 and 1, where 0 is neutral, 1 is full right, and -1 is full left
    :return: None
    :raise: ValueError if yaw is not between -1 and 1
    """
    if yaw < -1 or yaw > 1:
        raise ValueError("yaw must be between -1 and 1, inclusive")
    __uavControlThread.yaw = int((yaw/2 + 0.5) * (MAX_DIR - MIN_DIR) + MIN_DIR)


def set_roll(roll):
    """
    Sets the roll of the drone.
    :param roll: A number between -1 and 1, where 0 is neutral, 1 is full right, and -1 is full left
    :return: None
    :raise: ValueError if roll is not between -1 and 1
    """
    if roll < -1 or roll > 1:
        raise ValueError("roll must be between -1 and 1, inclusive")
    __uavControlThread.roll = int((roll/2 + 0.5) * (MAX_DIR - MIN_DIR) + MIN_DIR)
