#!/bin/sh

FILE_NAME=$1
PATH_FILE="/home/radar/acq/"$FILE_NAME
echo $FILE_NAME
TIME=5		# Time in seconds
FREQ="897.5M"		# Frequency in Hertz (M = Mega = 1e6)
SAMP_RATE="40M"
BAND="40M"

TIMESSS=$TIME's'

# ======================================================================


bladeRF-cli -p 1>/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "No bladeRF devices connected." >&2
    exit 1
fi


bladeRF-cli -e "rx config file=$PATH_FILE format=bin n=262144 channel=1,2; set frequency rx $FREQ; set samplerate rx $SAMP_RATE; set bandwidth rx $BAND; set agc off; set gain rx1 35; set gain rx2 35 ; rx start; rx; rx wait '$TIME's; exit"

#bladeRF-cli -e "rx config file=$PATH_FILE format=bin n=131072 channel=1,2; set frequency rx $FREQ; set samplerate rx $SAMP_RATE; set bandwidth rx $BAND; set agc on ; rx start; rx; rx wait '$TIME's"