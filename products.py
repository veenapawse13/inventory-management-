from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pymysql

from employees import  connect_database

from employees import treeview_data


def show_all(treeview,search_combobox,search_entry):

    treeview_data(treeview)
    search_combobox.set('Search By')
    search_entry.delete(0,END)


def search_product(search_combobox, search_entry, treeview):
    selected_option = search_combobox.get()

    # Check if a valid option is selected in the combobox
    if selected_option == 'Search By':
        messagebox.showwarning('Warning', 'Please select an option')
        return

    # Check if the search entry is empty
    search_value = search_entry.get()
    if search_value == '':
        messagebox.showwarning('Warning', 'Please enter the value to search')
        return

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return  # Exit if the connection fails

    # Get selected column name and search value
    search_column = selected_option
    print(f"Selected column: {search_column}")

    # Validate the column name to ensure it is a valid column in your database
    valid_columns = ['product_id', 'product_name', 'category']  # Adjust these according to your DB schema
    if search_column not in valid_columns:
        messagebox.showerror('Error', f'Invalid column selected for search: {search_column}')

        # Close the cursor and connection here, then exit
        cursor.close()
        connection.close()
        return  # Exit after showing the error

    print(f"Search value: {search_value}")

    # Safely construct the query with the column name and parameterized search value
    query = f"SELECT * FROM product_data WHERE {search_column} = %s"
    print(f"Executing query: {query} with value {search_value}")

    try:
        # Execute query with parameterized value
        cursor.execute(query, (search_value,))
        records = cursor.fetchall()

        # Check if no records were found
        if len(records) == 0:
            messagebox.showerror('Error', 'No records found!')
            return

        # Clear the treeview and insert the new records
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)

    except pymysql.MySQLError as err:
        messagebox.showerror('Database Error', f"Error executing query: {err}")

    finally:
        # Ensure the cursor and connection are always closed
        cursor.close()
        connection.close()






def clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    treeview.selection_remove(treeview.selection())
    category_combobox.set('Select')
    supplier_combobox.set('Select')
    name_entry.delete(0,END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    status_combobox.set('Select Status')






def delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    # Get selected row index from the treeview
    index = treeview.selection()

    # If no row is selected, show an error message
    if not index:
        messagebox.showerror('ERROR', 'No row is selected')
        return

    # Get the data of the selected row
    dict_data = treeview.item(index)
    content = dict_data['values']
    id = content[0]

    # Ask for user confirmation before deleting
    ans = messagebox.askyesno('Confirm', 'DO YOU REALLY WANT TO DELETE?')

    if ans:  # Only proceed if user confirms deletion
        # Connect to the database
        cursor, connection = connect_database()
        if not cursor or not connection:
            return  # Exit if database connection failed

        try:
            # Select the database and delete the product by ID
            cursor.execute('USE inventorys_system')

            # Delete the product from the product_data table using the ID
            cursor.execute('DELETE FROM product_data WHERE id=%s', (id,))

            # Commit the transaction
            connection.commit()

            # Refresh the treeview with updated data
            treeview_data(treeview)

            # Show success message
            messagebox.showinfo('Info', 'Record is deleted')
            clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox)

        except Exception as e:
            # Show error message if something goes wrong
            messagebox.showerror('ERROR', f'Error due to: {e}')

        finally:
            # Close the cursor and connection
            cursor.close()

def update_product(category, supplier, name, price, quantity, status, treeview):
    # Get selected row index from the treeview
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected')  # Show error if no row selected
        return

    # Get the data from the selected row
    dict_data = treeview.item(index)
    content = dict_data['values']
    id = content[0]  # Assuming 'id' is the first column in the treeview

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return  # Exit if database connection failed

    try:
        # Select the database and fetch the current product data
        cursor.execute('USE inventorys_system')
        cursor.execute('SELECT * FROM product_data WHERE id=%s', (id,))
        current_data = cursor.fetchone()

        if not current_data:
            messagebox.showerror('Error', 'Product not found in the database')
            return

        # Exclude the ID field from the current data (first field in current_data)
        current_data = current_data[1:]
        current_data=list(current_data)
        current_data[3]=str(current_data)


        # Prepare the new data to update (convert numbers to strings, clean up data)
        new_data = (
            category.strip(),  # Ensure no leading/trailing spaces
            supplier.strip(),
            name.strip(),
            str(price).strip(),  # Convert price to string and clean up
            str(quantity).strip(),  # Convert quantity to string and clean up
            status.strip()  # Clean up status as well
        )
        print(f"New Data: {new_data}")

        # If no changes are detected, inform the user
        if tuple(current_data) == new_data:
            messagebox.showinfo('Info', 'No changes detected')
            return

        # Update the product data with new values
        cursor.execute(
            'UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, quantity=%s, status=%s WHERE id=%s',
            (category, supplier, name, str(price), str(quantity), status, id)
        )
        connection.commit()  # Commit the changes

        quantity=int(quantity)
        messagebox.showinfo('Info', 'Data updated successfully')

        # Refresh the treeview with updated data (function assumed)
        treeview_data(treeview)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to: {e}')

    finally:
        # Always close the cursor and connection
        cursor.close()
        connection.close()








def select_data(event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox):
    index=treeview.selection()
    dict=treeview.item(index)
    content=dict['values']
    name_entry.delete(0,END)
    price_entry.delete(0,END)
    quantity_entry.delete(0,END)

    category_combobox.set(content[1])
    supplier_combobox.set(content[2])
    name_entry.insert(0,content[3])
    price_entry.insert(0,content[4])
    quantity_entry.insert(0,content[5])
    status_combobox.set(content[6])


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventorys_system')
        cursor.execute('Select * from product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('ERROR', f'Error due to{e}')

    finally:
        cursor.close()
        connection.close()

def fetch_supplier_category(category_combobox,supplier_combobox):
    category_option=[]
    supplier_option=[]

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('use inventorys_system')
    cursor.execute('SELECT name from category_data')
    names=cursor.fetchall()
    if len(names)>0:
        category_combobox.set('Select')
        for name in names:
            category_option.append(name[0])
        category_combobox.config(values=category_option)

    cursor.execute('SELECT name from supplier_data')
    names = cursor.fetchall()
    if len(names)>0:
        supplier_combobox.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supplier_combobox.config(values=supplier_option)

def save_product(category,supplier,name,price,quantity,status,treeview):
    if category=='Empty':
        messagebox.showerror('error','Please add categories')
    elif supplier=='Empty':
        messagebox.showerror('error', 'Please add suppliers')

    elif category=='Select' or supplier=='Select' or name=='' or price=='' or quantity=='' or status=='Select Status':
        messagebox.showerror('error', 'ALL fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventorys_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100),'
                       'supplier VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2),quantity INT, status VARCHAR(50))' )
        cursor.execute('Select * from product_data WHERE category=%s AND supplier=%s AND name=%s',(category,supplier,name) )
        existing_product=cursor.fetchone()
        if existing_product:
            messagebox.showerror('error','Product already exists')
            return


        cursor.execute('INSERT INTO product_data(category,supplier,name,price,quantity,status) VALUES(%s,%s,%s,%s,%s,%s)',
                       (category,supplier,name,price,quantity,status))

        connection.commit()
        messagebox.showinfo('Success','Data is added successfully')
        treeview_data(treeview)






def product_form(window):
    global back_image
    product_frame = Frame(window, width=1070, height=567, bg='white')
    product_frame.place(x=200, y=100)

    back_image = PhotoImage(file='back.png')
    back_button = Button(product_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: product_frame.place_forget())
    back_button.place(x=10, y=0)

    left_frame = Frame(product_frame, bg='white', bd=2, relief=RIDGE)
    left_frame.place(x=20, y=30)

    headingLabel = Label(left_frame, text='MANAGE PRODUCTS DETAILS', font=('times new roman', 14, 'bold'),
                         bg='#0f4d7d', fg='white')
    headingLabel.grid(row=0, columnspan=2, sticky='we')

    category_label = Label(left_frame, text='Category', font=('times new roman', 14, 'bold'), bg='white')
    category_label.grid(row=1, column=0, padx=20, sticky='w')
    category_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
    category_combobox.grid(row=1, column=1, pady=40)
    category_combobox.set('Empty')

    supplier_label = Label(left_frame, text='Supplier', font=('times new roman', 14, 'bold'), bg='white')
    supplier_label.grid(row=2, column=0, padx=20, sticky='w')
    supplier_combobox = ttk.Combobox(left_frame, font=('times new roman', 14, 'bold'), width=18, state='readonly')
    supplier_combobox.grid(row=2, column=1)
    supplier_combobox.set('Empty')

    name_label = Label(left_frame, text='Name', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=3, column=0, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    name_entry.grid(row=3, column=1, pady=40)

    price_label = Label(left_frame, text='Price', font=('times new roman', 14, 'bold'), bg='white')
    price_label.grid(row=4, column=0, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    price_entry.grid(row=4, column=1)

    quantity_label = Label(left_frame, text='Quantity', font=('times new roman', 14, 'bold'), bg='white')
    quantity_label.grid(row=5, column=0, padx=20, sticky='w')
    quantity_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='light yellow')
    quantity_entry.grid(row=5, column=1, pady=40)

    status_label = Label(left_frame, text='Status', font=('times new roman', 14, 'bold'), bg='white')
    status_label.grid(row=6, column=0, padx=20, sticky='w')
    status_combobox = ttk.Combobox(left_frame, values=('Active', 'Inactive', 'Pending'),
                                   font=('times new roman', 14, 'bold'), width=18, state='readonly')
    status_combobox.grid(row=6, column=1)
    status_combobox.set('Select Status')

    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=7, columnspan=2, pady=(30, 10))

    save_button = Button(button_frame, text='SAVE', font=('times new roman', 14), width=8, cursor='hand2',
                         fg='white', bg='#0f4d7d',command=lambda :save_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    save_button.grid(row=0, column=0, padx=10)

    update_button = Button(button_frame, text='UPDATE', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda :update_product(category_combobox.get(),supplier_combobox.get(),name_entry.get(),price_entry.get(),quantity_entry.get(),status_combobox.get(),treeview))
    update_button.grid(row=0, column=1, padx=10)

    delete_button = Button(button_frame, text='DELETE', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda :delete_product(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    delete_button.grid(row=0, column=2, padx=10)

    clear_button = Button(button_frame, text='CLEAR', font=('times new roman', 14), width=8, cursor='hand2',
                          fg='white', bg='#0f4d7d',command=lambda: clear_fields(treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))
    clear_button.grid(row=0, column=3, padx=10)

    search_frame = LabelFrame(product_frame, text='Search Product', font=('times new roman', 14), width=8,
                              cursor='hand2',bg='white'
                        )
    search_frame.place(x=480, y=30)

    search_combobox = ttk.Combobox(search_frame, values=('Category', 'Supplier', 'Name', 'Status'), state='readonly',
                                   width=16, font=('times new roman', 14))
    search_combobox.grid(row=0, column=0,padx=10)
    search_combobox.set('Search By')

    search_entry = Entry(search_frame, font=('times new roman', 14, 'bold'), bg='light yellow',width=16)
    search_entry.grid(row=0, column=1)

    search_button = Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2',
                           fg='white', bg='#0f4d7d',command=lambda :search_product(search_combobox,search_entry,treeview))
    search_button.grid(row=0, column=2, padx=(10,0),pady=10)


    show_button = Button(search_frame, text='Show ALL', font=('times new roman', 14), width=8, cursor='hand2',
                         fg='white', bg='#0f4d7d')
    show_button.grid(row=0, column=3,padx=10)

    treeview_frame=Frame(product_frame)
    treeview_frame.place(x=480,y=125,width=570,height=410)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('id','category','supplier','name','price','quantity','status'), show='headings',
                            yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading('id', text='ID')
    treeview.heading('category', text='Category')
    treeview.heading('supplier', text='Supplier')
    treeview.heading('name', text='Name')
    treeview.heading('price', text='Price')
    treeview.heading('quantity', text='Quantity')
    treeview.heading('status', text='Status')
    fetch_supplier_category(category_combobox,supplier_combobox)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event:select_data(event,treeview,category_combobox,supplier_combobox,name_entry,price_entry,quantity_entry,status_combobox))


    return product_frame