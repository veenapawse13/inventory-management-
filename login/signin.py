from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

#functionality part---------


def login_user():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showerror('Error','Password do not match')
    else:
        try:
            con=pymysql.connect(host='localhost', user='root',password='root12345')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again')
            return
        query='use userdat'
        mycursor.execute(query)
        query='select * from data where username=%s and password=%s'
        mycursor.execute(query,(usernameEntry.get(),passwordEntry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid username or password')
        else:
            messagebox.showinfo('Welcome','Login is Sucessful')


        
def forget_password():
    def change_password():
        if user_Entry.get()=='' or newpass_Entry.get()=='' or confirmpass_Entry.get()=='':
            messagebox.showerror('Error','All Fields Are Requiered',parent=window)
        elif newpass_Entry.get()!=confirmpass_Entry.get():
            messagebox.showerror('Error','Password and Confirm Password are not matching',parent=window)
        else:
            con=pymysql.connect(host='localhost', user='root',password='root12345',database='userdat')
            mycursor=con.cursor()
            query='select * from data where username=%s '
            mycursor.execute(query, (user_Entry.get()))
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Incorrect username',parent=window)
            else:
                query='update data set password=%s where username=%s'
                mycursor.execute(query,(newpass_Entry.get(),user_Entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Error','Password is reset,Please Login with new Password',parent=window)
                window.destroy()

    window = Toplevel()
    window.title('Change Password')
    bgPic = ImageTk.PhotoImage(file='background (2).jpg')
    bglabel = Label(window, image=bgPic)
    bglabel.grid()

    heading_label = Label(window, text='RESET PASSWORD', font=('arial','18', 'bold'),
                          bg='white', fg='magenta2')
    heading_label.place(x=480, y=60)

    userLabel=Label(window,text='Username',font=('Microsoft Yahei UI Leight', 12, 'bold'),
                 bg='white',fg='orchid1')
    userLabel.place(x=470,y=130)
    user_Entry=Entry(window,width=25,fg='magenta2',font=('arial', 11, 'bold'),bd=0)
    user_Entry.place(x=470,y=160) 

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=180)


    passwordLabel=Label(window,text='New Password',font=('Microsoft Yahei UI Leight', 12, 'bold'),
                 bg='white',fg='orchid1')
    passwordLabel.place(x=470,y=210)

    newpass_Entry=Entry(window,width=25,fg='magenta2',font=('arial', 11, 'bold'),bd=0)
    newpass_Entry.place(x=470,y=240) 

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)


    passwordLabel=Label(window,text='New Password',font=('Microsoft Yahei UI Leight', 12, 'bold'),
                 bg='white',fg='orchid1')
    passwordLabel.place(x=470,y=210)

    newpass_Entry=Entry(window,width=25,fg='magenta2',font=('arial', 11, 'bold'),bd=0)
    newpass_Entry.place(x=470,y=240) 

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=260)



    confirmpassLabel=Label(window,text='Confirm Password',font=('Microsoft Yahei UI Leight', 12, 'bold'),
                 bg='white',fg='orchid1')
    confirmpassLabel.place(x=470,y=290)

    confirmpass_Entry=Entry(window,width=25,fg='magenta2',font=('arial', 11, 'bold'),bd=0)
    confirmpass_Entry.place(x=470,y=320) 

    Frame(window, width=250, height=2, bg='orchid1').place(x=470, y=340)

    submitButton = Button(window, text='Submit', bd=0, bg='magenta2', fg='white', font=('Open Sans', '16', 'bold'),
                          width=19,cursor='hand2', activebackground='magenta2',activeforeground='white',command=change_password)
    submitButton.place(x=470,y=390)


    window.mainloop()

def user_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)

def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0,END)

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)


def signup_page():
    login_window.destroy()
    import signup



login_window=Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0,0)
login_window.title('LOGIN PAGE')


bgImage=ImageTk.PhotoImage(file='bg.jpg')
bgLabel=Label(login_window,image=bgImage)
bgLabel.place(x=0,y=0)


heading=Label(login_window,text='USER LOGIN',font=('times new roman',23,'bold')
              ,bg='white',fg='blue4')
heading.place(x=605,y=120)

usernameEntry=Entry(login_window,width=25,font=('times new roman',11,'bold'),bd=0,fg='blue4')
usernameEntry.place(x=580,y=200)
usernameEntry.insert(0,'Username')
usernameEntry.bind('<FocusIn>',user_enter)


frame1=Frame(login_window,width=250,height=2,bg='blue4')
frame1.place(x=580,y=222)

passwordEntry=Entry(login_window,width=25,font=('times new roman',11,'bold'),bd=0,fg='blue4')
passwordEntry.place(x=580,y=260)
passwordEntry.insert(0,'Password')
passwordEntry.bind('<FocusIn>',password_enter)

frame2=Frame(login_window,width=250,height=2,bg='blue4')
frame2.place(x=580,y=282)
openeye=PhotoImage(file='openeye.png')
eyeButton=Button(login_window,image=openeye,bd=0,bg='white',activebackground='white'
                 ,cursor='hand2',command=hide)
eyeButton.place(x=800,y=255)


forgetButton=Button(login_window,text='Forgot Password?',bd=0,bg='white',activebackground='white'
                 ,cursor='hand2',font=('times new roman',11,'bold')
                    ,fg='blue4',activeforeground='blue4',command=forget_password)
forgetButton.place(x=715,y=295)


loginButton=Button(login_window,text='LOGIN',font=('times new roman',16,'bold'),
                   fg='white',bg='firebrick1',activeforeground='white',activebackground='firebrick1'
                   ,cursor='hand2',bd=0,width=19,command=login_user)
loginButton.place(x=578,y=350)

orLabel=Label(login_window,text='--------------OR--------------',font=('times new roman',16,'bold'),fg='blue4',bg='white')
orLabel.place(x=583,y=400)

facebook_logo=PhotoImage(file='facebook (2).png')
fbLabel=Label(login_window,image=facebook_logo,bg='white')
fbLabel.place(x=640,y=440)

google_logo=PhotoImage(file='google (1).png')
googleLabel=Label(login_window,image=google_logo,bg='white')
googleLabel.place(x=690,y=440)

twitter_logo=PhotoImage(file='twitter (2).png')
twitterLabel=Label(login_window,image=twitter_logo,bg='white')
twitterLabel.place(x=740,y=440)

signupLabel=Label(login_window,text='Dont have an account?',font=('times new roman',9,'bold'),fg='blue4',bg='white')
signupLabel.place(x=590,y=500)

newaccountButton=Button(login_window,text='Create new account',font=('times new roman',9,'bold underline'),
                   fg='blue',bg='white',activeforeground='white',activebackground='blue'
                   ,cursor='hand2',bd=0,command=signup_page)
newaccountButton.place(x=715,y=500)


login_window.mainloop()