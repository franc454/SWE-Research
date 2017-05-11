#include "Logger.h"

Logger logger;

////////////////////////////
// USER-ENTERED VARIABLES //
////////////////////////////
char* dataLoggerName = "SC 01";
char* fileName = "SC01.txt"; // Name of file for logged data: 8.3 format (e.g, 
                             // ABCDEFGH.TXT); <= 8 chars before ".txt" is OK

//Setup logging interval here, may setup more than one variable. 
//Minimum interval = 1 sec, maximum interval is 1 second short of 7 days.  
int Log_Interval_Seconds = 30; //Valid range is 0-59 seconds
int Log_Interval_Minutes = 0; //Valid range is 0-59 minutes
int Log_Interval_Hours = 0; //Valid range is 0-23 hours
int Log_Interval_Days = 0; //Valid range is 0-6 days
bool external_interrupt = false; // e.g., rain gage

void setup(){
logger.initialize(dataLoggerName, fileName, Log_Interval_Days, Log_Interval_Hours, Log_Interval_Minutes, Log_Interval_Seconds, external_interrupt);
logger.setupLogger();
}

void loop(){
// ***************************************** 
logger.sleep(); // Send logger to sleep
logger.startLogging();  // Wake up and initialize
// ****** DO NOT EDIT ABOVE THIS LINE ****** 

//////////////////////////////////
// READ SENSORS: EDIT THIS PART //
//////////////////////////////////

logger.UltimateGPS();

// ****** DO NOT EDIT BELOW THIS LINE ****** 

// Wrap up files, turn off SD card, and go back to sleep
logger.endLogging();

// ***************************************** 

}
