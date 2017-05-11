# Using Arduino for Ultimate GPS readings

The Ultimate GPS provides a library of files to receive data.  Echo is a file that takes these data and sends them to the Serial Monitor.  These data contains time, elevation angle, azimuth, signal strength, etc.  Using a serial port monitor called 'RS232 Data Logger' from Eltima, I was able to save the output from the Ultimate GPS into .txt files.  Examples of these files are in the plot_LWC folder under the names hour_test_1.txt and hour_test_2.txt.  echo_with_signal_strength is a file that I have edited from the Ultimate GPS Library to provide the correct data needed for determining the liquid water content of a snowpack.



*Reading data in .txt file*

The important information in the output for calculating the liquid water content is located within the $GPGGA and $GPGSV lines.
From 'Datasheet for the PA6H (MTK3339) GPS module' which can be found at https://learn.adafruit.com/adafruit-ultimate-gps/downloads.

## $GPGGA

<img align="center" width="500" height="500" src="/images//gga.jpg">

$GPGGA contains time and date which is important for determining varying liquid water content during a long period of time.  Additionally, lo

## $GPGSV

<img align="center" width="500" height="500" src="/images//gsv.jpg">
