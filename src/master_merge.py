# Import libraries
import numpy as np
import pandas as pd
import os
import os.path
import datetime as dt
import argparse

# Print output to be displayed in terminal
print("***** ===== Copyright belongs to ducdh-dev ===== *****")
print("\nBegin merge script.\nScanning for files.\n\nImporting files:")

skiprows_input = input("Bạn muốn bỏ qua số dòng là (default=8): ")
skiprows = int(skiprows_input) if skiprows_input else 8

# Get all .xlsx files from project root recursively
targetF = []
errFiles = ""
validFiles = ""
validCnt = 0
errCnt = 0

for root, subdirs, files in os.walk(os.path.join(os.curdir, 'files')):
    for f in files:
        if f.endswith('.xlsx') and not (f == "master_table.xlsx" or f == "~$master_table.xlsx"):
            try:
                checkfile = open(os.path.join(root, f), encoding="utf-8")
                checkfile.close()
                validCnt += 1
                print("  " + os.path.join(root, f))
                validFiles += "  " + os.path.join(root, f) + "\n"
                targetF.append(os.path.join(root, f))
            except:
                errCnt += 1
                errFiles += "  " + os.path.join(root, f[2:]) + "\n"
                pass

# Output a log file from the merge process
if errCnt == 0:
    logMsg = "***** ===== Copyright belongs to ducdh-dev ===== *****\n\nProcess executed at: {}\n\nFiles imported:\n".format(str(dt.datetime.now()).split('.')[0]) + validFiles + "\nNumber of files imported = {}\n\nImport successful!".format(validCnt)
    log_file = open('log.txt', 'w', encoding="utf-8")
elif errCnt > 0:
    logMsg = "Process executed at: {}\n\nFiles imported:\n".format(str(dt.datetime.now()).split('.')[0]) + validFiles + "{} file(s) imported.\n\nWarning!!! Some files were in use during the time of import.".format(validCnt) \
    + "\nRun the script again in case there are changes from the affected files.\n\n{} file(s) affected:\n".format(errCnt) \
    + errFiles
    log_file = open('log.txt', 'w', encoding="utf-8")
    print("\n{} file(s) imported.\nWarning!!! {} file(s) in use during runtime:\n".format(validCnt, errCnt) + \
          errFiles + "There may have been changes to the affected files.")

logMsg += "\n\n***** ===== Copyright belongs to ducdh-dev ===== *****"
log_file.write(logMsg)
log_file.close()

# Load all .xlsx to dataframes and concatenate into master dataframe
dataframes = [pd.read_excel(t, skiprows=skiprows) for t in targetF]
df_master = pd.concat(dataframes)

# Exports a consolidated excel file 
if os.path.exists('master_table.xlsx'):
    try:
        mstFile = open('master_table.xlsx','r')
        mstFile.close()
        df_master.to_excel('master_table.xlsx', index = False)
        print("\nMerge complete!")
    except PermissionError:
        errMsg = "\nERROR!!! UPDATE FAILED! Please close the master_table.xlsx file and run the script again."
        print(errMsg)
        # open('log.txt', 'a').write(errMsg)   
        open('log.txt', 'w').write(errMsg)
else:
    df_master.to_excel('master_table.xlsx', index = False)
    print("Merge complete!")
