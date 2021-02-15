import pandas as pd
import numpy as np

# Data frame for the list of all assessments that were valid for the program year.
assess = pd.read_excel("Assessments.xlsx", index_col=None) # Read excel file.
assess = assess.replace("\r","",regex=True) # Get rid of all extra \r.
assess = assess.replace("\n","",regex=True) # Get rid of all extra \n.
assess = assess.drop(assess.columns[[1,2,3,4,5,6,7,9,10,11,12,14,16,17,18,19,21,22,23,24,25,26,28,29]],axis=1) # Get rid of all empty, meaningless columns.
assess = assess.dropna(axis=0, how='all', thresh=None, subset=None) # Get rid of all rows that are entirely empty.
assess = assess.drop(assess[assess["Unnamed: 15"] == "Math"].index) # Delete rows with unrelated value.

assess['Unnamed: 6'] = np.where(assess['Unnamed: 15'] == "Reading", 1, 2) #Add column with code for Modality.
assess.drop(assess[assess['Unnamed: 0'] == "Student:"].index, inplace=True) # Delete extra headers in assessment list.
assess['Unnamed: 15'] = assess['Unnamed: 15'].fillna(method='ffill') # Fill empty cells underneath with Student ID to get rid of extra rows.
assess.drop(assess[assess["Unnamed: 8"] == "Student Assessments"].index, inplace=True) # Delete extra headers in assessment list.
assess.drop(assess[assess["Unnamed: 13"] == "Student ID: "].index, inplace=True) # Delete extra headers in assessment list.
assess['Unnamed: 7'] = np.where((assess['Unnamed: 15'] == "Reading") | (assess['Unnamed: 15'] == "Listening"), None, assess['Unnamed: 15']) # Moving Student ID to new column.
assess['Unnamed: 7'] = assess['Unnamed: 7'].fillna(method='ffill') # Fill empty cells underneath with Student ID.
assess.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True) # Get rid of all rows that are entirely empty.
assess.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=False) # Delete all duplicate rows
assess.columns = ["Date", "Form", "Module", "Modality", "Score", "Level","Modality ID", "Student ID"] # Create label set for data frame
assess.drop(labels="Modality", axis=1, columns=None, level=None, inplace=True, errors='raise') # Delete Modality column with strings.

# Preparing file for MySQL
assess["Date"] = pd.to_datetime(assess["Date"]) # Format dates to fit MySQL.
assess["Score"] = assess["Score"].astype(float) # Format scores as floats.

# Dataframe for the list of all the learners who were active during the program year.
hours = pd.read_csv("hours.csv", header=None) # Read csv file.
hours.drop(hours.columns[[0,1,2,3,4,5,6,7]],axis=1,inplace=True) # Delete unnecessary columns.
new_header = hours.iloc[0] # Create a new header
hours = hours[1:] # Create new data frame for new header
hours.columns = new_header # Attach new header to new df
hours.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=False) # Delete all duplicate rows
hours.to_csv('active_learners.csv', index=True, header=True, index_label=None) # Create csv file

# Merging both lists
complete_learners = assess.merge(hours, how='outer', on="Student ID")
complete_learners.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True) # Delete all rows of learners with no hours (blank cell).
complete_learners.drop(complete_learners[complete_learners["Current FY Instr Hrs"] == "0.00"].index, inplace=True) # Delete learners with 0 hours in the PY.
complete_learners["Level"].replace(to_replace="Completed ESL L6", value="7", inplace=True, limit=None, regex=False, method='pad') # Replacing the "Completed ESL L&" level value with "L7."
complete_learners["Level"].replace(to_replace="ESL L", value="", inplace=True, limit=None, regex=True, method='pad') # Deleting "ESL L" for levels.
complete_learners["Level"].replace(to_replace="ABE L", value="", inplace=True, limit=None, regex=True, method='pad') # Deleting "ABE L" for level.
complete_learners["Level"] = complete_learners["Level"].astype(int) # Turn "Level" column values into integers.
complete_learners.to_csv('all_learners.csv', index=True, header=True, index_label=None) #Create csv file for the complete list.

# Separating listening and reading tests, and pre and post tests.
reading_tests = complete_learners[complete_learners["Modality ID"] == 1] # Create reading tests data frame
listening_tests = complete_learners[complete_learners["Modality ID"] == 2] # Create listening tests data frame
pre_listening = listening_tests.loc[listening_tests.groupby('Student ID')["Date"].idxmin()] # Create data frame with listening pre-tests only.
pre_reading = reading_tests.loc[reading_tests.groupby('Student ID')["Date"].idxmin()] # Create data frame with reading pre-tests only
post_listening = pd.merge(listening_tests, pre_listening, how='outer', indicator=True) # Merge to indicate which tests are listening pre-tests.
post_listening = post_listening.drop(post_listening[post_listening._merge == "both"].index) # Delete listening pre-tests from df.
post_reading = pd.merge(reading_tests, pre_reading, how='outer', indicator=True) # Merge to indicate which tests are reading pre-tests.
post_reading = post_reading.drop(post_reading[post_reading._merge == "both"].index) # Delete reading pre-tests from df.

# Deleting post_tests that got lower scores and keep only highest scores.
post_listening = post_listening.loc[post_listening.groupby('Student ID')["Score"].idxmax()]
post_reading = post_reading.loc[post_reading.groupby("Student ID")["Score"].idxmax()]

# Join pre_listening tests and post_listening tests, and pre-reading tests and post-listening tests, separately.
listening_tests = pd.merge(pre_listening, post_listening, how= "outer", on= "Student ID")
reading_tests = pd.merge(pre_reading, post_reading, how= "outer", on= "Student ID")

# Ready data frames for MySQL.
listening_tests.drop(listening_tests[["Modality ID_y", "Current FY Instr Hrs_y", "_merge"]], axis=1, inplace=True) # Delete unnecessary columns.
reading_tests.drop(reading_tests[["Modality ID_y", "Current FY Instr Hrs_y", "_merge"]], axis=1, inplace=True) # Delete unnecessary columns.
listening_tests["Modality ID_x"] = listening_tests["Modality ID_x"].astype(int) # Transform decimal values into integers.
reading_tests["Modality ID_x"] = reading_tests["Modality ID_x"].astype(int) # Transform decimal values into integers.
listening_tests["Level_y"] = listening_tests["Level_y"].fillna(0) # Transform empty values into 0.
reading_tests["Level_y"] = reading_tests["Level_y"].fillna(0) # Transform empty values into 0.
listening_tests["Level_y"] = listening_tests["Level_y"].astype(int) # Transform decimal values into integers.
reading_tests["Level_y"] = reading_tests["Level_y"].astype(int) # Transform decimal values into integers.
listening_tests = listening_tests.fillna("NULL") # Replace NaN values with NULL
reading_tests = reading_tests.fillna("NULL") # Replace NaN values with NULL


listening_tests.to_csv('listening_tests.csv', index=True, header=True, index_label=None) # Export to csv
reading_tests.to_csv('reading_tests.csv', index=True, header=True, index_label=None) # Export to csv
