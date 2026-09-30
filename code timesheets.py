import pandas as pd
from word2number import w2n

validation_results = [] # list for validation issues / warnings

# convert the hours existing in text (i.e, "seven") to number (i.e, 7)
def convert_hours(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        try:
            return float(w2n.word_to_num(str(value).lower()))
        except:
            return None

#paths that are used as input / output
INPUT_PATH = "C:/temp/timesheets/"
OUTPUT_PATH = "C:/temp/timesheets/output/"

#files that are used as input
projects_file = INPUT_PATH + "projects.csv"
employees_file = INPUT_PATH + "employees.csv"
timesheets_file = INPUT_PATH + "timesheets.csv"


#read the data of the input files
projects = pd.read_csv(projects_file)
employees = pd.read_csv(employees_file)
timesheets = pd.read_csv(timesheets_file)


# Clean column names (remove spaces - for exact mapping)
projects.columns = projects.columns.str.strip()
employees.columns = employees.columns.str.strip()
timesheets.columns = timesheets.columns.str.strip()


# VALIDATION OF projects.csv
for index, row in projects.iterrows():
    project_id = row["project_id"]

    if pd.isna(project_id) or str(project_id).strip() == "":
        validation_results.append({
            "WORKSHEET": "projects",
            "KEY IDENTIFICATION": "",
            "STATUS": "REJECTED",
            "COMMENT": "Project ID is missing"
        })

    elif pd.isna(row["project_name"]) or str(row["project_name"]).strip() == "":
        validation_results.append({
            "WORKSHEET": "projects",
            "KEY IDENTIFICATION": project_id,
            "STATUS": "FURTHER REVIEW",
            "COMMENT": "Project name is missing"
        })

    if pd.isna(row["budget"]) or str(row["budget"]).strip() == "":
        validation_results.append({
            "WORKSHEET": "projects",
            "KEY IDENTIFICATION": project_id,
            "STATUS": "FURTHER REVIEW",
            "COMMENT": "Project budget is missing"
        })

    else:
        budget = pd.to_numeric(row["budget"], errors="coerce")

        if not pd.isna(budget) and budget < 0:
            validation_results.append({
                "WORKSHEET": "projects",
                "KEY IDENTIFICATION": project_id,
                "STATUS": "REJECTED",
                "COMMENT": "Project budget cannot be negative"
            })

projects = projects[projects["project_id"].notna()].copy() # project id is required
projects = projects.drop_duplicates(subset=["project_id"]) #remove duplicate entries from projects data

# VALIDATION OF employees.csv
for index, row in employees.iterrows():
    employee_id = row["employee_id"]
    if pd.isna(employee_id) or str(employee_id).strip() == "":
        validation_results.append({
            "WORKSHEET": "employees",
            "KEY IDENTIFICATION": "",
            "STATUS": "REJECTED",
            "COMMENT": "Employee ID is missing"
        })
        continue

    if pd.isna(row["name"]) or str(row["name"]).strip() == "":
        validation_results.append({
            "WORKSHEET": "employees",
            "KEY IDENTIFICATION": employee_id,
            "STATUS": "FURTHER REVIEW",
            "COMMENT": "Employee name is missing"
        })
    
    if pd.isna(row["role"]) or str(row["role"]).strip() == "":
        validation_results.append({
            "WORKSHEET": "employees",
            "KEY IDENTIFICATION": employee_id,
            "STATUS": "FURTHER REVIEW",
            "COMMENT": "Employee role is missing"
        })
employees = employees[employees["employee_id"].notna()].copy() # employee id is required 
employees = employees.drop_duplicates(subset=["employee_id"]) #remove duplicate entries from employees data


# VALIDATION OF timesheets.csv
valid_employee_ids = set(employees["employee_id"])
valid_project_ids = set(projects["project_id"])

for index, row in timesheets.iterrows():

    employee_id = row["employee_id"]
    project_id = row["project_id"]

    key = f"{employee_id} / {project_id}"

    if pd.isna(employee_id) or str(employee_id).strip() == "":
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": "Employee ID is missing"
        })

    elif employee_id not in valid_employee_ids:
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": "Employee ID does not exist in employees.csv"
        })

    if pd.isna(project_id) or str(project_id).strip() == "":
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": "Project ID is missing"
        })

    elif project_id not in valid_project_ids:
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": "Project ID does not exist in projects.csv"
        })

    date = pd.to_datetime(row["date"],format="%d-%m-%y",errors="coerce")
    if pd.isna(date):
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": "Invalid or missing date"
        })

        
    # Invalid hours
    hours = convert_hours(row["hours"])
    if hours is None or hours <= 0 or hours > 24:
        validation_results.append({
            "WORKSHEET": "timesheets",
            "KEY IDENTIFICATION": key,
            "STATUS": "REJECTED",
            "COMMENT": f"Invalid hours value: {row['hours']}"
        })
        
    
timesheets = timesheets[timesheets["employee_id"].notna()].copy() # employee id is required 
timesheets = timesheets[timesheets["project_id"].notna()].copy() # project id is required
timesheets = timesheets[timesheets["employee_id"].isin(employees["employee_id"])].copy() #check that employee id of timesheets.csv exists in employee.scv
timesheets = timesheets[timesheets["project_id"].isin(projects["project_id"])].copy()#check that project id of timesheets.csv exists in projects.scv
timesheets["date"] = pd.to_datetime(timesheets["date"],format="%d-%m-%y",errors="coerce") # transform the dates to yyyy-mm-dd format 
timesheets = timesheets[timesheets["date"].notna()].copy() # days are required

timesheets["hours"] = timesheets["hours"].apply(convert_hours)

timesheets = timesheets[(timesheets["hours"].notna())&(timesheets["hours"] > 0)&(timesheets["hours"] <= 24)].copy() # hours in range [0,24]
timesheets = timesheets.drop_duplicates(subset=["employee_id", "project_id", "date"]) # Remove duplicate entries (one employee can have only one timesheet per project ped date)


#Save the clean version of timesheets.csv
timesheets["date"] = timesheets["date"].dt.strftime("%Y-%m-%d")


# Creation of a full info timesheets file (include enployees, projects & timesheets data) - full_info_timesheets.csv 
full_info_timesheets = timesheets.merge(employees[["employee_id", "name", "role"]],on="employee_id",how="left")
full_info_timesheets = full_info_timesheets.merge(projects[["project_id", "project_name", "budget"]],left_on="project_id",right_on="project_id",how="left")
full_info_timesheets = full_info_timesheets.rename(columns={"name": "employee_name","role": "employee_role","Project name": "project_name","Budget": "budget"}) #rename columns
full_info_timesheets = full_info_timesheets[["project_id", "project_name",  "budget", "employee_id","employee_name","employee_role","date","hours"]] #reorder columns

#Creation of issues / warning file 
validation_df = pd.DataFrame(validation_results,columns=["WORKSHEET","KEY IDENTIFICATION","STATUS","COMMENT"])
validation_file = OUTPUT_PATH + "validation_issues.xlsx"
validation_df.to_excel(validation_file,index=False,sheet_name="validation_results")


# USEFUL OUTPUTS FOR FURTHER ANALYSIS

# 1. PROJECT SUMMARY WS (Total hours, budget, number of employees involved per project)
project_summary = (full_info_timesheets.groupby(["project_id", "project_name", "budget"],as_index=False).agg(total_hours=("hours", "sum"),employees_involved=("employee_id", "nunique")))


# 2. EMPLOYEE SUMMARY WS (Total hours and number of projects per employee)
employee_summary = (full_info_timesheets.groupby(["employee_id", "employee_name", "employee_role"],as_index=False).agg(total_hours=("hours", "sum"),projects_count=("project_id", "nunique")))


# 3. EMPLOYEE_PROJECT (total hours per project for each employee)
hours_per_employee_project = (full_info_timesheets.groupby(["employee_id","employee_name","employee_role","project_id","project_name"],as_index=False)["hours"].sum())
hours_per_employee_project = hours_per_employee_project.rename(columns={"hours": "total_hours"})


#Creation of output excel files
excel_file = OUTPUT_PATH + "clean_timesheets & analysis.xlsx"

with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:

    # clean_timesheets WS
    timesheets.to_excel(writer,sheet_name="clean_timesheets",index=False)

    # full_info_timesheets WS
    full_info_timesheets.to_excel(writer,sheet_name="full_info_timesheets",index=False)

    # project_summary WS
    project_summary.to_excel(writer,sheet_name="project_summary",index=False)
    
    # employee_summary WS
    employee_summary.to_excel(writer,sheet_name="employee_summary",index=False)
    
    # employee_project WS
    hours_per_employee_project.to_excel(writer,sheet_name="employee_project",index=False)

#SUMMARY 
print(f"Valid projects.csv entries: {len(projects)}")
print(f"Valid employees.csv entries: {len(employees)}")
print(f"Valid timesheets.scv entries: {len(timesheets)}")
print()
print("Created files:")
print("- clean_timesheets & analysis.xlsx")
print ("- validation_issues.xlsx")
