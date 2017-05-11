# Final-Project

plot_LWC takes a .txt file with GPS data and returns a plot of liquid water content of
a snowpack through time based on that GPS data.  A PDF of the plot is also saved.
The liquid water content (LWC) values are averaged over a certain timestep.

plot_LWC.py calls liquid_water_content.py to convert signal strength above and below the 
snowpack, snow depth, and elevation angle to a liquid water content value. Run plot_LWC.py.

Adjustable interval of time for averaging LWC values ('time_step') is on line 38.
To change files, change the 'name' variable to your desired file's name.  The 'name'
variable is on line 32.

The PDF of the plot will be saved under the same name as the text file being read
but with '_SWEplotted.pdf' added.  For example, reading a file 'hour_test_1.txt' 
will save a PDF titled 'hour_test_1_SWEplotted.pdf.'

C/N0 values collected from the GPS need to be converted to SNR.  They are converted in lines
85 and 86.  Though they are converted, they still need to be normalized to values on a snow
free day (Refer to Section 3.2 in 'Measuring Snow Liquid Water Content with Low-Cost GPS 
Receivers' by Koch et al. 2014).  Since the C/N0 values used in plot_LWC are not normalized 
and there are no values for the GPS above the snowpack, the output for liquid water content 
are not correct.  If we could go to the field and collect data, we could slightly adjust this 
project to normalize the C/N0 values and calculate the liquid water content accurately.  
Unfortunately, since I didn't have the ability to do this the liquid water content values plotted
are not correct.

Author: Keenen Francois-King
