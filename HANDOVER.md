GLAZE / PASTRIES HANDOVER

Last Updated: June 2026

Purpose

This repository contains the GLAZE development framework and the PASTRIES operational application.

PASTRIES stands for:

Programme Administration & Student Tracking Register Information Efficiency System

The purpose of the system is to replace spreadsheet-based administration with a single operational platform for:

Students
Payments
Classes
Attendance (future)
Film Projects (future)
Reporting

The primary user is Tanya.

The primary design goal is simplicity and familiarity.

Current Status

Current phase:

Master Data Foundation Complete

Implemented:

Student ingestion pipeline
Enrolment ingestion pipeline
SQLite database
Streamlit application
Student-payment join view
Single source of truth architecture

Not yet implemented:

Attendance
Automated bank reconciliation
Teacher interface
Big Film management
Parent portal
System Architecture

The architecture follows a strict layered design.

Raw Data
↓
ETL Scripts
↓
SQLite Database
↓
Data Loader
↓
Streamlit Interface

No layer should bypass another layer.

Source Of Truth Rules
Rule 1

SQLite is the operational source of truth.

Database:

/Users/stephenwoods/Documents/glaze/data/glaze.db

The application should read from SQLite.

The application should not read operational data directly from CSV files.

Rule 2

Students exist once.

A student record must never be duplicated across multiple tables.

The students table is authoritative.

All other systems reference student_id.

Rule 3

Generated outputs are disposable.

Files such as:

students_master.csv
enrollments.csv

are generated artefacts.

If they are wrong:

fix the ETL.

Do not manually edit generated files.

Folder Structure
Data
/Users/stephenwoods/Documents/glaze/data

Contains:

Source CSV files
SQLite database
sqlite_ready outputs
Database
/Users/stephenwoods/Documents/glaze/data/glaze.db

Current tables:

students
enrollments
payments

Future tables:

attendance
classes
film_projects
communications
ETL Scripts
/Users/stephenwoods/Documents/glaze/scripts

Purpose:

Convert spreadsheets into clean structured datasets.

Current key script:

build_students_master.py
Data Access Layer
/Users/stephenwoods/Documents/glaze/core

Current key file:

data_loader.py

Purpose:

All application data access should happen here.

The UI should not contain SQL.

The UI should not read CSVs directly.

User Interface
/Users/stephenwoods/Documents/glaze/domains/pastries

Current key file:

app.py

Purpose:

Presentation only.

Display data.

Filter data.

Eventually edit data.

No business logic should live here.

Current Operational Workflow

Register CSV Files
↓
build_students_master.py
↓
students_master.csv
enrollments.csv
↓
SQLite Import
↓
glaze.db
↓
data_loader.py
↓
Streamlit Interface

Current UI

Current user-facing modules:

Students

Displays:

student records
enrolment information
Payments

Displays:

student payment summary
payment status
Development Principles
Keep Tanya Comfortable

The application should feel like an improved spreadsheet.

Not enterprise software.

Not a CRM.

Not an ERP.

Views Over Tables

Whenever possible:

Build views.

Do not create duplicate tables.

Example:

Master Tracker should be generated from:

students
+
payments

rather than stored separately.

Simplicity First

A working simple solution is preferred over a sophisticated unfinished solution.

No Duplicate Sources Of Truth

Never allow:

students spreadsheet
+
tracker spreadsheet
+
attendance spreadsheet

to become separate authoritative datasets.

There should be one student record.

Everything else references it.

Next Phase

Phase Name:

Master Tracker Stabilisation

Objectives:

Master Tracker view
Monthly payment columns
Current student payment warnings
CSV export
Upload Bank Statement page

Explicitly out of scope:

Attendance
Big Film
Teacher Portal
Parent Portal

until Tracker is stable.

Startup Procedure

Activate environment:

source /Users/stephenwoods/Documents/glaze/venv/bin/activate

Set project root:

export PYTHONPATH=/Users/stephenwoods/Documents/glaze

Run application:

streamlit run /Users/stephenwoods/Documents/glaze/domains/pastries/app.py
Critical Files

Highest-value files for understanding the system:

/Users/stephenwoods/Documents/glaze/domains/pastries/app.py

/Users/stephenwoods/Documents/glaze/core/data_loader.py

/Users/stephenwoods/Documents/glaze/scripts/build_students_master.py

Database creation script (if present)

A competent developer should begin with these files.

Long-Term Vision

PASTRIES should evolve into a unified operational platform.

Potential future modules:

Attendance
Teacher Dashboard
Parent Management
Film Project Management
Reporting
Communications
Analytics

The long-term objective is:

One student record.

One payment history.

One attendance history.

One source of truth.

Everything else becomes a view of that data.
