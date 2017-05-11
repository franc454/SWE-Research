# -*- coding: utf-8 -*-
"""
Run this file.

Takes a .txt file with GPS data and returns a plot of liquid water content of
a snowpack through time based on that GPS data.  Calls liquid_water_content.py 
to convert signal strength above and below the snowpack, snow depth, and elevation 
angle to a liquid water content value.  A PDF of the plot is also saved.
The liquid water content (LWC) values are averaged over a certain timestep.

Adjustable interval of time for averaging LWC values ('time_step') is on line 40.
To change files, change the name variable to your desired file's name.  The name
variable is on line 34.

The PDF of the plot will be saved under the same name as the text file being read
but with '_SWEplotted.pdf' added.  For example, reading a file 'hour_test_1.txt' 
will save a PDF titled 'hour_test_1_SWEplotted.pdf.'

Author: Keenen Francois-King
"""

#import modules.  liquid_water_content calculates the liquid water content (LWC) based
#on the snow depth, elevation angle of the received signal, and the signal strengths
#above and below the snow.
import liquid_water_content
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import defaultdict
import datetime as dt
from matplotlib.dates import DateFormatter

#Change this name to the name of the .txt file you want to read.  It will then 
#read the file and save the plots into a PDF of the same name
name = 'hour_test_2'

f = open(name + '.txt')
pdf = PdfPages(name + '_SWEplotted.pdf')

#adjust this to change how large of a timestep of SWE vals is averaged.
time_step = 1000 #[sec]

text = f.readlines()

#We don't have GPS readings above snowpack or snowpack depth.  Eventually we will 
#and can use the readings in the txt files from that GPS and the depth sensor to solve 
#for LWC. For now we will use the constants strength_above and snow_depth.
strength_above = 50 #signal strength at GPS above snowpack. Use C/N0 value [dBHz]
snow_depth = 1 #[m]
sat = []
sat_SNR = []
sat_LWC = []
sat_dict = defaultdict(list)
sat_dict_ave = defaultdict(list)
time = []
strength = []
angle = []


current_time = None
i = -1
z = 0
set_vals = False


for line in text:
    check_line = line.split(',')
    
    #$GPGGA gives the current timestamp and after it comes the $GPGSV which contains
    #the SNR value.  Store the timestamp as current_time so that SNR can later be 
    #plotted against time
    
    if check_line[0] == '$GPGGA':
        current_time = str(check_line[1])
    
    #append 2-item long lists containing time and SNR value to corresponding satellite's list
    elif check_line[0] == '$GPGSV':
        try:
            #The GPS recieves data at a frequency of 1575.42MHz.  We can convert 
            #the C/N0 value from the GPS which is in dB-Hz to an SNR value in dB 
            #which is used in calculating the SWE. Reciever frequency = 1575.42MHz.  
            #Bandwidth = 10*log(1575.42*1,000,000) = 91.973963545486232243880870991767 dB.
            #SNR = C/N0 - BW = C/N0 - 91.973963545486232243880870991767.  Also 
            #C/N0 values are recorded as positive but they are negative.
            sat_SNR.append([int((int(current_time[:2])*3600)+(int(current_time[2:4])*60)+\
                        (int(current_time[4:6]))), float((strength_above)-91.973963545486232243880870991767), \
                        float(float(check_line[7])-91.973963545486232243880870991767), snow_depth, float(check_line[5])])
        except (ValueError, IndexError):
            continue
    else:
        continue

#This function calls liquid_water_content.  This will convert the values of SNR to
#values of LWC.
def fx(x):
    all_converted = []
    for instance in list(map(lambda y: liquid_water_content.LWE(y).solve_equations(), x)):
        all_converted.append(instance)
    return all_converted  

#Call function above.  Convert SNR vals in sat_SNR to LWC values in sat_LWC
sat_LWC = fx(sat_SNR)

sat_data = []
prev = sat_LWC[0][0]
count = 0
total_count = 0
sihvola = 0
denoth = 0
roth = 0

#average LWC values for all repeated times so that way we have no repeats in time.
for i in sat_LWC:
    total_count += 1
    if i[0] == prev and total_count != len(sat_LWC):
        count += 1
        sihvola += i[1]
        denoth += i[2]
        roth += i[3]
    else:
        if count == 0:
            count += 1
        if total_count == len(sat_LWC):
            count += 1
            sihvola += i[1]
            denoth += i[2]
            roth += i[3]
        sat_data.append([prev, (sihvola/count), (denoth/count), (roth/count)])
        prev = i[0]
        count = 1
        sihvola = i[1]
        denoth = i[2]
        roth = i[3]

start = sat_data[0][0]
sat_data_ave = []
interval = 0
count = 0
total_count = 0
time_ave = 0
sihvola_ave = 0
denoth_ave = 0
roth_ave = 0

#Average SWE values for a certain timestep set above.  Time and all SWE values will 
#be averaged.
#If there is still time left in the interval we will enter the if statement.
#The time between the current data and previous is then taken from the interval.
#If the interval becomes greater than the timestep, we have reached the end
#of the timestep and will move on to the else statement, append the average
#and start a new interval.
for i in sat_data:

    if time_step > (interval + (i[0]-start)) and total_count != len(sat_data):
        interval += (i[0]-start)
        count += 1
        time_ave += i[0]
        sihvola_ave += i[1]
        denoth_ave += i[2]
        roth_ave += i[3]
        total_count += 1
    else:
        #two cases will result in an error if we don't do this step.  Those are
        #cases where we have a data point that is not within the time_step of
        #another point or when we are at the last data point.  We need to then
        #add the values for those cases.
        if count == 0 or total_count == len(sat_SNR):
            time_ave += i[0]
            sihvola_ave += i[1]
            denoth_ave += i[2]
            roth_ave += i[3]
            count += 1
        
        #average the values for time and LWC and append to new list
        sat_data_ave.append([int(time_ave/count), (sihvola_ave/count), \
                             (denoth_ave/count), (roth_ave/count)])
        total_count += 1
        #reset these values so we can start averaging a new interval of data points
        start = i[0]
        count = 1
        interval = 0
        time_ave = i[0]
        sihvola_ave = i[1]
        denoth_ave = i[2]
        roth_ave = i[3]

#separate data to make plotting and formatting easier
time = []
sihv = []
deno = []
roth = []
for x in sat_data_ave:
    time.append(str(int(x[0]/3600)) + ':' + str(int((float(x[0]/3600)-int(x[0]/3600))*60))\
                        + ':' + str(int(int((((float(x[0]/3600) - int(x[0]/3600))*60)-\
                        (int((float(x[0]/3600)-int(x[0]/3600))*60)))*60))))
    sihv.append(x[1])
    deno.append(x[2])
    roth.append(x[3])      

plottable_time = []
for x in time:
    time_plot = dt.datetime.strptime(x, '%H:%M:%S')
    plottable_time.append(time_plot)

#plot data
fig = plt.figure(figsize = (18,5))
ax = plt.subplot(111)
ax.set_title('Liquid Water Content (averaged at ' + str(time_step) + \
                        ' second intervals)', fontsize=15, fontweight='bold')
ax.set_ylabel('Liquid Water Content [%]')
ax.set_xlabel('UTC Time [HH:MM:SS]')
ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
ax.plot(plottable_time, sihv, 'ro', markersize=3, label = 'Sihvola')
ax.plot(plottable_time, deno, 'bo', markersize=3, label = 'Denoth')
ax.plot(plottable_time, roth, 'go', markersize=3, label = 'Roth')
ax.legend(loc = 'center left', bbox_to_anchor=(1, 0.5))
pdf.savefig()
plt.show()
pdf.close()
    