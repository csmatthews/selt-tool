# -----------------------------------------------------------------------------
# Name:        Geodatabase Cleanup Tool 
# Version: 	   2.0.0
# Purpose:     Cleans up null Feature Classes.
# Author:      Christian Matthews, Rockingham Planning Commission
#              cmatthews@rpc-nh.org
# Last Updated: 03/04/2019
# -----------------------------------------------------------------------------
# Import System Libraries
import arcpy
import time
start_time = time.clock()
print('Imported System Libraries: ' +
      str(round((time.clock()-start_time)/60, 1)) + ' Minutes')
arcpy.env.workspace = arcpy.GetParameterAsText(0)

# Delete Null Feature Classes
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    result = arcpy.GetCount_management(fc)
    count = int(result.getOutput(0))
    if int(count) == 0:
        arcpy.Delete_management(fc)
		