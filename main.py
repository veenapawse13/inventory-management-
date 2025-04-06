import tempfile
from tkinter import *
from tkinter import messagebox
import  random
import random,os,smtplib

#Functionality part---------
def send_email():
    def send_gmail():
         try:
             ob = smtplib.SMTP('smtp.gmail.com', 587)
             ob.starttls()
             ob.login(senderEntry.get(), phoneEntry.get())
             message = email_textarea.get(1.0, END)
             ob.sendmail(senderEntry.get(), receieverEntry.get(), message)
             ob.quit()
             messagebox.showinfo('SUCCESS', 'BILL Successfully generated')
         except:
             messagebox.showerror('ERROR','Something went wrong')


    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('ERROR','BILL IS EMPTY')
    else:
        window1 = Toplevel()
        window1.title('send gmail')
        window1.config(bg='gray20')
        window1.resizable(0, 0)

        senderFrame = LabelFrame(window1, text='SENDER', font=('arial', 16, 'bold'), bd=6, bg='gray20', fg='white')
        senderFrame.grid(row=0, column=0, padx=40, pady=20)

        gmailIDLabel = Label(senderFrame, text="Sender's Email", font=('arial', 14, 'bold'), bd=6, bg='gray20',
                             fg='white')
        gmailIDLabel.grid(row=0, column=0, padx=10, pady=8)

        senderEntry = Entry(senderFrame, font=('arial', 16, 'bold'), width=23, relief=RIDGE, fg='white')
        senderEntry.grid(row=0, column=1, padx=10, pady=8)

        passwordLabel = Label(senderFrame, text="Password", font=('arial', 14, 'bold'), bd=6, bg='gray20', fg='white')
        passwordLabel.grid(row=1, column=0, padx=10, pady=8)

        passwordEntry = Entry(senderFrame, font=('arial', 16, 'bold'), width=23, relief=RIDGE, fg='white',show='*')
        passwordEntry.grid(row=1, column=1, padx=10, pady=8)

        # Recipient Frame
        recipientFrame = LabelFrame(window1, text='RECIPIENT', font=('arial', 16, 'bold'), bd=6, bg='gray20',
                                    fg='white')
        recipientFrame.grid(row=1, column=0, padx=40, pady=20)

        # Receiver Label
        receieverLabel = Label(recipientFrame, text="Email Address", font=('arial', 14, 'bold'), bd=6, bg='gray20',
                               fg='white')
        receieverLabel.grid(row=0, column=0, padx=10, pady=8)

        # Receiver Entry
        receieverEntry = Entry(recipientFrame, font=('arial', 16, 'bold'), width=23, relief=RIDGE, fg='white')
        receieverEntry.grid(row=0, column=1, padx=10, pady=8)

        # Message Label
        messageLabel = Label(recipientFrame, text="MESSAGE", font=('arial', 14, 'bold'), bd=6, bg='gray20', fg='white')
        messageLabel.grid(row=1, column=0, padx=10, pady=8)

        # Scrollbar for the Text Area
        scrollbar = Scrollbar(recipientFrame)
        scrollbar.grid(row=2, column=2, sticky='ns', pady=8)

        # Email Textarea with Scrollbar
        email_textarea = Text(recipientFrame, font=('arial', 14, 'bold'), bd=2, relief=SUNKEN, width=42, height=10,
                              yscrollcommand=scrollbar.set)
        email_textarea.grid(row=2, column=0, columnspan=2, padx=10, pady=8)

        # Link the scrollbar to the Text widget
        scrollbar.config(command=email_textarea.yview)

        # Clear the textarea and insert content if needed
        email_textarea.delete(1.0, END)
        # Assuming you want to copy content from another Text widget (for example, 'textarea' widget),
        # make sure 'textarea' is defined somewhere in your code, e.g.,
        # textarea = Text(window1, height=10, width=30)
        # And make sure to use correct reference:
        # email_textarea.insert(END, textarea.get(1.0, END))



        # Copy text from 'textarea' to 'email_textarea' if desired
        email_textarea.insert(END, textarea.get(1.0, END).replace('\t\t\t','\t\t'))

        # Send Button
        sendButton = Button(window1, text='SEND', font=('arial', 16, 'bold'), width=15,command=send_gmail)
        sendButton.grid(row=3, column=0, pady=20)

        window1.mainloop()




def print_bill():
    if textarea.get(1.0,END)=='\n':
        messagebox.showerror('ERROR','BILL IS EMPTY')
    else:
        file=tempfile.mktemp('.txt')
        open(file,'w').write(textarea.get(1.0,END))
        os.startfile(file,'print')


def search_bill():
    for i in os.listdir('bills/'):
        if i.split('.')[0]==billEntry.get():
            f=open(f'bills/{i}','r')
            textarea.delete(1.0,END)
            for data in f:
                textarea.insert(END,data)
            f.close()
            break
    else:
        messagebox.showerror('ERROR','Invalid Bill Number ')








if not os.path.exists('bills'):
    os.mkdir('bills')





def save_bill():
    global billnumber
    result=messagebox.askyesno('Confirm','DO you want to save the BILL?')
    if result:
        bill_content=textarea.get(1.0,END)
        file=open(f'bills/{billnumber}.txt','w')
        file.write(bill_content)
        file.close()
        messagebox.showinfo('SUCCESS',f'bill number {billnumber} IS saved Successfully')
        billnumber = random.randint(500, 1000)



billnumber=random.randint(500,1000)
def bill_area():
    if nameEntry.get()==''or phoneEntry.get()=='':
        messagebox.showerror('Error','Customer Details are Required!')
    elif cosmeticpriceEntry.get()=='' and GrocerypriceEntry.get()=='' and DrinkspriceEntry.get()=='':
        messagebox.showerror('Error', 'NO Products are selected!!')
    elif cosmeticpriceEntry.get()=='0 Rs' and GrocerypriceEntry.get()=='0 Rs' and DrinkspriceEntry.get()=='0 Rs':
        messagebox.showerror('Error', 'NO Products are selected!!')
    else:
        textarea.delete(1.0, END)
        textarea.insert(END, '\t\t**WELCOME CUSTOMER**\n')
        textarea.insert(END, f'\nBill Number: {billnumber}')
        textarea.insert(END, f'\nCustomer Name: {nameEntry.get()}')
        textarea.insert(END, f'\nCustomer phone Number: {phoneEntry.get()}')
        textarea.insert(END, '\n==================================================')
        textarea.insert(END, 'Product\t\tQuantity\t\tPrice')
        textarea.insert(END, '\n==================================================')
        if BathsoapEntry.get() != '0':
            textarea.insert(END, f'\nBath Soap\t\t{BathsoapEntry.get()}\t\t{soapprice} Rs')

        if facecreamEntry.get() != '0':
            textarea.insert(END, f'\nFace cream\t\t{facecreamEntry.get()}\t\t{facecreamprice} Rs')

        if facewashEntry.get() != '0':
            textarea.insert(END, f'\nFace Wash\t\t{facewashEntry.get()}\t\t{facewashprice} Rs')

        if hairsparyEntry.get() != '0':
            textarea.insert(END, f'\nHair Spary\t\t{hairsparyEntry.get()}\t\t{hairsparyprice} Rs')

        if hairgelEntry.get() != '0':
            textarea.insert(END, f'\nHair Gel\t\t{hairgelEntry.get()}\t\t{hairgelprice} Rs')

        if RiceEntry.get() != '0':
            textarea.insert(END, f'\nRice\t\t{RiceEntry.get()}\t\t{Riceprice} Rs')

        if DaalEntry.get() != '0':
            textarea.insert(END, f'\nDaal\t\t{DaalEntry.get()}\t\t{daalprice} Rs')

        if OilEntry.get() != '0':
            textarea.insert(END, f'\nOil\t\t{OilEntry.get()}\t\t{oilprice} Rs')

        if SpicesEntry.get() != '0':
            textarea.insert(END, f'\nSpices\t\t{SpicesEntry.get()}\t\t{Spicesprice} Rs')

        if SugarEntry.get() != '0':
            textarea.insert(END, f'\nSugar\t\t{SugarEntry.get()}\t\t{Sugarprice} Rs')

        if WheatEntry.get() != '0':
            textarea.insert(END, f'\nWheat\t\t{WheatEntry.get()}\t\t{Wheatprice} Rs')

        if MaazaEntry.get() != '0':
            textarea.insert(END, f'\nMaaza\t\t{MaazaEntry.get()}\t\t{Maazprice} Rs')

        if PepsiEntry.get() != '0':
            textarea.insert(END, f'\nPepsi\t\t{PepsiEntry.get()}\t\t{Pepsiprice} Rs')

        if SpriteEntry.get() != '0':
            textarea.insert(END, f'\nSprite\t\t{SpriteEntry.get()}\t\t{Spriteprice} Rs')

        if LimcaEntry.get() != '0':
            textarea.insert(END, f'\nLimcas\t\t{LimcaEntry.get()}\t\t{Limcasprice} Rs')

        if FrootiEntry.get() != '0':
            textarea.insert(END, f'\nFrooti\t\t{FrootiEntry.get()}\t\t{Frootiprice} Rs')

        if CocoEntry.get() != '0':
            textarea.insert(END, f'\nCoco\t\t{CocoEntry.get()}\t\t{Cocoprice} Rs')

        textarea.insert(END, '\n==================================================')

        if cosmeticTaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nCosmetic Tax\t\t\t\t{cosmeticTaxEntry.get()}')

        if GroceryTaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nGrocery Tax\t\t\t\t{GroceryTaxEntry.get()}')

        if DrinkTaxEntry.get() != '0.0 Rs':
            textarea.insert(END, f'\nDrinks Tax\t\t\t\t{DrinkTaxEntry.get()}')

        textarea.insert(END, f'\n\n Total-Bill\t\t\t\t{totalbill}')
        textarea.insert(END, '\n==================================================')
        save_bill()


































def total():
    global soapprice,facecreamprice,facewashprice,hairsparyprice,hairgelprice,Bodylotionprice
    global Riceprice,daalprice,oilprice,Spicesprice,Sugarprice,Wheatprice
    global Maazprice,Pepsiprice,Spriteprice, Limcasprice ,Frootiprice, Cocoprice
    global  totalbill


    # Cosmetic price calculations
    soapprice = int(BathsoapEntry.get()) * 20
    facecreamprice = int(facecreamEntry.get()) * 50
    facewashprice = int(facewashEntry.get()) * 100
    hairsparyprice = int(hairsparyEntry.get()) * 150
    hairgelprice = int(hairgelEntry.get()) * 80
    Bodylotionprice = int(BodylotionEntry.get()) * 60

    # Calculate the total cosmetic price by adding individual item prices
    totalcosmeticprice = soapprice + facecreamprice + facewashprice + hairsparyprice + hairgelprice + Bodylotionprice
    cosmeticpriceEntry.delete(0, END)
    cosmeticpriceEntry.insert(0, f'{totalcosmeticprice} Rs')

    # Cosmetic tax calculation (12%)
    cosmeticTax = totalcosmeticprice * 0.12
    cosmeticTaxEntry.delete(0, END)
    cosmeticTaxEntry.insert(0, f'{cosmeticTax} Rs')

    # Grocery price calculations
    Riceprice = int(RiceEntry.get()) * 30
    daalprice = int(DaalEntry.get()) * 100
    oilprice = int(OilEntry.get()) * 120
    Spicesprice = int(SpicesEntry.get()) * 50
    Sugarprice = int(SugarEntry.get()) * 140
    Wheatprice = int(WheatEntry.get()) * 80

    # Calculate the total grocery price by adding individual item prices
    totalgroceryprice = Riceprice + daalprice + oilprice + Spicesprice + Sugarprice + Wheatprice
    GrocerypriceEntry.delete(0, END)
    GrocerypriceEntry.insert(0, f'{totalgroceryprice} Rs')

    # Grocery tax calculation (5%)
    Grocerytax = totalgroceryprice * 0.05
    GroceryTaxEntry.delete(0, END)
    GroceryTaxEntry.insert(0, f'{Grocerytax} Rs')

    # Drinks price calculations
    Maazprice = int(MaazaEntry.get()) * 30
    Pepsiprice = int(PepsiEntry.get()) * 100
    Spriteprice = int(SpriteEntry.get()) * 120
    Limcasprice = int(LimcaEntry.get()) * 50
    Frootiprice = int(FrootiEntry.get()) * 140
    Cocoprice = int(CocoEntry.get()) * 80

    # Calculate the total drinks price by adding individual item prices
    totaldrinksprice = Maazprice + Pepsiprice + Spriteprice + Limcasprice + Frootiprice + Cocoprice
    DrinkspriceEntry.delete(0, END)
    DrinkspriceEntry.insert(0, f'{totaldrinksprice} Rs')

    # Drinks tax calculation (5%)
    DrinkTax = totaldrinksprice * 0.07
    DrinkTaxEntry.delete(0, END)
    DrinkTaxEntry.insert(0, f'{DrinkTax} Rs')

    totalbill=totalcosmeticprice+totalgroceryprice+totaldrinksprice+cosmeticTax+Grocerytax+DrinkTax












#GUI part
#def retail():
window=Tk()
window.title('Retail Billing System')
window.geometry('1270x685')

headingLabel=Label(window,text='Retail Billing System',font=('times new roman',30,'bold')
                   ,bg='gray20',fg='gold',bd=12,relief=GROOVE)
headingLabel.pack(fill=X)

customer_details_frame=LabelFrame(window,text='Customer Details',font=('times new roman',15,'bold')
                                  , fg='gold', bd=12, relief=GROOVE,bg='gray20' )
customer_details_frame.pack(fill=X)

nameLabel=Label(customer_details_frame,text='Name',font=('times new roman',15,'bold'),bg='gray20',fg='white')
nameLabel.grid(row=0,column=0,padx=20)

nameEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
nameEntry.grid(row=0,column=1,padx=8)


phoneLabel=Label(customer_details_frame,text='Phone Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
phoneLabel.grid(row=0,column=2,padx=20,pady=2)
phoneEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
phoneEntry.grid(row=0,column=3,padx=8)

billLabel=Label(customer_details_frame,text='Bill Number',font=('times new roman',15,'bold'),bg='gray20',fg='white')
billLabel.grid(row=0,column=4,padx=20,pady=2)
billEntry=Entry(customer_details_frame,font=('arial',15),bd=7,width=18)
billEntry.grid(row=0,column=5,padx=8)

searchButton=Button(customer_details_frame,text='SEARCH',font=('times new roman',12,'bold'),
                    bd=7,width=10,command=search_bill)
searchButton.grid(row=0,column=6,padx=20,pady=8)

productFrame=Frame(window)
productFrame.pack()

cosmeticsFrame=LabelFrame(productFrame,text='Cosmetics',font=('times new roman',15,'bold')
                                  , fg='gold', bd=8, relief=GROOVE,bg='gray20' )
cosmeticsFrame.grid(row=0,column=0)

BathsoapLabel=Label(cosmeticsFrame,text='Bath Soap',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BathsoapLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')
BathsoapEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
BathsoapEntry.grid(row=0,column=1,padx=10)
BathsoapEntry.insert(0,0)

facecreamLabel=Label(cosmeticsFrame,text='Face Cream',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facecreamLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')
facecreamEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
facecreamEntry.grid(row=1,column=1,pady=9,padx=10)
facecreamEntry.insert(0,0)

facewashLabel=Label(cosmeticsFrame,text='Face Wash',font=('times new roman',15,'bold'),bg='gray20',fg='white')
facewashLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')
facewashEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
facewashEntry.grid(row=2,column=1,padx=10)
facewashEntry.insert(0,0)

hairsparyLabel=Label(cosmeticsFrame,text='Hair Spary',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairsparyLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')
hairsparyEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
hairsparyEntry.grid(row=3,column=1,padx=10)
hairsparyEntry.insert(0,0)

hairgelLabel=Label(cosmeticsFrame,text='Hair Gel',font=('times new roman',15,'bold'),bg='gray20',fg='white')
hairgelLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')
hairgelEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
hairgelEntry.grid(row=4,column=1,padx=10)
hairgelEntry.insert(0,0)

BodylotionLabel=Label(cosmeticsFrame,text='Body Lotion',font=('times new roman',15,'bold'),bg='gray20',fg='white')
BodylotionLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')
BodylotionEntry=Entry(cosmeticsFrame,font=('arial',15,'bold'),bd=5,width=10)
BodylotionEntry.grid(row=5,column=1,padx=10)
BodylotionEntry.insert(0,0)

groceryFrame=LabelFrame(productFrame,text='Grocery',font=('times new roman',15,'bold')
                                  , fg='gold', bd=8, relief=GROOVE,bg='gray20' )
groceryFrame.grid(row=0,column=1)

RiceLabel=Label(groceryFrame,text='Rice',font=('times new roman',15,'bold'),bg='gray20',fg='white')
RiceLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')
RiceEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
RiceEntry.grid(row=0,column=1,padx=10)
RiceEntry.insert(0,0)

OilLabel=Label(groceryFrame,text='Oil',font=('times new roman',15,'bold'),bg='gray20',fg='white')
OilLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')
OilEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
OilEntry.grid(row=1,column=1,padx=10)
OilEntry.insert(0,0)

DaalLabel=Label(groceryFrame,text='Daal',font=('times new roman',15,'bold'),bg='gray20',fg='white')
DaalLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')
DaalEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
DaalEntry.grid(row=2,column=1,padx=10)
DaalEntry.insert(0,0)

SpicesLabel=Label(groceryFrame,text='Spices',font=('times new roman',15,'bold'),bg='gray20',fg='white')
SpicesLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')
SpicesEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
SpicesEntry.grid(row=3,column=1,padx=10)
SpicesEntry.insert(0,0)

SugarLabel=Label(groceryFrame,text='Sugar',font=('times new roman',15,'bold'),bg='gray20',fg='white')
SugarLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')
SugarEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
SugarEntry.grid(row=4,column=1,padx=10)
SugarEntry.insert(0,0)

WheatLabel=Label(groceryFrame,text='Wheat-flour',font=('times new roman',15,'bold'),bg='gray20',fg='white')
WheatLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')
WheatEntry=Entry(groceryFrame,font=('arial',15,'bold'),bd=5,width=10)
WheatEntry.grid(row=5,column=1,padx=10)
WheatEntry.insert(0,0)

drinksFrame=LabelFrame(productFrame,text='Cold-Drinks',font=('times new roman',15,'bold')
                                  , fg='gold', bd=8, relief=GROOVE,bg='gray20' )
drinksFrame.grid(row=0,column=2)

MaazaLabel=Label(drinksFrame,text='Maaza',font=('times new roman',15,'bold'),bg='gray20',fg='white')
MaazaLabel.grid(row=0,column=0,pady=9,padx=10,sticky='w')
MaazaEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
MaazaEntry.grid(row=0,column=1,padx=10)
MaazaEntry.insert(0,0)


PepsiLabel=Label(drinksFrame,text='Pepsi',font=('times new roman',15,'bold'),bg='gray20',fg='white')
PepsiLabel.grid(row=1,column=0,pady=9,padx=10,sticky='w')
PepsiEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
PepsiEntry.grid(row=1,column=1,padx=10)
PepsiEntry.insert(0,0)

SpriteLabel=Label(drinksFrame,text='Sprite',font=('times new roman',15,'bold'),bg='gray20',fg='white')
SpriteLabel.grid(row=2,column=0,pady=9,padx=10,sticky='w')
SpriteEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
SpriteEntry.grid(row=2,column=1,padx=10)
SpriteEntry.insert(0,0)

LimcaLabel=Label(drinksFrame,text='Limca',font=('times new roman',15,'bold'),bg='gray20',fg='white')
LimcaLabel.grid(row=3,column=0,pady=9,padx=10,sticky='w')
LimcaEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
LimcaEntry.grid(row=3,column=1,padx=10)
LimcaEntry.insert(0,0)

FrootiLabel=Label(drinksFrame,text='Frooti',font=('times new roman',15,'bold'),bg='gray20',fg='white')
FrootiLabel.grid(row=4,column=0,pady=9,padx=10,sticky='w')
FrootiEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
FrootiEntry.grid(row=4,column=1,padx=10)
FrootiEntry.insert(0,0)

CocoLabel=Label(drinksFrame,text='Coco Cola',font=('times new roman',15,'bold'),bg='gray20',fg='white')
CocoLabel.grid(row=5,column=0,pady=9,padx=10,sticky='w')
CocoEntry=Entry(drinksFrame,font=('arial',15,'bold'),bd=5,width=10)
CocoEntry.grid(row=5,column=1,padx=10)
CocoEntry.insert(0,0)

billframe=Frame(productFrame,bd=8,relief=GROOVE)
billframe.grid(row=0,column=3,padx=10)
billareaLabel=Label(billframe,text='Bill Area',font=('times new roman',15,'bold'),bd=7,relief=GROOVE)
billareaLabel.pack(fill=X)

scrollbar = Scrollbar(billframe, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

textarea=Text(billframe,height=16,width=50,yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)

billmeanuFrame=LabelFrame(window,text='Bill menu',font=('times new roman',15,'bold')
                                  , fg='gold', bd=5, relief=GROOVE,bg='gray20' )
billmeanuFrame.pack()

cosmeticpriceLabel=Label(billmeanuFrame,text='Cosmetic-Price',font=('times new roman',13,'bold'),bg='gray20',fg='white')
cosmeticpriceLabel.grid(row=0,column=0,pady=6,padx=10,sticky='w')
cosmeticpriceEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
cosmeticpriceEntry.grid(row=0,column=1,pady=6,padx=10)

GrocerypriceLabel=Label(billmeanuFrame,text='Grocery-Price',font=('times new roman',13,'bold'),bg='gray20',fg='white')
GrocerypriceLabel.grid(row=1,column=0,pady=6,padx=10,sticky='w')
GrocerypriceEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
GrocerypriceEntry.grid(row=1,column=1,pady=6,padx=10)

DrinkspriceLabel=Label(billmeanuFrame,text='Cold-Drinks-Price',font=('times new roman',13,'bold'),bg='gray20',fg='white')
DrinkspriceLabel.grid(row=2,column=0,pady=6,padx=10,sticky='w')
DrinkspriceEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
DrinkspriceEntry.grid(row=2,column=1,pady=6,padx=10)

#TAX

cosmeticTaxLabel=Label(billmeanuFrame,text='Cosmetic-Tax',font=('times new roman',13,'bold'),bg='gray20',fg='white')
cosmeticTaxLabel.grid(row=0,column=2,pady=6,padx=10,sticky='w')
cosmeticTaxEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
cosmeticTaxEntry.grid(row=0,column=3,pady=6,padx=10)

GroceryTaxLabel=Label(billmeanuFrame,text='Grocery-Tax',font=('times new roman',13,'bold'),bg='gray20',fg='white')
GroceryTaxLabel.grid(row=1,column=2,pady=6,padx=10,sticky='w')
GroceryTaxEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
GroceryTaxEntry.grid(row=1,column=3,pady=6,padx=10)

DrinkTaxLabel=Label(billmeanuFrame,text='Cold-Drinks-Tax',font=('times new roman',13,'bold'),bg='gray20',fg='white')
DrinkTaxLabel.grid(row=2,column=2,pady=6,padx=10,sticky='w')
DrinkTaxEntry=Entry(billmeanuFrame,font=('arial',15,'bold'),bd=5,width=10)
DrinkTaxEntry.grid(row=2,column=3,pady=6,padx=10)

buttonFrame=Frame(billmeanuFrame,bd=8,relief=GROOVE)
buttonFrame.grid(row=0,column=4,rowspan=3)

totalButton=Button(buttonFrame,text='Total',font=('arial',16,'bold'),bg='gray20',fg='white'
                   ,bd=5,width=8,pady=10,command=total)
totalButton.grid(row=0,column=0,pady=20,padx=5)

billButton=Button(buttonFrame,text='Bill',font=('arial',16,'bold'),bg='gray20',fg='white'
                   ,bd=5,width=8,pady=10,command=bill_area)
billButton.grid(row=0,column=1,pady=20,padx=5)

EmailButton=Button(buttonFrame,text='Email',font=('arial',16,'bold'),bg='gray20',fg='white'
                   ,bd=5,width=8,pady=10,command=send_email)
EmailButton.grid(row=0,column=2,pady=20,padx=5)

PrintButton=Button(buttonFrame,text='Print',font=('arial',16,'bold'),bg='gray20',fg='white'
                   ,bd=5,width=8,pady=10,command=print_bill)
PrintButton.grid(row=0,column=3,pady=20,padx=5)


ClearButton=Button(buttonFrame,text='Clear',font=('arial',16,'bold'),bg='gray20',fg='white'
                   ,bd=5,width=6,pady=10,padx=5)
ClearButton.grid(row=0,column=4,pady=20,padx=5)
window.mainloop()
