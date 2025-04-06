from os.path import exists
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from django.db import connection

from employees import connect_database, treeview_data, select_data


def search_supplier(search_value, treeview):
    # Check if the search value is empty
    if search_value == '':
        messagebox.showerror('Error', 'Please enter invoice no.')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventorys_system')

        # Make sure to pass search_value as a tuple
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (search_value,))

        record = cursor.fetchone()
        if not record:
            messagebox.showerror('Error', 'No record found')
            return

        # Clear the treeview and insert the found record
        treeview.delete(*treeview.get_children())
        treeview.insert('', 'end', values=record)

    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror('ERROR', f'Error due to: {e}')

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def show_all(treeview, search_entry):
    # Refresh the treeview with all data
    treeview_data(treeview)

    # Clear the search entry field
    search_entry.delete(0, 'end')


def clear_selection(invoice_entry,name_entry,contact_entry,description_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())



    messagebox.showinfo('Info', 'Selection cleared')



def delete_supplier(invoice, treeview):

    index = treeview.selection()
    if not index:
        messagebox.showerror('ERROR', 'No row is selected')
        return

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        # Use the correct database
        cursor.execute('USE inventorys_system')

        # Correct the DELETE query: remove the * and ensure it's valid
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s', (invoice,))  # Tuple with one element

        # Commit the transaction
        connection.commit()

        # Refresh the treeview data
        treeview_data(treeview)

        # Show success message
        messagebox.showinfo('Info', 'Record is deleted')

    except Exception as e:
        # Show error message if something goes wrong
        messagebox.showerror('ERROR', f'Error due to: {e}')

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def update_supplier(invoice,name,contact,description,treeview):
    index= treeview.selection()
    if not index:
        messagebox.showerror('ERROR''NO row is selected')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventorys_system')
        cursor.execute('SELECT * from supplier_data WHERE invoice=%s',invoice)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        print(current_data)

        new_data=(name,contact,description)
        print(new_data)

        if current_data==new_data:
            messagebox.showinfo('INFO','NO changes detected')
            return


        cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,description=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('INFO','Data is updated')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('ERROR', f'Error due to{e}')

    finally:
        cursor.close()
        connection.close()



def select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview):

    index = treeview.selection()
    content=treeview.item(index)
    actual_content=content['values']
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)

    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])







def treeview_data (treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventorys_system')
        cursor.execute('Select * from supplier_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
    except Exception as e:
        messagebox.showerror('ERROR', f'Error due to{e}')

    finally:
        cursor.close()
        connection.close()



def add_supplier(invoice,name,contact,description,treeview):
    if invoice=='' or name=='' or contact=='' or description=='':
        messagebox.showerror('Error','All fields are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('use inventorys_system')

            cursor.execute(
                'CREATE TABLE IF NOT EXISTS supplier_data (invoice INT PRIMARY KEY,name VARCHAR(100), contact VARCHAR(15),description TEXT)')
            cursor.execute('SELECT * from supplier_data WHERE invoice=%s', invoice)
            if cursor.fetchone():
                messagebox.showerror('ERROR', 'Invoice-NO is already exists')
                return

            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)',(invoice,name,contact,description))
            connection.commit()
            messagebox.showinfo('INFO','Data is inserted')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('ERROR',f'Error due to{e}')
        finally:
            cursor.close()
            connection.close()




def supplier_form(window):
    global back_image
    supplier_frame = Frame(window, width=1070, height=567, bg='white')
    supplier_frame.place(x=200, y=100)
    headingLabel = Label(supplier_frame, text='MANAGE SUPPLIER DETAILS', font=('times new roman', 16, 'bold'),
                         bg='#0f4d7d', fg='white')
    headingLabel.place(x=0, y=0, relwidth=1)
    back_image = PhotoImage(file='back.png')
    back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)

    left_Frame=Frame(supplier_frame,bg='white')
    left_Frame.place(x=10,y=100)

    invoice_label=Label(left_Frame,text='Invoice NO.',font=('times new roman',14,'bold'),bg='white')
    invoice_label.grid(row=0,column=0,padx=(20,40),sticky='w')
    invoice_entry=Entry(left_Frame,font=('times new roman',14,'bold'),bg='light yellow')
    invoice_entry.grid(row=0,column=1)

    name_label = Label(left_Frame, text='Supplier Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=1, column=0, padx=(20,40),pady=20,sticky='w')
    name_entry = Entry(left_Frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    name_entry.grid(row=1, column=1)

    contact_label = Label(left_Frame, text=' Supplier Contact', font=('times new roman', 14, 'bold'), bg='white')
    contact_label.grid(row=2, column=0, padx=(20,40),sticky='w')
    contact_entry = Entry(left_Frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    contact_entry.grid(row=2, column=1)

    description_label = Label(left_Frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=3, column=0, padx=(20,40),sticky='w',pady=25)
    description_text=Text(left_Frame,width=25,height=6,bd=2,bg='light yellow')
    description_text.grid(row=3,column=1,pady=25)

    button_frame=Frame(left_Frame,bg='white')
    button_frame.grid(row=4,columnspan=2,pady=20)

    add_button = Button(button_frame, text='ADD', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda :add_supplier(invoice_entry.get(),name_entry.get(),
                                                                                 contact_entry.get(),description_text.get(1.0,END).strip(),treeview) )
    add_button.grid(row=0, column=0, padx=20)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 14), width=8, cursor='hand2',
                        fg='white', bg='#0f4d7d',command=lambda :update_supplier(invoice_entry.get(),name_entry.get(),
                                                                                 contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0, column=1)

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14), width=8, cursor='hand2',
                        fg='white', bg='#0f4d7d',command=lambda :delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0, column=2, padx=20)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14), width=8, cursor='hand2',
                        fg='white', bg='#0f4d7d',command=lambda: clear_selection(invoice_entry,name_entry,contact_entry,description_text,treeview))


    clear_button.grid(row=0, column=3)



    right_frame=Frame(supplier_frame,bg='white')
    right_frame.place(x=520,y=95,width=500,height=345)

    search_frame=Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,20))

    num_label=Label(search_frame,text='Invoice NO.',font=('times new roman',14,'bold'),bg='white')
    num_label.grid(row=0,column=0,padx=(0,15),sticky='w')
    search_entry=Entry(search_frame,font=('times new roman',14,'bold'),bg='light yellow',width=12)
    search_entry.grid(row=0,column=1)

    search_button = Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2',
                          fg='white', bg='#0f4d7d',command=lambda :search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0, column=2,padx=15)
    show_button = Button(search_frame, text='Show', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda : show_all(treeview,search_entry))
    show_button.grid(row=0, column=3)



    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx = Scrollbar(right_frame, orient=HORIZONTAL)
    treeview=ttk.Treeview(right_frame,columns=('invoice','name','contact','description'),show='headings',
                          yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)

    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('invoice',text='Invoice ID')
    treeview.heading('name',text='Supplier Name')
    treeview.heading('contact',text='Contact')
    treeview.heading('description', text='Description')

    treeview.column('invoice',width=80)
    treeview.column('name',width=140)
    treeview.column('contact',width=120)
    treeview.column('description',width=300)

    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',
                       lambda event: select_data(event, invoice_entry, name_entry, contact_entry, description_text,
                                                 treeview))

    return supplier_frame















