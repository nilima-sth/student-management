# Student Management (Odoo 19)

This module adds a complete student administration app in Odoo, built on top of `res.partner`.

## Features

- Student profile management (extends contacts):
  - Date of birth and computed age
  - Enrollment date
  - Student lifecycle stage (draft, documents pending, approved, admitted, active, alumni, cancelled)
  - Quick actions: admit, mark alumni, cancel student
- Course management:
  - Course name, code, description, duration, fee
  - Student-course many-to-many enrollment
- Guardian management:
  - Link guardians to students with relationship type
  - Contact fields (phone, email, address)
- Classroom management:
  - Semester-based classrooms
  - Class teacher assignment
  - Subject/course mapping
  - Student count computation
- Attendance management:
  - Attendance header with date, class, and teacher
  - Auto-populated attendance lines from selected classroom
  - Present/absent counters
- Student report cards:
  - Per-student report records
  - Subject-wise lines with full marks, pass marks, obtained marks
  - Pass/fail boolean per line
  - Computed total obtained marks

## Main Models

- `res.partner` (extended): student flags and classroom assignment
- `student.course`
- `student.guardian`
- `student.classroom`
- `student.attendance`
- `student.attendance.line`
- `student.report`
- `student.report.line`

## Dependencies

From `__manifest__.py`:

- `base`
- `contacts`
- `account`
- `web_map`

## Menus

The module adds a top-level **Student Management** app with menus for:

- Students
- Courses
- Guardians
- Classrooms
- Attendance
- Report Cards

## Installation

1. Put this addon inside your Odoo custom addons path.
2. Update the app list from Odoo Apps.
3. Search for `SMS` (Student Management System).
4. Install the module.

## Notes

- Student records are contacts (`res.partner`) with `is_student = True`.
- Attendance lines are generated from classroom students when classroom changes.
- Access rights are defined in `security/ir.model.access.csv`.
