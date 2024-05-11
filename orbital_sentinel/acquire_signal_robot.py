import time
import subprocess

from rfence.mimo.acquire_utils import rotate_acquire


def main():
    file = "rfence/mimo/tracker_config.toml"
    sh_file = 'rfence/mimo/acq_mimo.sh'
    lmt_angle = 90
    stp_amgle = 5
    symetric = 1

    rotate_acquire(lmt_angle, stp_amgle, symetric, file, sh_file)


if __name__ == '__main__':
    main()
