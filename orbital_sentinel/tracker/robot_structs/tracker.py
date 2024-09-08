from orbital_sentinel.tracker.robot_structs.motor import Motor
from orbital_sentinel.tracker.robot_structs.target import Orbital_target_natural
from orbital_sentinel.tracker.gps import compute_coordinate

from time import sleep


class Tracker:
    """
    This represents a tracker that contains motor
    """

    def __init__(self, config_file: str):

        print('Tracker initialize')

        self.motor_ele = Motor(config_file, motor_type="elevation")
        self.state_ang_ele = False
        self.ang_ele = 0

        self.motor_azi = Motor(config_file, motor_type="azimuth")
        self.state_ang_azi = False
        self.ang_azi = 0

        self.position_lon = 0
        self.position_lat = 0
        self.position_alt = 0

        self.target = 'None'

    def set_position(self, longitude, latitude, altitude):

        self.position_lon = longitude
        self.position_lat = latitude
        self.position_alt = altitude

    def ele_rotate(self, ang_ele: float):
        """Rotate around the elevation by adding angle value from the start position.

        Args:
            ang_ele: The elevation angle to reach by the motor.

        Returns:
            The angle value after rotation.
        """
        print('Rotation elevation == ', ang_ele)
        self.motor_ele.rotate(ang_ele)
        self.ang_ele = self.motor_ele.current_angle

    def azi_rotate(self, ang_azi: float):
        """Rotate around the azimuth by adding angle value from the start position.

        Args:
            ang_azi: The azimuth angle to reach by the motor.

        Returns:
            The angle value after rotation.
        """
        print('Rotation azimuth == ', ang_azi)
        self.motor_azi.rotate(ang_azi)
        self.ang_azi = self.motor_azi.current_angle

    def bi_rotate(self, ang_ele: float, ang_azi: float):
        """Rotate around the azimuth and elevation by adding angle values from the start positions.

        Args:
            ang_ele: The elevation angle to reach by the motor.
            ang_azi: The azimuth angle to reach by the motor.

        Returns:
            The angle values after rotations.
        """
        self.ele_rotate(ang_ele)
        self.azi_rotate(ang_azi)

    def ele_rotate_relative(self, ang_ele_ref: float):
        """Align the elevation angle with the target from a referential.

        Args:
            ang_ele_ref: Target angle value in elevation.

        """
        ang_ele_delta = ang_ele_ref - self.ang_ele

        self.ele_rotate(ang_ele_delta)

    def azi_rotate_relative(self, ang_azi_ref: float):
        """Align the azimuth angle with the target from a referential.

        Args:
            ang_azi_ref: Target angle value in azimuth.

        """
        ang_azi_delta = ang_azi_ref - self.ang_azi

        self.azi_rotate(ang_azi_delta)

    def bi_rotate_relative(self, ang_ele_ref: float, ang_azi_ref: float):
        """ Align the elevation and azimuth angles with the target from a referential.

        Args:
            ang_ele_ref: Target angle value in elevation.
            ang_azi_ref: Target angle value in azimuth.

        Returns:

        """
        ang_ele_delta = ang_ele_ref - self.ang_ele
        ang_azi_delta = ang_azi_ref - self.ang_azi

        self.bi_rotate(ang_ele_delta, ang_azi_delta)

    def get_angles(self):
        """ Get the angles value from initialize point.

        Returns:
            The azimuth value.
            The elevation value.
        """
        print(self.ang_ele, self.ang_azi)
        return

    def disp_angles(self):

        if self.state_ang_ele is True and self.state_ang_azi is True:

            print('Angle Azimuth : ', self.ang_azi,
                  'Angle Elevation : ', self.ang_ele)

        elif self.state_ang_ele is False and self.state_ang_azi is False:

            print('Angle Elevation : ', '?????', 'Angle Azimuth : ', '?????')
            print('Tracker is not initialize, You must use homing function or define your own position referential')

    def ele_home(self):
        """Initialize elevation motor only.

        """
        self.motor_ele.homing()
        self.state_ang_ele = True
        self.ang_ele = 0

    def azi_home(self):
        """Initialize azimuth motor only.

        """
        self.motor_azi.homing()
        self.state_ang_azi = True
        self.ang_azi = 0

    def bi_home(self):
        """Initialize both motor

        """
        self.ele_home()
        self.azi_home()

    def ele_ref(self):
        """Use current elevation value as new referential.

        """
        # self.ang_ele = self.motor_ele.position_ref()*
        self.ang_ele = 0
        self.state_ang_ele = True

    def azi_ref(self):
        """Use current azimuth value as new referential.

        """
        # self.ang_azi = self.motor_azi.position_ref()
        self.ang_azi = 0
        self.state_ang_azi = True

    def bi_ref(self):
        """Use current elevation and azimuth values as new referential.

        """
        self.ele_ref()
        self.azi_ref()

    def get_ele_speed(self):
        """

        Returns:

        """

        print(self.motor_ele.get_speed())

    def get_azi_speed(self):
        """

        Returns:

        """
        print(self.motor_azi.get_speed())

    def get_bi_speed(self):
        """

        Returns:

        """
        self.get_ele_speed()
        self.get_azi_speed()

    def get_ele_eng_ratio(self):
        """

        Returns:

        """
        print(self.motor_ele.get_ratio())

    def get_azi_eng_ratio(self):
        """

        Returns:

        """
        print(self.motor_azi.get_ratio())

    def get_bi_eng_ratio(self):
        """

        Returns:

        """
        self.get_ele_eng_ratio()
        self.get_azi_eng_ratio()

    def get_position(self):
        """

        Returns:

        """

        # if self.position_lon & self.position_lat == 0.0:
        #    print('Tracker not initialized')
        # else:
        print('Longitude : ', self.position_lon, ' | Latitude : ', self.position_lat)

    def set_position_auto(self):
        """

        Returns:

        """
        data = compute_coordinate('$GPRMC')
        self.position_lon = data['longitude']
        self.position_lat = data['latitude']

    def set_position_manual(self, lon_value: float, lat_value: float, alt_value: float):
        """

        Args:
            lon_value:
            lat_value:
            alt_value:

        Returns:

        """
        self.position_lon = lon_value
        self.position_lat = lat_value
        self.position_alt = alt_value

    def create_target(self, id_target: str):

        self.target = Orbital_target_natural(id_target)
        print('New target : ', id_target)

    def change_target(self, id_new_target: str):

        self.target.change_target(id_new_target)

    def point_target(self):
        """

        Returns:

        """

        print(self.get_angles())
        self.target.compute_position(self.position_lat,
                                     self.position_lon,
                                     self.position_alt)
        if self.target.visibility == 1:
            delta_a = self.target.azimuth
            delta_e = self.target.elevation

            self.bi_rotate_relative(delta_e, delta_a)
            print('Target Lock')

        elif self.target.visibility == 0:
            print('Target not available, abord pointing')

    def tracking_target(self):
        """

        Returns:

        """

        while True:

            try:
                self.point_target()
                sleep(0.05)

            except KeyboardInterrupt:
                print('Stop tracking mod')
                break

    def get_target_info(self):
        """

        Returns:

        """

        self.target.compute_position(self.position_lat,
                                     self.position_lon,
                                     self.position_alt)
        self.target.get_position()


