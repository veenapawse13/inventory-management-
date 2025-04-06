from tkinter import *
from chatterbot import ChatBot
from chatterbot.trainers import  ListTrainer



bot=ChatBot('Bot')
trainer = ListTrainer(bot)



def botReply():
    question=questionField.get()




    textarea.insert(END,'You: '+question)



    questionField.delete(0,END)




window = Tk()
window.geometry('500x570+100+30')
window.title('ChatBot')
window.config(bg='#00008B')  # Dark blue background for window

# Add logo image
logoPic = PhotoImage(file='pic.png')
logoPicLabel = Label(window, image=logoPic, bg='#00008B')  # Matching logo background
logoPicLabel.pack(pady=5)

# Create center frame for the text area and scrollbar
centerFrame = Frame(window, bg='#1E3A5F')  # Darker blue background for the center frame
centerFrame.pack()

# Create a scrollbar with light blue color
scrollbar = Scrollbar(centerFrame, orient=VERTICAL, bg='#00BFFF', activebackground='#4682B4')  # Bright blue scrollbar with a darker active state
scrollbar.pack(side=RIGHT, fill=Y)

# Create text area with white background and dark blue text
textarea = Text(centerFrame, font=('times new roman', 20, 'bold'), height=10, yscrollcommand=scrollbar.set, wrap=WORD, bg='white', fg='#00008B')  # Dark blue text
textarea.pack(side=LEFT, padx=5)

# Configure scrollbar to work with text area
scrollbar.config(command=textarea.yview)

questionField=Entry(window,font=('verdana',20,'bold'))
questionField.pack(pady=15,fill=X)


askPic=PhotoImage(file='ask.png')
askButton=Button(window, image=askPic, command=botReply)
askButton.pack()


window.mainloop()


