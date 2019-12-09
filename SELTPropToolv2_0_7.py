# -----------------------------------------------------------------------------
# Name:        SELT Tool
# Version: 	   2.0.7
# Purpose:     Analyzes parcels for SELT conservation suitability.
# Author:      Christian Matthews, Rockingham Planning Commission
#              cmatthews@rpc-nh.org
# Last Updated: 03/25/2019
# -----------------------------------------------------------------------------
# Import System Libraries
import arcpy
import time
start_time = time.clock()
arcpy.env.overwriteOutput = True


# Variables to Modify
arcpy.env.workspace = arcpy.GetParameterAsText(0)
seltPropPath = arcpy.GetParameterAsText(1)
seltProp = arcpy.Describe(seltPropPath)
seltProp = seltProp.name
workPath = arcpy.GetParameterAsText(2)
bufDist = arcpy.GetParameterAsText(3)


# Setup
arcpy.CreateFileGDB_management(workPath + '\\', seltProp + '.gdb')
scratchGDB = workPath + '\\' + seltProp + '.gdb'
workFC = scratchGDB + '\\' + seltProp + '_Working'
arcpy.CopyFeatures_management(seltProp, workFC)
seltPropBuf = workFC + '_Buf'
arcpy.Buffer_analysis(seltProp, seltPropBuf, bufDist, 'FULL', 'ROUND')
arcpy.AddMessage('Completed Initial Setup: ' + str(round((time.clock() -
                 start_time)/60, 1)) + ' Minutes')


# Intersect
intersectList = ['Roads', 'Ponds', 'Streams',  'Watersheds',
                 'Wetlands', 'Prime_Wetlands', 'Floodplain',
                 'Favorable_Gravel_Well', 'Future_WS',
                 'High_Trans_Aquifer_2000_Less',
                 'High_Trans_Aquifer_2000_More',
                 'Groundwater_GA1', 'Groundwater_GA2', 'Groundwater_GAA',
                 'SW_Protection_Areas', 'High_Priority_WSLs', 'WSIPA', 'WHPA',
                 'Hydrologic_AOC', 'Pollutant_Attenuation', 'Flood_Storage',
                 'Public_Water_Supply_FAs', 'Conservation_Priorities',
                 'Climate_Resilience', 'NEC_Ranked', 'NEC_Focus',
                 'Proactive_FA_SELT', 'SELT_Drinking_Water_FA',
                 'Active_Farmland', 'Non_Consv_Ag', 'Blanding_Land', 'IBA',
                 'WAPTIERS', 'Unfragmented_Forests', 'Coastal_Plan_Focus',
                 'MVRCP', 'Food_Deserts', 'MMRGCFA', 'CtC_Corridor', 'CtC_FA', 'GreatThicket', 'BarringtonNRA', 'DES_OutstResourceWS',]
intersectbufList = ['Lamprey_Wild_Scenic', 'NHB']
for fc in intersectList:
    intersectPath = scratchGDB+'\\'+seltProp+'_Intersect_'+fc
    arcpy.Intersect_analysis([seltProp, fc], intersectPath)
for fc in intersectbufList:
    intersectPath = seltPropBuf+'_Intersect_'+fc
    arcpy.Intersect_analysis([seltPropBuf, fc], intersectPath)
arcpy.AddMessage('Intersected Features: ' + str(round((time.clock() -
                 start_time)/60, 1)) + ' Minutes')


# Add Fields
addFields = [['Road_Frontage', 'DOUBLE', 'Road on Property (Feet)'],
             ['Street_Name', 'TEXT', 'Street Name'],
             ['LC_LEGEND', 'TEXT', 'Road Type'],
             ['LEGIS_CLAS', 'TEXT', 'Road Class'],
             ['Pond_Acres', 'DOUBLE', 'Pond on Property (Acres)'],
             ['Pond_OnSize', 'TEXT', 'Size of Pond (Acres)'],
             ['Pond_Dir', 'TEXT', 'Pond Direction'],
             ['Pond_Dist', 'DOUBLE', 'Pond Distance (Feet)'],
             ['Pond_NearSize', 'DOUBLE', 'Near Pond Size (Acres)'],
             ['Stream_Length', 'DOUBLE', 'Stream Length (Feet)'],
             ['Stream_Name', 'TEXT', 'Stream Name'],
             ['Lamprey_Wild_Scenic', 'TEXT', 'Lamprey Wild & Scenic Overlap'],
             ['Catchment_Area', 'TEXT', 'Catchment Area'],
             ['Wetlands_Acres', 'DOUBLE', 'Wetlands (Acres)'],
             ['Prime_Wetlands_Acres', 'DOUBLE',
              'Prime Wetland on Property (Acres)'],
             ['Prime_Wetlands_OnSize', 'TEXT',
              'Size of Prime Wetland (Acres)'],
             ['Prime_Wetlands_Dir', 'TEXT', 'Prime Wetlands Direction'],
             ['Prime_Wetlands_Dist', 'DOUBLE',
              'Prime Wetlands Distance (Feet)'],
             ['Prime_Wetlands_NearSize', 'DOUBLE',
              'Near Prime Wetlands Size (Acres)'],
             ['Floodplain_Acres', 'DOUBLE', 'Floodplain (Acres)'],
             ['Favorable_Gravel_Well_Acres', 'DOUBLE',
              'DES Favorable Gravel Well (Acres)'],
             ['Future_WS_Acres', 'DOUBLE', 'DES Future Water Supply (Acres)'],
             ['High_Trans_Aquifer_Less_2000_Acres', 'DOUBLE',
              'High Transmissivity Aquifers <=2,000 (Acres)'],
             ['High_Trans_Aquifer_More_2000_Acres', 'DOUBLE',
              'High Transmissivity Aquifers >2,000 (Acres)'],
             ['Groundwater_GA1_Acres', 'DOUBLE', 'Groundwater GA1 (Acres)'],
             ['Groundwater_GA2_Acres', 'DOUBLE', 'Groundwater GA2 (Acres)'],
             ['Groundwater_GAA_Acres', 'DOUBLE', 'Groundwater GAA (Acres)'],
             ['SW_Protection_Areas', 'TEXT', 'Source Water Protection Area'],
			 ['SW_Protection_Areas_Acres', 'DOUBLE', 'SWPA (Acres)'],
             ['High_Priority_WSLs_Acres', 'DOUBLE',
              'High Priority WSLs (Acres)'],
             ['WSIPA_Acres', 'DOUBLE',
              'Water Supply Intake Protection Areas (Acres)'],
             ['WSIPA_Name', 'TEXT',
              'Water Supply Intake Protection Areas Name'],
             ['WHPA_Acres', 'DOUBLE', 'WHPA (Acres)'],
             ['WHPA_Name', 'TEXT', 'WHPA Name'],
			 ['Hydrologic_AOC_Acres', 'DOUBLE', 'Hydrologic AOC (Acres)'],
             ['Hydrologic_AOC', 'TEXT', 'Hydrologic AOC'],
             ['Pollutant_Attenuation_Acres', 'DOUBLE',
              'Pollutant Attenuation (Acres)'],
             ['Pollutant_Attenuation_Tier', 'TEXT',
              'Pollutant Attenuation Tier'],
             ['Flood_Storage_Acres', 'DOUBLE',
              'Flood Storage (Acres)'],
             ['Flood_Storage_Tier', 'TEXT',
              'Flood Storage Tier'],
             ['Public_Water_Supply_FAs_Acres', 'DOUBLE',
              'Public Water Supply (Acres)'],
             ['Public_Water_Supply_FAs_Name', 'TEXT',
              'Public Water Supply Tier'],
             ['Conservation_Priorities_Acres', 'DOUBLE',
              'Rochester Conservation Priorities (Acres)'],
             ['Conservation_Priorities_Priority', 'TEXT',
              'Rochester Conservation Priority'],
             ['Climate_Resilience', 'TEXT', 'Climate Resilience Score'],
			 ['Climate_Resilience_Av', 'DOUBLE','CR Average (Acres)'],
			 ['Climate_Resilience_SAA', 'DOUBLE','CR SA Average (Acres)'],
			 ['Climate_Resilience_AA', 'DOUBLE','CR A Average (Acres)'],
			 ['Climate_Resilience_FAA', 'DOUBLE','CR Far A Average (Acres)'],
             ['NEC_Ranked_Acres', 'DOUBLE', 'NEC Ranked (Acres)'],
             ['NEC_Focus_Acres', 'DOUBLE', 'NEC Focus (Acres)'],
             ['Proactive_FA_SELT_Acres', 'DOUBLE',
              'Proactive FA SELT (Acres)'],
             ['SELT_Drinking_Water_FA_Acres', 'DOUBLE',
              'SELT Drinking Water FA (Acres)'],
             ['Active_Farmland_Acres', 'DOUBLE', 'Active Farmland (Acres)'],
             ['Non_Consv_Ag_Acres', 'DOUBLE', 'Non Consv Ag (Acres)'],
             ['Blanding_Land_Acres', 'DOUBLE',
              'Blandings Turtle Conservation Area (Acres)'],
             ['Blanding_Land_Tier', 'TEXT',
              'Blandings Turtle Conservation Area Tier'],
             ['Reptiles_E', 'DOUBLE', 'Endangered Reptiles'],
             ['Reptiles_T', 'DOUBLE', 'Threatened Reptiles'],
             ['Reptiles_SC', 'DOUBLE', 'Special Concern Reptiles'],
             ['Birds_E', 'DOUBLE', 'Endangered Birds'],
             ['Birds_T', 'DOUBLE', 'Threatened Birds'],
             ['Birds_SC', 'DOUBLE', 'Special Concern Birds'],
             ['Fish_E', 'DOUBLE', 'Endangered Fish'],
             ['Fish_T', 'DOUBLE', 'Threatened Fish'],
             ['Fish_SC', 'DOUBLE', 'Special Concern Fish'],
             ['Insects_E', 'DOUBLE', 'Endangered Insects'],
             ['Insects_T', 'DOUBLE', 'Threatened Insects'],
             ['Insects_SC', 'DOUBLE', 'Special Concern Insects'],
             ['Plants_E', 'DOUBLE', 'Endangered Plants'],
             ['Plants_T', 'DOUBLE', 'Threatened Plants'],
             ['Plants_SC', 'DOUBLE', 'Special Concern Plants'],
             ['Plants_Com', 'DOUBLE', 'Plant Communities'],
             ['IBA_Acres', 'DOUBLE', 'IBA (Acres)'],
             ['IBA_NAME', 'TEXT', 'IBA Name'],
             ['WAPTIERS_NH', 'DOUBLE', 'WAP Tier 1 (Acres)'],
             ['WAPTIERS_BR', 'DOUBLE', 'WAP Tier 2 (Acres)'],
             ['WAPTIERS_SL', 'DOUBLE', 'WAP Tier 3 (Acres)'],
             ['Unfragmented_Forests_Acres', 'DOUBLE',
              'Unfragmented Forests (Acres)'],
             ['Unfragmented_Forests_OnSize', 'TEXT',
              'Size of Unfragmented Forest Block (Acres)'],
             ['Coastal_Plan_Focus_Core_Acres', 'DOUBLE',
              'Coastal Plan Focus Core (Acres)'],
             ['Coastal_Plan_Focus_Core_Name', 'TEXT',
              'Coastal Plan Focus Core Name'],
             ['Coastal_Plan_Focus_Landscape_Acres', 'DOUBLE',
              'Coastal Plan Focus Landscape (Acres)'],
             ['Coastal_Plan_Focus_Landscape_Name', 'TEXT',
              'Coastal Plan Focus Landscape Name'],
             ['MVRCP_Acres', 'DOUBLE', 'MVRCP (Acres)'],
             ['MVRCP_Level', 'TEXT', 'MVRCP Level'],
             ['Food_Deserts_Acres', 'DOUBLE', 'Food Desert (Acres)'],
             ['MMRGCFA_Acres', 'DOUBLE',
              'MMRG Conservation Focus Areas (Acres)'],
			 ['MMRGCFA_Tier', 'TEXT',
              'MMRG Conservation Focus Tier'], 
             ['CtC_Corridor', 'DOUBLE', 'CtC Corridor (Acres)'],
             ['CtC_FA_Acres', 'DOUBLE', 'CtC Focus Area (Acres)'],
             ['CtC_FA_Name', 'TEXT', 'CtC Focus Area Name'],
			 ['GreatThicket_Acres', 'DOUBLE', 'Great Thicket (Acres)' ],
			 ['GreatThicket_Name', 'TEXT', 'Great Thicket Name'],
			 ['BarringtonNRA_Acres', 'DOUBLE', 'Barrington NRA (Acres)'],
			 ['BarringtonNRA_Name', 'TEXT', 'BarringtonNRA Name'],
			 ['DES_ORWS', 'DOUBLE', 'Outst Resource WS (Acres)']]
for field in addFields:
    arcpy.AddField_management(workFC, field[0], field[1], '', '', '', field[2])
arcpy.AddMessage('Added Fields: ' + str(round((time.clock()-start_time)/60, 1))
                 + ' Minutes')


# Area/Length
fcList = [['Roads', 'Shape_Length', 'Road_Frontage'],
          ['Ponds', 'Shape_Area', 'Pond_Acres'],
          ['Streams', 'Shape_Length', 'Stream_Length'],
          ['Wetlands', 'Shape_Area', 'Wetlands_Acres'],
          ['Prime_Wetlands', 'Shape_Area', 'Prime_Wetlands_Acres'],
          ['Floodplain', 'Shape_Area', 'Floodplain_Acres'],
          ['Favorable_Gravel_Well', 'Shape_Area',
           'Favorable_Gravel_Well_Acres'],
          ['Future_WS', 'Shape_Area', 'Future_WS_Acres'],
          ['High_Trans_Aquifer_2000_Less', 'Shape_Area',
           'High_Trans_Aquifer_Less_2000_Acres'],
          ['High_Trans_Aquifer_2000_More', 'Shape_Area',
           'High_Trans_Aquifer_More_2000_Acres'],
          ['Groundwater_GA1', 'Shape_Area', 'Groundwater_GA1_Acres'],
          ['Groundwater_GA2', 'Shape_Area', 'Groundwater_GA2_Acres'],
          ['Groundwater_GAA', 'Shape_Area', 'Groundwater_GAA_Acres'],
		  ['SW_Protection_Areas', 'Shape_Area', 'SW_Protection_Areas_Acres'],
          ['High_Priority_WSLs', 'Shape_Area', 'High_Priority_WSLs_Acres'],
          ['WSIPA', 'Shape_Area', 'WSIPA_Acres'],
          ['WHPA', 'Shape_Area', 'WHPA_Acres'],
		  ['Hydrologic_AOC', 'Shape_Area', 'Hydrologic_AOC_Acres'],
          ['Pollutant_Attenuation', 'Shape_Area',
           'Pollutant_Attenuation_Acres'],
          ['Flood_Storage', 'Shape_Area',
           'Flood_Storage_Acres'],
          ['Public_Water_Supply_FAs', 'Shape_Area',
           'Public_Water_Supply_FAs_Acres'],
          ['Conservation_Priorities', 'Shape_Area',
           'Conservation_Priorities_Acres'],
          ['NEC_Ranked', 'Shape_Area', 'NEC_Ranked_Acres'],
          ['NEC_Focus', 'Shape_Area', 'NEC_Focus_Acres'],
          ['Proactive_FA_SELT', 'Shape_Area', 'Proactive_FA_SELT_Acres'],
          ['SELT_Drinking_Water_FA', 'Shape_Area',
           'SELT_Drinking_Water_FA_Acres'],
          ['Active_Farmland', 'Shape_Area', 'Active_Farmland_Acres'],
          ['Non_Consv_Ag', 'Shape_Area', 'Non_Consv_Ag_Acres'],
          ['Blanding_Land', 'Shape_Area', 'Blanding_Land_Acres'],
          ['IBA', 'Shape_Area', 'IBA_Acres'],
          ['Unfragmented_Forests', 'Shape_Area', 'Unfragmented_Forests_Acres'],
          ['Coastal_Plan_Focus', 'Shape_Area',
           'Coastal_Plan_Focus_Core_Acres'],
          ['Coastal_Plan_Focus', 'Shape_Area',
           'Coastal_Plan_Focus_Landscape_Acres'],
          ['MVRCP', 'Shape_Area', 'MVRCP_Acres'],
          ['Food_Deserts', 'Shape_Area', 'Food_Deserts_Acres'],
          ['MMRGCFA', 'Shape_Area', 'MMRGCFA_Acres'],
          ['CtC_Corridor', 'Shape_Area', 'CtC_Corridor'],
          ['CtC_FA', 'Shape_Area', 'CtC_FA_Acres'],
		  ['GreatThicket', 'Shape_Area', 'GreatThicket_Acres'],
		  ['BarringtonNRA', 'Shape_Area', 'BarringtonNRA_Acres'],
		  ['DES_OutstResourceWS', 'Shape_Area' 'DES_ORWS']]
for fc in fcList:
    result = arcpy.GetCount_management(scratchGDB + '\\' + seltProp +
                                       '_Intersect_'+fc[0])
    count = int(result.getOutput(0))
    if int(count) == 1:
        sumTotal = 0
        with arcpy.da.SearchCursor(scratchGDB + '\\' + seltProp +
                                   '_Intersect_'+fc[0], fc[1]) as cursor:
            for row in cursor:
                sumTotal = sumTotal + row[0]
            if fc[1] == 'Shape_Area':
                sumTotal = round(sumTotal/43560, 2)
                arcpy.CalculateField_management(workFC, fc[2], "'" +
                                                str(sumTotal)+"'")
            else:
                arcpy.CalculateField_management(workFC, fc[2], "'" +
                                                str(sumTotal)+"'")
        del cursor, row
    if int(count) > 1:
        sumTotal = 0
        arcpy.Dissolve_management(scratchGDB + '\\' + seltProp +
                                  '_Intersect_' + fc[0], scratchGDB + '\\' +
                                  seltProp + '_Intersect_' + fc[0] +
                                  '_Dissolve', '', '', 'SINGLE_PART')
        if fc[1] == 'Shape_Area':
            with arcpy.da.SearchCursor(scratchGDB + '\\' +
                                       seltProp + '_Intersect_' + fc[0] +
                                       '_Dissolve', 'Shape_Area') as cursor:
                for row in cursor:
                    sumTotal = sumTotal + row[0]
                sumTotal = round(sumTotal/43560, 2)
                arcpy.CalculateField_management(workFC, fc[2], "'" +
                                                str(sumTotal)+"'")
        elif fc[1] == 'Shape_Length':
            with arcpy.da.SearchCursor(scratchGDB + '\\' +
                                       seltProp + '_Intersect_' + fc[0] +
                                       '_Dissolve', 'Shape_Length') as cursor:
                for row in cursor:
                    sumTotal = round(sumTotal + row[0], 2)
                arcpy.CalculateField_management(workFC, fc[2], "'" +
                                                str(sumTotal)+"'")
        del cursor, row


# Multiple Strings
fcList = [['Roads', 'STREET', 'Street_Name'],
          ['Roads', 'LC_LEGEND', 'LC_LEGEND'],
          ['Roads', 'LEGIS_CLAS', 'LEGIS_CLAS'],
          ['Streams', 'GNIS_Name', 'Stream_Name'],
          ['Ponds', 'Ponds_Acres', 'Pond_OnSize'],
          ['Watersheds', 'HU_12_NAME', 'Catchment_Area'],
          ['SW_Protection_Areas', 'NAME', 'SW_Protection_Areas'],
          ['WSIPA', 'NAME', 'WSIPA_Name'],
          ['WHPA', 'NAME', 'WHPA_Name'],
          ['Hydrologic_AOC', 'SYS_NAME', 'Hydrologic_AOC'],
          ['Pollutant_Attenuation', 'Polluntant_Tier',
           'Pollutant_Attenuation_Tier'],
          ['Flood_Storage', 'Flood_Tier', 'Flood_Storage_Tier'],
          ['Public_Water_Supply_FAs', 'PWS_Tier',
           'Public_Water_Supply_FAs_Name'],
          ['Conservation_Priorities', 'Priority',
           'Conservation_Priorities_Priority'],
          ['Climate_Resilience', 'Resilience_Category', 'Climate_Resilience'],
          ['Blanding_Land', 'tier', 'Blanding_Land_Tier'],
          ['IBA', 'Name', 'IBA_Name'],
          ['Unfragmented_Forests', 'TOTALACRES',
           'Unfragmented_Forests_OnSize'],
          ['MVRCP', 'Level', 'MVRCP_Level'],
          ['MMRGCFA', 'Tier', 'MMRGCFA_Tier'],
          ['Prime_Wetlands', 'Prime_Wetlands_Acres', 'Prime_Wetlands_OnSize'],
          ['CtC_FA', 'Name', 'CtC_FA_Name'],
		  ['GreatThicket', 'NAME', 'GreatThicket_Name'],
		  ['BarringtonNRA', 'Name', 'BarringtonNRA_Name']]
for fc in fcList:
    result = arcpy.GetCount_management(scratchGDB + '\\' + seltProp +
                                       '_Intersect_'+fc[0])
    count = int(result.getOutput(0))
    if int(count) > 0:
        fieldList = []
        with arcpy.da.SearchCursor(scratchGDB + '\\' + seltProp +
                                   '_Intersect_'+fc[0], fc[1]) as cursor:
            for row in cursor:
                if row[0] not in fieldList and row[0] is not None:
                    fieldList.append(str(row[0]))
        del cursor, row
        fieldString = ', '.join(fieldList)
        arcpy.CalculateField_management(workFC, fc[2], '"'+fieldString+'"')


# Nearest Feature
dirList = [['Ponds', 'Shape_Area', 'Pond_NearSize', 'Pond_Dir', 'Pond_Dist',
            'OBJECTID'],
           ['Prime_Wetlands', 'Shape_Area', 'Prime_Wetlands_NearSize',
            'Prime_Wetlands_Dir', 'Prime_Wetlands_Dist', 'OBJECTID']]
for fc in dirList:
    result = arcpy.GetCount_management(scratchGDB + '\\' + seltProp +
                                       '_Intersect_'+fc[0])
    count = int(result.getOutput(0))
    if int(count) == 0:
        arcpy.Near_analysis(workFC, fc[0], '', '', 'ANGLE')
        arcpy.CalculateField_management(workFC, fc[4], '!NEAR_DIST!')
        with arcpy.da.SearchCursor(workFC,
                                   ['NEAR_ANGLE', 'NEAR_FID']) as cursor:
            for row in cursor:
                if int(row[0]) == -180:
                    arcpy.CalculateField_management(workFC, fc[3], "'West'")
                elif int(row[0]) < -90:
                    arcpy.CalculateField_management(workFC, fc[3],
                                                    "'Southwest'")
                elif int(row[0]) == -90:
                    arcpy.CalculateField_management(workFC, fc[3], "'South'")
                elif int(row[0]) < -0:
                    arcpy.CalculateField_management(workFC, fc[3],
                                                    "'Southeast'")
                elif int(row[0]) == 0:
                    arcpy.CalculateField_management(workFC, fc[3], "'South'")
                elif int(row[0]) < 90:
                    arcpy.CalculateField_management(workFC, fc[3],
                                                    "'Northeast'")
                elif int(row[0]) == 90:
                    arcpy.CalculateField_management(workFC, fc[3], "'North'")
                elif int(row[0]) < 180:
                    arcpy.CalculateField_management(workFC, fc[3],
                                                    "'Northwest'")
                elif int(row[0]) == 180:
                    arcpy.CalculateField_management(workFC, fc[3], "'West'")
        nearID = 0
        nearID = nearID + row[1]
        del cursor, row
        with arcpy.da.SearchCursor(fc[0], [fc[1], fc[5]]) as cursor:
            for row in cursor:
                if nearID == row[1]:
                    arcpy.CalculateField_management(workFC, fc[2],
                                                    row[0]/43560)
        del cursor, row


# Yes or No
fcList = [['Lamprey_Wild_Scenic', 'Lamprey_Wild_Scenic']]
for fc in fcList:
    result = arcpy.GetCount_management(seltPropBuf+'_Intersect_'+fc[0])
    count = int(result.getOutput(0))
    if int(count) > 0:
        arcpy.CalculateField_management(workFC, fc[1], "'Yes'")
    else:
        arcpy.CalculateField_management(workFC, fc[1], "'No'")


# Specific Attribute
fcList = [['NUM', 'WAPTIERS', 'Shape_Area', 'WAPTIER', '1', 'WAPTIERS_NH'],
          ['NUM', 'WAPTIERS', 'Shape_Area', 'WAPTIER', '2', 'WAPTIERS_BR'],
          ['NUM', 'WAPTIERS', 'Shape_Area', 'WAPTIER', '3', 'WAPTIERS_SL'],
		  ['NUM', 'Climate_Resilience', 'Shape_Area', 'gridcode', '6', 'Climate_Resilience_Av'],
		  ['NUM', 'Climate_Resilience', 'Shape_Area', 'gridcode', '7', 'Climate_Resilience_SAA'],
		  ['NUM', 'Climate_Resilience', 'Shape_Area', 'gridcode', '8', 'Climate_Resilience_AA'],
		  ['NUM', 'Climate_Resilience', 'Shape_Area', 'gridcode', '9', 'Climate_Resilience_FAA'],
          ['NUMTEXT', 'Coastal_Plan_Focus', 'Shape_Area', 'TYPE', 'Core',
           'Coastal_Plan_Focus_Core_Acres'],
          ['NUMTEXT', 'Coastal_Plan_Focus', 'Shape_Area', 'TYPE',
           'Landscape', 'Coastal_Plan_Focus_Landscape_Acres'],
          ['TEXT', 'Coastal_Plan_Focus', 'NAME', 'TYPE', 'Core',
           'Coastal_Plan_Focus_Core_Name'],
          ['TEXT', 'Coastal_Plan_Focus', 'NAME', 'TYPE', 'Landscape',
           'Coastal_Plan_Focus_Landscape_Name']]
for fc in fcList:
    result = arcpy.GetCount_management(scratchGDB + '\\' + seltProp +
                                       '_Intersect_' + fc[1])
    count = int(result.getOutput(0))
    if int(count) > 0:
        fieldList = []
        if fc[0] == 'NUM':
            sumTotal = 0
            with arcpy.da.SearchCursor(scratchGDB + '\\' + seltProp +
                                       '_Intersect_' + fc[1],
                                       [fc[2], fc[3]]) as cursor:
                for row in cursor:
                    if int(row[1]) == int(fc[4]):
                        sumTotal = sumTotal + row[0]
                sumTotal = round(sumTotal/43560, 2)
                arcpy.CalculateField_management(workFC, fc[5], "'" +
                                                str(sumTotal)+"'")
            del cursor, row
        if fc[0] == 'NUMTEXT':
            sumTotal = 0
            with arcpy.da.SearchCursor(scratchGDB + '\\' + seltProp +
                                       '_Intersect_' + fc[1],
                                       [fc[2], fc[3]]) as cursor:
                for row in cursor:
                    if row[1] == fc[4]:
                        sumTotal = sumTotal + row[0]
                sumTotal = round(sumTotal/43560, 2)
                arcpy.CalculateField_management(workFC, fc[5], "'" +
                                                str(sumTotal) + "'")
            del cursor, row
        elif fc[0] == 'TEXT':
            with arcpy.da.SearchCursor(scratchGDB + '\\' + seltProp +
                                       '_Intersect_' + fc[1],
                                       [fc[2], fc[3]]) as cursor:
                for row in cursor:
                    if row[1] == fc[4]:
                        if row[0] not in fieldList and row[0] is not None:
                            fieldList.append(str(row[0]))
            del cursor, row
            fieldString = ', '.join(fieldList)
            arcpy.CalculateField_management(workFC, fc[5], '"'+fieldString+'"')
arcpy.AddMessage('Calculated Fields: ' + str(round((time.clock() - start_time)
                 / 60, 1)) + ' Minutes')


# NHB
arcpy.Statistics_analysis(seltPropBuf+'_Intersect_NHB',
                          seltPropBuf+'_Intersect_NHB_sum',
                          'OBJECTID COUNT', ['TYPE', 'STATELISTI'])
result = arcpy.GetCount_management(seltPropBuf+'_Intersect_NHB_sum')
count = int(result.getOutput(0))
if int(count) > 0:
    plantTotal = 0
    with arcpy.da.SearchCursor(seltPropBuf+'_Intersect_NHB_sum',
                               ['TYPE', 'FREQUENCY', 'STATELISTI']) as cursor:
        for row in cursor:
            if row[0] == 'Reptiles':
                if row[2] == 'E':
                    arcpy.CalculateField_management(workFC, 'Reptiles_E', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'T':
                    arcpy.CalculateField_management(workFC, 'Reptiles_T', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'SC':
                    arcpy.CalculateField_management(workFC, 'Reptiles_SC', "'"
                                                    + str(row[1]) + "'")
            elif row[0] == 'Fish':
                if row[2] == 'E':
                    arcpy.CalculateField_management(workFC, 'Fish_E', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'T':
                    arcpy.CalculateField_management(workFC, 'Fish_T', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'SC':
                    arcpy.CalculateField_management(workFC, 'Fish_SC', "'"
                                                    + str(row[1]) + "'")
            elif row[0] == 'Birds':
                if row[2] == 'E':
                    arcpy.CalculateField_management(workFC, 'Birds_E', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'T':
                    arcpy.CalculateField_management(workFC, 'Birds_T', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'SC':
                    arcpy.CalculateField_management(workFC, 'Birds_SC', "'"
                                                    + str(row[1]) + "'")
            elif row[0] == 'Insects':
                if row[2] == 'E':
                    arcpy.CalculateField_management(workFC, 'Insects_E', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'T':
                    arcpy.CalculateField_management(workFC, 'Insects_T', "'"
                                                    + str(row[1]) + "'")
                elif row[2] == 'SC':
                    arcpy.CalculateField_management(workFC, 'Insects_SC', "'"
                                                    + str(row[1]) + "'")
            elif row[0] in ('Plant species'):
                if row[2] == 'E':
                    plantTotal = plantTotal + row[1]
                    arcpy.CalculateField_management(workFC, 'Plants_E', "'"
                                                    + str(plantTotal)+"'")
                    plantTotal = 0
                elif row[2] == 'T':
                    plantTotal = plantTotal + row[1]
                    arcpy.CalculateField_management(workFC, 'Plants_T', "'"
                                                    + str(plantTotal) + "'")
                    plantTotal = 0
                elif row[2] == 'SC':
                    plantTotal = plantTotal + row[1]
                    arcpy.CalculateField_management(workFC, 'Plants_E', "'"
                                                    + str(plantTotal) + "'")
                    plantTotal = 0
            elif row[0] in ('Plant Community', 'Plant Community System'):
                plantTotal = plantTotal + row[1]
                arcpy.CalculateField_management(workFC, 'Plants_Com', "'"
                                                + str(plantTotal)+"'")
    del cursor, row
# Clean Up
dropFields = ['NEAR_FID', 'NEAR_DIST', 'NEAR_ANGLE']
arcpy.DeleteField_management(workFC, dropFields)
arcpy.TableToExcel_conversion(workFC, workPath + '\\' + seltProp +
                              '_Output.xlsx', 'ALIAS')
