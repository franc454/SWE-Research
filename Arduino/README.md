# Using Arduino for Ultimate GPS readings

The Ultimate GPS provides a library of files to receive data.  Echo is a file that takes these data and sends them to the Serial Monitor.  These data contains time, elevation angle, azimuth, signal strength, etc.  Using a serial port monitor called 'RS232 Data Logger' from Eltima, I was able to save the output from the Ultimate GPS into .txt files.  Examples of these files are in the plot_LWC folder under the names hour_test_1.txt and hour_test_2.txt.  echo_with_signal_strength is a file that I have edited from the Ultimate GPS Library to provide the correct data needed for determining the liquid water content of a snowpack.



*Reading data in .txt file*

The important information in the output for calculating the liquid water content is located within the $GPGGA and $GPGSV lines.
From 'Datasheet for the PA6H (MTK3339) GPS module' which can be found at https://learn.adafruit.com/adafruit-ultimate-gps/downloads.

## $GPGGA

$GPGGA contains time which is important for determining varying liquid water content during a long period of time.  Additionally, GPS location is provided and can be used to determine the location of a satellite relative to the Ultimate GPS.  I used this line for time in the plot_LWC.py code but for actual field research, the $GPRMC line may be better suited because it also provides the date.

<img align="center" width="500" height="500" src="/images//gga.jpg">


## GPRMC

$GPRMC provides date, time and location.  This line might be better suited for long data collection periods because it provides the date as well, which is not provided with $GPGGA.

<img align="center" width="500" height="500" src="/images//rmc.jpg">


## $GPGSV

$GPGSV provides the elevation angle, azimuth and C/N0 values received by the Ultimate GPS from a given satellite.  At one time, the Ultimate GPS can be receiving data from a number of satellites.  C/N0 values are later converted to SNR values in the plot_LWC.py file.  C/N0 is given in dB-Hz and the equations used in 'Measuring Snow Liquid Water Content with Low-Cost GPS Receivers' by Koch et al. 2014 calculate liquic water content with SNR, which has units of dB.  

Converting C/N0 to SNR:
  Reciever frequency = 1575.42MHz.  
  Bandwidth = 10 * log(1575.42 * 1,000,000) = 91.973963545486232243880870991767 dB.
  SNR = C/N0 - BW = C/N0 - 91.973963545486232243880870991767.
  
Additionally, elevation angle of the wave being received by the Ultimate GPS is important to the equations in Koch et al. 2014.  Azimuths are important for understanding the behavior of each satellite that is used in order to normalize the C/N0 values.  Normalizing C/N0 values is important for calculating liquid water content (Refer to Section 3.2 in 'Measuring Snow Liquid Water Content with Low-Cost GPS Receivers' by Koch et al. 2014).  Unfortunately, I didn't have the ability to normalize the C/N0 values and thus, plot_LWC doesn't plot the correct liquid water content values.
  
<img align="center" width="500" height="500" src="/images//gsv.jpg">
