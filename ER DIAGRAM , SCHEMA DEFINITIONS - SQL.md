       ER DIAGRAM 
RELATIONS ----> (employees.employee_id --> timesheets.employee_id)     (projects.project_id --> timesheets.project_id)

PRIMARY KEYS ---> (employees.employee_id) , (projects.project_id)

COMPOSITE PRIMARY KEY ---> (timesheets.employee_id, timesheets.project_id, timesheets_date)

FOREIGN KEYS ---> (timesheets.employee_id) , (timesheets.project_id)





       RELATIONAL SCHEMA - SQL - SCHEMA DEFINITIONS

CREATE TABLE projects (
    project_id VARCHAR(50) PRIMARY KEY,
    project_name VARCHAR(255),
    budget VARCHAR(50)
);

CREATE TABLE employees (
    employee_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255),
    role VARCHAR(255)
);

CREATE TABLE timesheets (
    employee_id VARCHAR(50) NOT NULL,
    project_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    hours DECIMAL(5, 2) NOT NULL,

    PRIMARY KEY (employee_id, project_id, date),

    FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),

    FOREIGN KEY (project_id)
        REFERENCES projects(project_id),

    CHECK (hours > 0 AND hours <= 24)
);


NOTE ---> The budget field is stored as text because the source data may contain both numeric values and ranges (e.g. 3-5).  



