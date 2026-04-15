# 🎓 Student Management System (Odoo 19)

The **Student Management System (SMS)** module provides a complete student administration solution in Odoo 19. It is built on top of the existing `res.partner` model, extending Contacts to manage students efficiently.

---

## 🚀 Key Features

### 👩‍🎓 Student Profile Management  
*(Extends Odoo Contacts)*

- Date of Birth with **computed age**
- Enrollment date tracking
- Student lifecycle stages:
  - Draft  
  - Documents Pending  
  - Approved  
  - Admitted  
  - Active  
  - Alumni  
  - Cancelled  
- Quick action buttons:
  - Admit student  
  - Mark as Alumni  
  - Cancel student  

---

### 📚 Course Management

- Course name, code, description
- Duration and fee configuration
- Many-to-many student-course enrollment relationship

---

### 👨‍👩‍👧 Guardian Management

- Link guardians to students
- Define relationship type (e.g., Father, Mother, Guardian)
- Contact details:
  - Phone  
  - Email  
  - Address  

---

### 🏫 Classroom Management

- Semester-based classroom structure
- Assign class teacher
- Map subjects/courses to classrooms
- Automatically computed student count

---

### 🗓️ Attendance Management

- Attendance header:
  - Date  
  - Classroom  
  - Teacher  
- Automatically generated attendance lines based on selected classroom students
- Computed counters:
  - Total Present  
  - Total Absent  

---

### 📝 Student Report Cards

- Individual student report records
- Subject-wise report lines including:
  - Full marks  
  - Pass marks  
  - Obtained marks  
- Automatic pass/fail status per subject
- Computed total obtained marks

---

## 🧩 Main Models

| Model | Description |
|-------|------------|
| `res.partner` (extended) | Student flags, lifecycle stage, classroom assignment |
| `student.course` | Course management |
| `student.guardian` | Guardian-student relationship |
| `student.classroom` | Classroom and semester management |
| `student.attendance` | Attendance header |
| `student.attendance.line` | Attendance details per student |
| `student.report` | Student report card |
| `student.report.line` | Subject-wise marks |

---

## 📦 Dependencies

Defined in `__manifest__.py`:

- `base`
- `contacts`
- `account`
- `web_map`

---

## 🗂️ Menus

Adds a top-level **Student Management** application with the following menus:

- Students  
- Courses  
- Guardians  
- Classrooms  
- Attendance  
- Report Cards  

---

## ⚙️ Installation

1. Place the module inside your custom addons path.
2. Update the Apps list in Odoo.
3. Search for **SMS – Student Management System**.
4. Click **Install**.

---

## 📌 Technical Notes

- Students are stored as `res.partner` records with `is_student = True`.
- Attendance lines are auto-generated when a classroom is selected.
- Access rights are configured in `security/ir.model.access.csv`.
- Age, student count, attendance counters, and total marks are computed fields.