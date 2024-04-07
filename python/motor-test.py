from gpiozero import OutputDevice, InputDevice
from time import sleep


devices = [OutputDevice(14),  # red   (1st coil, +)
           OutputDevice(15),  # blue  (1st coil, -)
           OutputDevice(18),  # green (2nd coil, +)
           OutputDevice(23)]  # black (2nd coil, -)

sleep_time = 0.005

current_phase = 0



phases = [[1, 0, 0, 0],
          [0, 0, 1, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 1]]


def update_output(phase):
    print(f"   phase {phase}: {phases[phase]}")
    for i in range(4):
        if devices[i].value != phases[phase][i]:
            devices[i].toggle()

def forward(steps):
    global current_phase 
    for i in range(steps):
        print(f"step {i}:")
        current_phase = (current_phase + 1) % 4;
        update_output(current_phase)   
        sleep(sleep_time)

def init():
    print("init")
    for i in range(4):
        devices[i].off()


init()
# 200 steps for the motor
# 1:51 gears
forward(100)