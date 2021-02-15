# Data cleaning for reports from online platform for adult education

# Overview:
This repository contains the code to clean a Student Assessment report pulled from an adult education online platform used by numerous adult education nonprofit organizations.

# Goal:
The report from the paltform can be pulled either as a pdf or an xlsx file. Unfortunately, the xlsx file comes with lots of formatting, merging, empty columns, etc., and 
cannot be used to compute any aggregate information necessary for organizations that use the platform and are restricted by state policy requirements. 
This "necessary information" includes, for example, number of active learners with a valid progress test, score difference, selection of best progress test, presence/absence 
of EFL gains, among others.

# Files included:
The repository contains two files: 
>.py : It cleans the data and produces a simple data frame.

>.sql : It works on the - imported - data frame to produce aggregate information.
