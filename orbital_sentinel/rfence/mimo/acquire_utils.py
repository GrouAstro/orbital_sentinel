import time
import subprocess

from tracker.robot_structs.tracker import Tracker


def rotate_acquire(angle: int, step: int, mirror_mod: int, tracker_file, acq_file):
    """ Configure tracker to acquire signal with different angles.
        Need config_file to set up robot and sh file to use bladeRF
    Args:
        angle: Angle limit.
        step: Value between each angle value
        mirror_mod: 1 if you want the other side.
        tracker_file: Robot configuration
        acq_file: Automatic file to pilot bladeRF device.

    Returns: Acquire files.

    """

    robot = Tracker(tracker_file)

    n_step = int(angle / step)
    argument_script_sh = '0'
    print('Angle : ', argument_script_sh)
    subprocess.call(['bash', acq_file, argument_script_sh])

    for i in range(n_step):

        robot.azi_rotate(step)
        argument = str(i * step + step)
        print('Angle : ', argument)
        subprocess.call(['bash', acq_file, argument])
        time.sleep(1)

    robot.azi_rotate(-angle)

    if mirror_mod == 1:

        robot.azi_rotate(-step)
        argument_script_sh = '-' + str(step)
        print('Angle : ', argument_script_sh)
        subprocess.call(['bash', acq_file, argument_script_sh])

        for i in range(n_step-1):

            robot.azi_rotate(-step)
            argument = str(-(i+1) * step + int(argument_script_sh))
            print('Angle : ', argument)
            subprocess.call(['bash', acq_file, argument])
            time.sleep(1)

    else:
        print('Acq stop')
    print('Acq stop')
    robot.azi_rotate(angle)
