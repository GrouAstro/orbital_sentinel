import time
import subprocess

from tracker.robot_structs.tracker import Tracker


def main():
    file = "rfence/mimo/tracker_config.toml"
    space_sen = Tracker(file)
    angle_tar = 180
    step_angle = 5
    nb_stp = int(angle_tar / step_angle)

    sh_file = 'rfence/mimo/acq_mimo.sh'
    argument_script_sh = '0'

    subprocess.call(['bash', sh_file, argument_script_sh])

    for i in range(nb_stp):
        space_sen.azi_rotate(step_angle)
        argument = str(i * step_angle + step_angle)
        print('Angle : ', i * step_angle)
        subprocess.call(['bash', sh_file, argument])
        time.sleep(3)

    print('Acq stop')
    space_sen.azi_rotate(-angle_tar)


if __name__ == '__main__':
    main()
