# Using Arduino for Ultimate GPS readings

The Ultimate GPS provides a library of files to recieve data from the Ultimate GPS.  Echo is a file that takes this data and sends it to the Serial Monitor.  This data contains time, elevation angle, azimuth, signal strength, etc.  Using a serial port monitor called 'RS232 Data Logger' from Eltima, I was able to save the output from the Ultimate GPS into .txt files.  Examples of these files are in the plot_LWC folder under the names hour_test_1.txt and hour_test_2.txt.  



*Reading data in .txt file*

The important information in the output for calculating the liquid water content is located within the $GPGGA and $GPGSV lines.
From 'Datasheet for the PA6H (MTK3339) GPS module' which can be found at https://learn.adafruit.com/adafruit-ultimate-gps/downloads.

## $GPGGA

<img align="center" width="500" height="500" src="/images//gga.jpg">



## $GPGSV

<img align="center" width="500" height="500" src="/images//gsv.jpg">
