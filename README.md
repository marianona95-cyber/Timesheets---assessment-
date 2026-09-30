Validation cleaning, and summarizing exercise using employee, project & timesheet data
By Maria Nona


         Project Summary

The scope of this project is to produce a validated and cleaned timesheet dataset, enriched by combining data from the input files and supplemented with aggregated information for further analysis.
The entire process has been developed and automated using a Python script.

The script uses three input files:
•	projects.csv
•	employees.csv
•	timesheets.csv

The input files have been placed locally in the path c/temp/ timesheets for implementation purposes. 

By performing validation tests on these files separately, the script produces the file clean_timesheets & analysis.xlsx that includes 

•	A clean version of timesheets.csv, excluding problematic cases.
•	A combined dataset containing information from all three input files, using employee_id and project_id as mapping keys. The combination is performed using the cleaned datasets.
•	Aggregated data for further analysis:
        o       Project Summary
        o	Employee Summary
        o	Employee Project

Also, the process produces a file validation_issues.xlsx that includes the cases that have been rejected through the cleansing and validation process and the cases that need to be further reviewed. 

The output path has been defined through the process as: c/temp/ timesheets /output


 	Assumptions & Validation Rules

•	projects.csv 
        o       The project_id is required and should be unique. Missing project id is flagged as rejected and is excluded from the final clean dataset.If double entries are identified, only the one is included to the final clean dataset.
        o       The project name has not restrictions. Missing project name is included in the final clean dataset and is flagged as further review to the validation_issues.xlsx 
        o       If numerical, budget must not be negative. Range values are preserved as provided. Missing budget is flagged as further review to the validation_issues.xlsx

•	employees.csv 
        o       The employee_id is required and should be unique. Missing employee id is flagged as rejected and is excluded from the final clean dataset.If double entries are identified, only the one is included
        o       The employee name has not restrictions. Missing employee name is included in the final clean dataset and is flagged as further review to the validation_issues.xlsx
        o       The employee role has not restrictions. Missing employee role is included in the final clean dataset and is flagged as further review to the validation_issues.xlsx

•	timesheets.csv 
        o       The employee id is required and must exist in employees.csv. Missing or unknown employee id is flagged as rejected and is excluded from the final clean dataset.
        o       The project id is required and must exist in projects.csv. Missing or unknown project id is flagged as rejected and is excluded from the final clean dataset.
        o       The date is required as it is part of the timesheets key and must be a valid date in DD-MM-YY format. Invalid or missing date is flagged as rejected and is excluded from the final clean dataset.
        o       The field hours is required and must be >  0 and ≤ 24. Invalid hours are flagged as rejected and are excluded from the final clean dataset.


        NOTES 

•	Hours can be provided either as numbers or as words (e.g. 8 or eight).
•	The original budget value from projects.csv is preserved without transformation or calculation. Therefore, ranges such as 3-5 remain unchanged in the output.

                    ASSUMPTIONS

•	Ηours is not part of the primary key, but it is required because it is the main measure used in the analysis and aggregation outputs. Records with missing or invalid hours are therefore excluded from the final dataset.
•	Records are classified into three categories: 
       o	Rejected records, which are excluded from the final dataset and are flagged in the validation output
       o	Records requiring further review, which remain in the dataset but are flagged in the validation output. 
       o	Records without validation issues are accepted and included in the final dataset without a validation entry.


        OUTPUTS

        The process exports 2 excel files: 

1.	validation_issues.xlsx
        Contains all identified Issues and Warnings in the validation_results worksheet.

2.	clean_timesheets & analysis.xlsx
        Contains the following worksheets:
        •	clean_timesheets — cleaned and validated timesheet data.
        •	full_info_timesheets — combined information from employees, projects, and timesheets.
        •	project_summary — total hours and number of employees involved per project, accompanied by the budget.
        •	employee_summary — total hours and number of projects per employee.
        •	employee_project — total hours per employee and project.


        HOW I ENSURED THE PIPELINE CAN BE SAFELY RERUN 
The pipeline is designed to be rerunnable because it reads the original input CSV files and generates the output files from scratch on each execution. 
The validation results are stored in a new validation_results list for each run, while the input data is not modified directly. 
The cleaning and validation steps are deterministic, including removing invalid records and duplicates based on defined keys. 
The output Excel files are also overwritten with the latest results, preventing old results from being mixed with new data. 
Therefore, running the pipeline multiple times with the same input files produces consistent outputs without accumulating duplicate records or validation issues.

       HOW I WOULD IMPROVE OR SCALE THIS SOLUTION WITH MORE TIME How
With more time, I would make the pipeline more modular by separating the validation, cleaning, transformation, and reporting steps into individual functions. 
I would also introduce configuration files for input/output paths and validation rules instead of hardcoding them in the script. 
Finally, I would improve logging and error handling so that each pipeline run produces a clear execution log and can be monitored more easily in a production environment.



