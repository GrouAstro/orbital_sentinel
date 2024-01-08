# import RPi.GPIO as gpio
import toml
import time


class Motor:
    """
    This class represents one motor of the tracker.
    """

    def __init__(self, config_file: dict, motor_type: str):
        """Initialize a new motor.
        Args:
            config_file: The global configuration for motorization.
            motor_type:  The angular type.
        """
        print('initialisation du moteur : ', motor_type)
        conf = toml.load(config_file)

        self.stp_pin = conf["motor"][motor_type]["stp"]
        self.dir_pin = conf["motor"][motor_type]["dir"]
        self.ena_pin = conf["motor"][motor_type]["ena"]
        self.end_pin = conf["motor"][motor_type]["end_stop"]

        self.driver_stp = conf["motor"][motor_type]["step"]
        self.ratio_eng = conf["motor"][motor_type]["eng_1"] / conf["motor"][motor_type]["eng_2"]

        self.delay = 0.0005
        self.speed = (self.driver_stp / self.ratio_eng) * (self.delay * 2)

        self.n_step = 0

        self.current_angle = 0.0
        self.state_motor = False

        # Configuration des broches GPIO
        # gpio.setmode(gpio.BCM)                # TODO uncomment
        # gpio.setup(self.stp_pin, gpio.OUT)    # TODO uncomment
        # gpio.setup(self.dir_pin, gpio.OUT)    # TODO uncomment
        # gpio.setup(self.ena_pin, gpio.OUT)    # TODO uncomment
        # gpio.setup(self.end_pin, gpio.IN)     # TODO uncomment

        # Désactivation du mode d'arrêt d'urgence (enable)
        # gpio.output(self.ena_pin, gpio.HIGH)  # TODO check this

    def one_step(self):
        """Move the stepper motor by one step.
        Returns:
            One step done.
        """
        # gpio.output(self.stp_pin, gpio.HIGH) # TODO uncomment
        time.sleep(self.delay)
        # gpio.output(self.stp_pin, gpio.LOW) # TODO uncomment
        time.sleep(self.delay)

    def direction(self, motor_dir: str):
        """Choose the motor direction.
        Args:
            motor_dir: Direction

        """

        if motor_dir == 'forward':
            md = 1  # TODO remove before push
            #gpio.output(self.dir_pin, gpio.HIGH)   # TODO uncomment

        elif motor_dir == 'backward':
            md = -1 # TODO remove before push
            # gpio.output(self.dir_pin, gpio.LOW)   # TODO uncomment

        else:
            print('Incorrect direction')

    def lock_motor(self, motor_ena: str):

        if motor_ena == 'lock':
            me = 1 # TODO remove before push
            # gpio.output(self.ena_pin, gpio.HIGH)  # TODO uncomment

        elif motor_ena == 'unlock':
            me = -1 # TODO remove before push
            # gpio.output(self.ena_pin, gpio.LOW)   # TODO uncomment

        else:
            print('Incorrect cannot un/lock the motor')

    def rotate(self, angle: float):
        """Do motor's rotation.

        Args:
            angle: The target angle.

        Returns:
            The real angle due to the motor step resolution and gear ratio.
        """
        if angle >= 0:
            self.direction('forward')
        else:
            self.direction('backward')

        # Calcul du nombre de step pour satisfaire l'angle
        deg_stp = (360 / self.driver_stp) * self.ratio_eng
        tgt_stp = angle / deg_stp
        int_tgt_stp = round(tgt_stp)

        # Rotation du moteur
        for i in range(int_tgt_stp):
            self.one_step()
            #print(i * (360 / self.driver_stp) * self.ratio_eng)

        self.current_angle = int_tgt_stp * deg_stp

        return self.current_angle

    def homing(self):
        """Rotate motor until it stops to the start position.

        Returns: The current angle is equal to 0.

        """
        state_end = 0

        if self.state_motor is False:
            # if gpio.input(self.end_pin) == gpio.LOW:  # TODO uncomment

            # gpio.output(self.dir_pin, gpio.HIGH)  # TODO check this
            sens = 1                                # TODO remove before push
            self.rotate(3)

            # gpio.output(self.dir_pin, gpio.LOW)   # TODO check this
            sens = -1                               # TODO remove before push

            # while gpio.input(self.end_pin) == gpio.LOW:   # TODO uncomment
            # while state_end == 0:                         # TODO uncomment
            #    self.one_step()                            # TODO uncomment

            self.current_angle = 0
            self.state_motor = 1

        else:
            print('Motor Already Initialize')

        return self.current_angle

    def position_ref(self):
        """Set the current angle as new referential

        Returns:

        """
        self.current_angle = 0.0
        return self.current_angle

    def set_speed(self, speed):
        """Set the motor's speed, you must respect the limitation.
        Args:
            speed: The speed in sec.rot⁻1.

        Returns: Delay for 1/2 step.

        """
        self.speed = speed
        full_step_sys = self.driver_stp / self.ratio_eng
        delay_time = round(speed / (2 * full_step_sys))
        if delay_time < 40:
            print('Speed too fast, please choose a lowest one')

        elif delay_time >= 40:
            print('Speed set to ', full_step_sys * (delay_time * 2), ' sec.rot')
            self.delay = delay_time

        return self.delay

    def get_speed(self):
        """Get motor speed.
        Returns: sec.rot⁻1 and delay for 1/2 step.

        """

        return self.speed, self.delay

    def get_ratio(self):
        """Get gear ratio.
        Returns: Gear_ratio_1 / Gear_ratio_2.

        """

        return self.ratio_eng