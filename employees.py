from operator import index
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Treeview

from django.db import connection
from django.db.models.sql.compiler import cursor_iter
from tkcalendar import DateEntry
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='root12345')
        cursor = connection.cursor()
    except:
        messagebox.showerror('Error', 'Database connectivity issue,Open mysql command line client')
        return None, None

    return cursor, connection


def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventorys_system')
    cursor.execute('USE inventorys_system')
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS employee_data(empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), education VARCHAR(50),'
        'work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50), designation VARCHAR(50), leave_approval VARCHAR(50))')


def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventorys_system')
    try:
        cursor.execute('SELECT * from employee_data')
        employee_record = cursor.fetchall()
        employee_treeview.delete(*employee_treeview.get_children())
        for record in employee_record:
            employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event, empid_entry, name_entry, email_entry,
                gender_combobox, dob_date_entry, contact_entry,
                employment_type_combobox, education_combobox,
                work_shift_combobox, address_text,
                doj_date_entry, salary_entry,
                designation_combobox,
                leave_approval_combobox):
    index = employee_treeview.selection()
    content = employee_treeview.item(index)
    row = content['values']
    clear_fields(empid_entry, name_entry, email_entry,
                 gender_combobox, dob_date_entry, contact_entry,
                 employment_type_combobox, education_combobox,
                 work_shift_combobox, address_text,
                 doj_date_entry, salary_entry,
                 designation_combobox,
                 leave_approval_combobox, False)
    print(row)
    empid_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    employment_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    designation_combobox.set(row[12])
    leave_approval_combobox.set(row[13])


def add_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                 designation, leave_approval):
    if (
            empid == '' or name == '' or email == '' or gender == 'Select Gender' or employment_type == 'Select type' or education == 'Select Education' or
            work_shift == 'Select Shift' or address == '\n' or salary == '' or
            designation == 'Select Designation' or leave_approval == 'Select Approval Status'):
        messagebox.showerror('Error', 'ALL fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventorys_system')
        try:
            cursor.execute('SELECT empid from employee_data WHERE empid=%s', (empid,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'ID already exists')
                return
            cursor.execute('INSERT INTO employee_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (
                empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                designation, leave_approval))
            connection.commit()
            treeview_data()
            messagebox.showinfo('SUCCESS', 'Data is inserted successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def clear_fields(empid_entry, name_entry, email_entry,
                 gender_combobox, dob_date_entry, contact_entry,
                 employment_type_combobox, education_combobox,
                 work_shift_combobox, address_text,
                 doj_date_entry, salary_entry,
                 designation_combobox,
                 leave_approval_combobox, check):
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    from datetime import date
    dob_date_entry.set_date(date.today())
    gender_combobox.set('Select Gender')
    contact_entry.delete(0, END)
    employment_type_combobox.set('Select Type')
    education_combobox.set('Select Education')
    work_shift_combobox.set('Select Work-Shift')
    address_text.delete(1.0, END)
    doj_date_entry.set_date(date.today())
    salary_entry.delete(0, END)
    designation_combobox.set('Select designation')
    leave_approval_combobox.set('Select Approval Status')
    if check:
        employee_treeview.selection_remove(employee_treeview.selection())


def update_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                    salary, designation, leave_approval):
    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return

    # Ensure all fields are filled
    if not all([empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
                designation, leave_approval]):
        messagebox.showerror('Error', 'All fields must be filled')
        return

    try:
        cursor, connection = connect_database()
        if not cursor or not connection:
            messagebox.showerror('Error', 'Failed to connect to the database')
            return

        cursor.execute('USE inventorys_system')

        # Correct query to fetch data based on empid
        cursor.execute('SELECT * FROM employee_data WHERE empid=%s', (empid,))
        current_data = cursor.fetchone()

        if current_data is None:
            messagebox.showerror('Error', 'Employee ID does not exist')
            return

        # Extract relevant columns from current data (assuming the order in current_data is [empid, name, ...])
        current_name, current_email, current_gender, current_dob, current_contact, current_employment_type, current_education, current_work_shift, current_address, current_doj, current_salary, current_designation, current_leave_approval = current_data[1:]

        # Create new data tuple
        new_data = (name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, designation, leave_approval)

        print("Current Data:", current_data)  # For debugging
        print("New Data:", new_data)  # For debugging

        # Compare only the relevant fields
        if (current_name, current_email, current_gender, current_dob, current_contact, current_employment_type,
            current_education, current_work_shift, current_address, current_doj, current_salary, current_designation, current_leave_approval) == new_data:
            messagebox.showinfo('Information', 'No changes detected')
            return

        # Perform update
        cursor.execute('''
            UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, employment_type=%s,
                                 education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, designation=%s, leave_approval=%s
            WHERE empid=%s
        ''', (
            name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary,
            designation, leave_approval, empid
        ))

        connection.commit()

        # Update the treeview with the new data
        treeview_data()  # Assuming this function updates the treeview
        messagebox.showinfo('Success', 'Data is updated successfully')

    except Exception as e:
        messagebox.showerror('Error', f"An error occurred: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def delete_employee(empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj,
                    salary, designation, leave_approval):
    selected = employee_treeview.selection()

    if not selected:
        messagebox.showerror('ERROR', 'No row is selected')
        return

    # Confirm deletion
    result = messagebox.askyesno('Confirm', 'Do you really want to delete the records?')

    if result:
        try:
            cursor, connection = connect_database()
            if not cursor or not connection:
                messagebox.showerror('ERROR', 'Failed to connect to the database')
                return

            cursor.execute('USE inventorys_system')  # Corrected the typo in the database name

            # Execute delete query
            cursor.execute('DELETE FROM employee_data WHERE empid=%s', (empid,))

            connection.commit()  # Ensure you actually commit the changes

            # Update the treeview to reflect the changes
            treeview_data()
            messagebox.showinfo('SUCCESS', 'Record is deleted')

        except Exception as e:
            messagebox.showerror('ERROR', f"An error occurred: {e}")

        finally:
            # Always close the cursor and connection after use
            if cursor:
                cursor.close()
            if connection:
                connection.close()


def search_employee(search_option,value):
    if search_option=='SEARCH BY':
        messagebox.showerror('Error','NO option is selected')
    elif value=='':
        messagebox.showerror('Error','Enter the value to search')
    else:
        cursor,connection = connect_database()
        if not  cursor or not connection:
            return
        try:
            cursor.execute('use inventorys_system')
            cursor.execute(f'SELECT * from employee_data WHERE {search_option} LIKE %s',f'%{value}%')
            records=cursor.fetchall()
            employee_treeview.delete(*employee_treeview.get_children())
            for record in records:
                employee_treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('ERROR', f"An error occurred: {e}")

        finally:
            # Always close the cursor and connection after use
            if cursor:
                cursor.close()
            if connection:
                connection.close()


def show_all(search_entry,search_combobox):
    treeview_data()
    search_entry.delete(0,END)
    search_combobox.set('SEARCH BY')






















# Functionality part
def employee_form(window):
    global back_image, employee_treeview
    employee_frame = Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=100)
    headingLabel = Label(employee_frame, text='MANAGE EMPLOYEE DETAILS', font=('times new roman', 16, 'bold'),
                         bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='back.png')

    top_frame = Frame(employee_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('empid', 'Name', 'Email', 'employment_type',
                                                         'education', 'work_shift'), font=('times new roman', 12),
                                   state='readonly', justify=CENTER)
    search_combobox.set('SEARCH BY')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)

    search_button = Button(search_frame, text='SEARCH', font=('times new roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda :search_employee(search_combobox.get(),search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    show_button = Button(search_frame, text='SHOW ALL', font=('times new roman', 12), width=10, cursor='hand2',
                         fg='white', bg='#0f4d7d',command=lambda :show_all(search_entry,search_combobox))
    show_button.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)

    employee_treeview = ttk.Treeview(top_frame, columns=(
        'empid', 'name', 'email', 'gender', 'dob', 'contact', 'employment_type', 'education', 'work_shift', 'address',
        'doj', 'designation', 'salary', 'leave_approval'), show='headings', yscrollcommand=vertical_scrollbar.set,
                                     xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_treeview.xview)
    vertical_scrollbar.config(command=employee_treeview.yview)
    employee_treeview.pack(pady=(10, 0))

    employee_treeview.heading('empid', text='EmpID')
    employee_treeview.heading('name', text='Name')
    employee_treeview.heading('email', text='Email')
    employee_treeview.heading('gender', text='Gender')
    employee_treeview.heading('dob', text='Date of Birth')
    employee_treeview.heading('contact', text='Contact')
    employee_treeview.heading('employment_type', text='Employment Type')
    employee_treeview.heading('education', text='Education')
    employee_treeview.heading('work_shift', text='Work Shift')
    employee_treeview.heading('address', text='Address')
    employee_treeview.heading('doj', text='Date of Joining')
    employee_treeview.heading('designation', text='Designation')
    employee_treeview.heading('salary', text='Salary')
    employee_treeview.heading('leave_approval', text='Leave Approval')

    employee_treeview.column('empid', width=60)
    employee_treeview.column('name', width=140)
    employee_treeview.column('email', width=180)
    employee_treeview.column('gender', width=80)
    employee_treeview.column('contact', width=100)
    employee_treeview.column('dob', width=100)
    employee_treeview.column('employment_type', width=120)
    employee_treeview.column('education', width=120)
    employee_treeview.column('work_shift', width=100)
    employee_treeview.column('address', width=200)
    employee_treeview.column('doj', width=100)
    employee_treeview.column('designation', width=120)
    employee_treeview.column('salary', width=140)
    employee_treeview.column('leave_approval', width=120)

    treeview_data()

    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    empid_label = Label(detail_frame, text='EmpId', font=('times new roman', 12), bg='white')
    empid_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    empid_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    empid_entry.grid(row=0, column=1, padx=20, pady=10)

    name_label = Label(detail_frame, text='Name', font=('times new roman', 12), bg='white')
    name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    name_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    name_entry.grid(row=0, column=3, padx=20, pady=10)

    email_label = Label(detail_frame, text='Email', font=('times new roman', 12), bg='white')
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = Label(detail_frame, text='Gender', font=('times new roman', 12), bg='white')
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female', 'Other'), font=('times new roman', 12),
                                   width=18, state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)

    dob_label = Label(detail_frame, text='Date of Birth', font=('times new roman', 12), bg='white')
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    dob_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly',
                               date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1, column=3)

    contact_label = Label(detail_frame, text='Contact', font=('times new roman', 12), bg='white')
    contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    employment_type_label = Label(detail_frame, text='Employment Type', font=('times new roman', 12), bg='white')
    employment_type_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    employment_type_combobox = ttk.Combobox(detail_frame, values=('Full-Time', 'Part-Time', 'Casual', 'Intern'),
                                            font=('times new roman', 12),
                                            width=18, state='readonly')
    employment_type_combobox.set('Select Type')
    employment_type_combobox.grid(row=2, column=1)

    education_label = Label(detail_frame, text='Education', font=('times new roman', 12), bg='white')
    education_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')
    education_options = ["B.com", "M.com", "B.sc", "M.sc", "BBA"]

    education_combobox = ttk.Combobox(detail_frame, values=education_options, font=('times new roman', 12),
                                      width=18, state='readonly')
    education_combobox.set('Select Education ')
    education_combobox.grid(row=2, column=3)

    work_shift_label = Label(detail_frame, text='Work-Shift', font=('times new roman', 12), bg='white')
    work_shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')
    work_shift_combobox = ttk.Combobox(detail_frame, values=('Morning', 'Afternoon', 'Night'),
                                       font=('times new roman', 12),
                                       width=18, state='readonly')
    work_shift_combobox.set('Select Work-Shift ')
    work_shift_combobox.grid(row=2, column=5)

    address_label = Label(detail_frame, text='Address', font=('times new roman', 12), bg='white')
    address_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('times new roman', 12), bg='lightyellow')
    address_text.grid(row=3, column=1, rowspan=2)

    doj_label = Label(detail_frame, text='Date of Joining', font=('times new roman', 12), bg='white')
    doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly',
                               date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=3)

    designation_label = Label(detail_frame, text='Designation', font=('times new roman', 12), bg='white')
    designation_label.grid(row=4, column=2, padx=20, pady=10, sticky='w')
    designation_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee', 'Trainer'),
                                        font=('times new roman', 12),
                                        width=18, state='readonly')
    designation_combobox.set('Select Designation ')
    designation_combobox.grid(row=4, column=3)

    salary_label = Label(detail_frame, text='Salary', font=('times new roman', 12), bg='white')
    salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')
    salary_entry = Entry(detail_frame, font=('times new roman', 12), bg='light yellow')
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    leave_approval_label = Label(detail_frame, text='Leave Approval', font=('times new roman', 12), bg='white')
    leave_approval_label.grid(row=4, column=4, padx=20, pady=10, sticky='w')

    leave_approval_combobox = ttk.Combobox(detail_frame, values=('Pending', 'Approved', 'Rejected'),
                                           font=('times new roman', 12), width=18, state='readonly')
    leave_approval_combobox.set('Select Approval Status')
    leave_approval_combobox.grid(row=4, column=5, padx=20, pady=10)

    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=520)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 12), width=10, cursor='hand2',
                        fg='white', bg='#0f4d7d',
                        command=lambda: add_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                     gender_combobox.get(), dob_date_entry.get(), contact_entry.get(),
                                                     employment_type_combobox.get(), education_combobox.get(),
                                                     work_shift_combobox.get(), address_text.get("1.0", "end-1c"),
                                                     doj_date_entry.get(), salary_entry.get(),
                                                     designation_combobox.get(),
                                                     leave_approval_combobox.get()))
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',
                           command=lambda: update_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                          gender_combobox.get(), dob_date_entry.get(),
                                                          contact_entry.get(),
                                                          employment_type_combobox.get(), education_combobox.get(),
                                                          work_shift_combobox.get(), address_text.get("1.0", "end-1c"),
                                                          doj_date_entry.get(), salary_entry.get(),
                                                          designation_combobox.get(),
                                                          leave_approval_combobox.get()))
    update_button.grid(row=0, column=1, padx=20)



    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 12), width=10, cursor='hand2',
                           fg='white', bg='#0f4d7d',  command=lambda: delete_employee(empid_entry.get(), name_entry.get(), email_entry.get(),
                                                          gender_combobox.get(), dob_date_entry.get(),
                                                          contact_entry.get(),
                                                          employment_type_combobox.get(), education_combobox.get(),
                                                          work_shift_combobox.get(), address_text.get("1.0", "end-1c"),
                                                          doj_date_entry.get(), salary_entry.get(),
                                                          designation_combobox.get(),
                                                          leave_approval_combobox.get()))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 12), width=10, cursor='hand2',
                          fg='white', bg='#0f4d7d', command=lambda: clear_fields(empid_entry, name_entry, email_entry,
                                                                                 gender_combobox, dob_date_entry,
                                                                                 contact_entry,
                                                                                 employment_type_combobox,
                                                                                 education_combobox,
                                                                                 work_shift_combobox, address_text,
                                                                                 doj_date_entry, salary_entry,
                                                                                 designation_combobox,
                                                                                 leave_approval_combobox, True))
    clear_button.grid(row=0, column=3, padx=20)

    employee_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, empid_entry, name_entry, email_entry,
                                                                          gender_combobox, dob_date_entry,
                                                                          contact_entry,
                                                                          employment_type_combobox, education_combobox,
                                                                          work_shift_combobox, address_text,
                                                                          doj_date_entry, salary_entry,
                                                                          designation_combobox,
                                                                          leave_approval_combobox))

    create_database_table()
    return employee_frame
