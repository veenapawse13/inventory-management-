
from tkinter import *

from django.db import connection

from employees import connect_database, employee_form
from  supplier import  supplier_form
from  category import  category_form
from products import  product_form


from tkinter import messagebox
import time




def update():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventorys_system')
    cursor.execute('SELECT * from employee_data')
    emp_records=cursor.fetchall()
    total_emp_count_label.config(text=len(emp_records))

    cursor.execute('SELECT * from supplier_data')
    sup_records = cursor.fetchall()
    total_sup_count_label.config(text=len(sup_records))

    cursor.execute('SELECT * from category_data')
    cat_records = cursor.fetchall()
    total_cat_count_label.config(text=len(cat_records))


    cursor.execute('SELECT * from product_data')
    prod_records = cursor.fetchall()
    total_prod_count_label.config(text=len(prod_records))


   


    date_time = time.strftime('%I:%M:%S %p on %A, %B %d/%m/%Y')

    subtitleLabel.config(text=f'Welcome Admin\t\t\t {date_time}')

    # Call update again after 1000ms (1 second)
    subtitleLabel.after(1000, update)





current_frame=None
def show_form(form_function):
    global  current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)



from unicodedata import category

# GUI part
window = Tk()

window.title('Dashboard')
window.geometry('1270x668+0+0')
window.resizable(0, 0)
window.config(bg='white')

bg_image = PhotoImage(file='inventory.png')
titlelabel = Label(window, image=bg_image, compound=LEFT, text='Inventory Management System',
                   font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
titlelabel.place(x=0, y=0, relwidth=1)

logoutButton = Button(window, text='Login', font=('times new roman', 20, 'bold'), fg='#010c48',)
logoutButton.place(x=1100, y=10)

subtitleLabel = Label(window, text='Welcome Admin\t\t Date:22-02-2025\t\t Time: 12:36:17 pm',
                      font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=0, y=102, width=200, height=555)

logoImage = PhotoImage(file='logo.png')
imageLabel = Label(leftFrame, image=logoImage)
imageLabel.pack()

menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
menuLabel.pack(fill=X)

employee_icon = PhotoImage(file='employee.png')
employee_button = Button(leftFrame, image=employee_icon, compound=LEFT, text='EMPLOYEES',
                         font=('times new roman', 19, 'bold'), anchor='c', padx=5, command=lambda :show_form(employee_form))
employee_button.pack(fill=X)

supplier_icon = PhotoImage(file='supplier.png')
supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT, text='SUPPLIER',
                         font=('times new roman', 20, 'bold'), anchor='w', padx=10,command=lambda: show_form(supplier_form))
supplier_button.pack(fill=X)

category_icon = PhotoImage(file='category.png')
category_button = Button(leftFrame, image=category_icon, compound=LEFT, text='CATEGORY',
                         font=('times new roman', 20, 'bold'), anchor='c', padx=10,command=lambda :show_form(category_form))
category_button.pack(fill=X)

products_icon = PhotoImage(file='product.png')
products_button = Button(leftFrame, image=products_icon, compound=LEFT, text='PRODUCTS',
                         font=('times new roman', 19, 'bold'), anchor='w', padx=10,command=lambda :show_form(product_form))
products_button.pack(fill=X)

sales_icon = PhotoImage(file='sales.png')
sales_button = Button(leftFrame, image=sales_icon, compound=LEFT, text='SALES', font=('times new roman', 20, 'bold'),
                      anchor='w', padx=10)
sales_button.pack(fill=X)

exit_icon = PhotoImage(file='exit.png')
exit_button = Button(leftFrame, image=exit_icon, compound=LEFT, text='EXIT', font=('times new roman', 20, 'bold'),
                     anchor='w', padx=10)
exit_button.pack(fill=X)

emp_frame = Frame(window, bg='#2C3E50', bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon = PhotoImage(file='total_emp.png')
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg='#2C3E50')
total_emp_icon_label.pack()
total_emp_label = Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white',
                        font=('times new roman', 15, 'bold'))
total_emp_label.pack()
total_emp_count_label = Label(emp_frame, text='0', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold'))
total_emp_count_label.pack()

sup_frame = Frame(window, bg='#8E44AD', bd=3, relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon = PhotoImage(file='total_sup.png')
total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg='#8E44AD')
total_sup_icon_label.pack()
total_sup_label = Label(sup_frame, text='Total Suppliers', bg='#8E44AD', fg='white',
                        font=('times new roman', 15, 'bold'))
total_sup_label.pack()
total_sup_count_label = Label(sup_frame, text='0', bg='#8E44AD', fg='white', font=('times new roman', 30, 'bold'))
total_sup_count_label.pack()

cat_frame = Frame(window, bg='#AE2727', bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)
total_cat_icon = PhotoImage(file='total_cat.png')
total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg='#AE2727')
total_cat_icon_label.pack()
total_cat_label = Label(cat_frame, text='Total Categories', bg='#AE2727', fg='white',
                        font=('times new roman', 15, 'bold'))
total_cat_label.pack()
total_cat_count_label = Label(cat_frame, text='0', bg='#AE2727', fg='white', font=('times new roman', 30, 'bold'))
total_cat_count_label.pack()

prod_frame = Frame(window, bg='#2ECCC0', bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon = PhotoImage(file='total_prod.png')
total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg='#2ECCC0')
total_prod_icon_label.pack()
total_prod_label = Label(prod_frame, text='Total Products', bg='#2ECCC0', fg='white',
                         font=('times new roman', 15, 'bold'))
total_prod_label.pack()
total_prod_count_label = Label(prod_frame, text='0', bg='#2ECCC0', fg='white', font=('times new roman', 30, 'bold'))
total_prod_count_label.pack()


sales_frame = Frame(window, bg='#208e4e', bd=3, relief=RIDGE)
sales_frame.place(x=600, y=495, height=170, width=280)
total_sales_icon = PhotoImage(file='total_sales.png')
total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg='#208e4e')
total_sales_icon_label.pack()
total_sales_label = Label(sales_frame, text='Total Sales', bg='#208e4e', fg='white',
                  font=('times new roman', 15, 'bold'))
total_sales_label.pack()
total_sales_count_label = Label(sales_frame, text='0', bg='#208e4e', fg='white', font=('times new roman', 30, 'bold'))


update()
window.mainloop()
