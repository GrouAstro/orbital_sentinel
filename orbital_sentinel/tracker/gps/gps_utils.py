import serial.tools.list_ports
import serial


def gps_device() -> serial:
    """Establish new connection to the gps device.
    Returns: Connection to the GPS module.
    """
    ports = list(serial.tools.list_ports.comports())
    # TODO improve this function to detect automatically GPS usb
    for p in ports:
        print(p)

    gps = serial.Serial(p.device)
    if gps.isOpen():
        gps.close()

    gps = serial.Serial(p.device, 4800, timeout=1)
    print('GPS connexion success ' + gps.name)

    return gps


def data_from_gps(gps_usb: serial, nmea: str) -> list[str]:
    """Load data from gps device and decode with your NMEA choice.
    Args:
        gps_usb: Gps port connexion.
        nmea: Gps frame to use.
    Returns:
    """
    data = list
    i = 0
    while i != 1:
        try:
            ser_bytes = gps_usb.readline()
            decoded_bytes = ser_bytes.decode("utf-8")
            data = decoded_bytes.split(",")
            if nmea == "$GPRMC":
                if data[0] == nmea and data[2] == 'A':
                    i = 1
                else:
                    print('No signal')

            if nmea == "$GGA":
                if data[0] == nmea and data[6] == '1':
                    i = 1
                else:
                    print('No signal')

        except UnicodeDecodeError:
            print('Invalid start byte')

    return data


def position(data: serial, nmea: str) -> dict:
    """Decode brut data and compute position from gps device. Gps module return data in arrays of strings by frame.
    Gps module return position in degrees minutes seconds, this function convert into decimal degrees format:
    One minute is equal to 1/60 degrees.
    One seconds is equal to 1/3600 degrees.
    Args:
        data: data from gps.
        nmea: gps frame to use.
    Returns:
        Position in sphere coordinates (Latitude, Longitude and in GGA case the altitude).
    """

    if nmea == '$GPRMC':
        # For GPRMC frame, latitude value is in 4th row.
        lat_nmea = data[3]
        # First and second values correspond to the first decimal part
        lat_deg = int(lat_nmea[:2])
        # Conversion degrees minutes into decimal degrees
        lat_mm = float(lat_nmea[2:4]) / 60
        # Conversion degrees seconds into decimal degrees
        lat_ss = float(lat_nmea[5:7]) / 3600
        # Add values from conversion
        lat_dec = lat_deg + lat_mm + lat_ss

        # For GPRMC frame, longitude value is in 5th row.
        long_nmea = data[5]
        # First to the third values correspond to the first decimal part
        long_deg = int(long_nmea[:3])
        # Conversion degrees minutes into decimal degrees
        long_mm = float(long_nmea[3:5]) / 60
        # Conversion degrees seconds into decimal degrees
        long_ss = float(long_nmea[6:8]) / 3600
        # Add values from conversion
        long_dec = long_deg + long_mm + long_ss

        alt = "N/A"

    elif nmea == '$GGA':

        # For GPGGA frame, latitude value is in 4th row.
        lat_nmea = data[2]
        # First and second values correspond to the first decimal part
        lat_deg = int(lat_nmea[:2])
        # Conversion degrees minutes into decimal degrees
        lat_mm = float(lat_nmea[2:4]) / 60
        # Conversion degrees seconds into decimal degrees
        lat_ss = float(lat_nmea[5:7] / 3600)
        # Add values from conversion
        lat_dec = lat_deg + lat_mm + lat_ss

        # For GPGGA frame, longitude value is in 4th row.
        long_nmea = data[4]
        # First to the third values correspond to the first decimal part
        long_deg = int(long_nmea[:3])
        # Conversion degrees minutes into decimal degrees
        long_mm = float(long_nmea[3:5]) / 60
        # Conversion degrees seconds into decimal degrees
        long_ss = float(long_nmea[6:8]) / 3600
        # Add values from conversion
        long_dec = long_deg + long_mm + long_ss

        alt = data[9]

    gps_ang = {"latitude": lat_dec, "longitude": long_dec, "altitude": alt}

    return gps_ang


def timestamp(data: serial, nmea: str) -> str:
    """ Decode timestamp from gps device.
    Gps module return data in arrays of strings by frame.
    Args:
        data: data from gps.
        nmea: nmea: gps frame to use.
    Returns:
    """
    if nmea == '$GPRMC':
        # For GPRMC frame, Time value is in second row.
        utc_nmea = data[1]
        utc_hh = utc_nmea[:2]
        utc_mm = utc_nmea[2:4]
        utc_ss = utc_nmea[4:6]

    elif nmea == '$GGA':
        utc_nmea = data[1]
        utc_hh = utc_nmea[:2]
        utc_mm = utc_nmea[2:4]
        utc_ss = utc_nmea[4:6]

    utc = {"time": utc_hh + ':' + utc_mm + ':' + utc_ss}

    return utc


def compute_data(nmea: str) -> dict:
    """Compute time and gps position.
    Args:
        nmea: gps frame to use.
    Returns: Position and time.
    """
    device = gps_device()
    data_device = data_from_gps(device, nmea)

    gps_features = {"position": position(data_device, nmea), "timestamp": timestamp(data_device, nmea)}

    return gps_features
