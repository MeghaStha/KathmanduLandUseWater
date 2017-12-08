# Author: Jeff Davids
# Modified: 
# Company: TU Delft
# Date: 161026
# Date Modified:
# Purpose: Merge multiple land use stats files into one flat file .csv
# v1.1
#
# Instructions: Fill in...
#
#   Import system modules
import os
import datetime

print ("Merging files, please wait...\n")

#   Modify the following three variables as desired
inputFilePath = r"G:\_GIS\2016MDP\LandUseStats\Stats"
outputFilePath = r"G:\_GIS\2016MDP\LandUseStats\Merged"
outputFileName = "Merged_LandUseStats_" + datetime.datetime.strftime(datetime.datetime.now(), '%Y%M%d%H%M%S') + ".csv"
try: 
    outFile = open(outputFilePath + '/' + outputFileName, 'w')
except OSError:
    input("Output file: '" + outputFileName + "' open. Please close the file and try again.")
    sys.exit()

#   Write headers to output file
outFile.write("siteID, devLow, devHigh, forestDecid, shrubland, rice, mixedPlanted, totalArea, %devLow, %devHigh, %forestDecid, %shrubland, %rice, %mixedPlanted, %totalArea\n")

dirList=os.listdir(inputFilePath)
for fName in dirList:
    if fName == outputFileName or fName.find("stats") == -1:
        continue
    inFile = open(inputFilePath + '/' + fName, 'r')
    print("Merging file " + fName + "; please wait.")

#   Create the siteID from the fName after removing stats
    siteID = fName.replace("stats","")
    
#   Write siteID to outFile
    outFile.write("%s," % (siteID))

#   Initialize areas to zero
    area1 = 0
    area2 = 0
    area3 = 0
    area4 = 0
    area5 = 0
    area6 = 0

#   Set iteration variables
    numIterations = 7
    i = 1

#   Read first line of data
    row = inFile.readline()

#   Check to make sure there is data in the row and limit to number of iterations    
    while i <= numIterations and len(row) > 0:

#   Set classID and area and remove carriage return from area
        dataFields = row.split(" ")
        classID = dataFields[0]
        area = round(float(dataFields[1].replace("\n","")),0)

#   Print data to user
        print("Class " + str(classID) + " had " + str(area) + " m^2 of area.")

#   Set areas depending on classID        
        if classID == "1":
            area1 = area
        elif classID == "2":
            area2 = area
        elif classID == "3":
            area3 = area
        elif classID == "4":
            area4 = area
        elif classID == "5":
            area5 = area
        elif classID == "6":
            area6 = area

#   Move to next iteration
        i += 1

#   Read next line of data
        row = inFile.readline()

#   Calculate total area for sub watershed
    areaTotal = area1 + area2 + area3 + area4 + area5 + area6
    percent1 = round(area1 / areaTotal * 100,4)
    percent2 = round(area2 / areaTotal * 100,4)
    percent3 = round(area3 / areaTotal * 100,4)
    percent4 = round(area4 / areaTotal * 100,4)
    percent5 = round(area5 / areaTotal * 100,4)
    percent6 = round(area6 / areaTotal * 100,4)
    percentTotal = round(percent1 + percent2 + percent3 + percent4 + percent5 + percent6,2)
        
#   Write data to outFile
    outFile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" 
        % (str(area1),str(area2),str(area3),str(area4),str(area5),str(area6),
        str(areaTotal),str(percent1),str(percent2),str(percent3),str(percent4),
        str(percent5),str(percent6),str(percentTotal)))

#   Clean up
    inFile.close()
outFile.close()
