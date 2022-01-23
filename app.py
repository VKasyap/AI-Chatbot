from tkinter import *
from chat_tkinter import *
#print(bot_name)

BG_GRAY='#ABB2B9'
BG_COLOR='#17202A'
TEXT_COLOR='#EAECEE'

FONT='Helvetica 12'
FONT_BOLD= 'Helvetica 13 bold'

class ChatApplication:
    def __init__(self):
        self.window=Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()  #This is what we call to start our application on Tkinter

    def _setup_main_window(self):
        self.window.title('Chat')
        self.window.resizable(width=True, height=False)  #This will make the window not adjustable
        self.window.configure(width=550, height=550, bg=BG_COLOR)

        #Head Label
        head_label= Label(self.window, bg=BG_COLOR, fg= TEXT_COLOR, text='Welcome!', font=FONT_BOLD, pady=10) #pady moves the window by 10
        head_label.place(relwidth=1)  #Setting the relative width as 1 would take the whole window as the width

        #Tiny divider
        line= Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely= 0.07, relheight=0.012)

        #Text widget
        self.text_widget=Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5,pady=5)

        #The above line means we can display 20 characters in 1 line.We can use 2 lines. and some padding so it doesnt start at beginning
        #NOTE: We didnt use self. for the head_label and line because it wont be used later in other functions. But the text_widget would be used later.
        self.text_widget.place(relheight=0.745, relwidth=1, rely= 0.08) #This indicats that this window uses up 75% of window and we use whole width
        self.text_widget.configure(cursor='arrow',state=DISABLED)

        #Add a Scroll bar so we can scroll up and down.
        scrollbar= Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)     #This has to cover the entire text widget area and it is placed to the right
        scrollbar.configure(command= self.text_widget.yview)  #This will change the y position that helps to scroll

        #Bottom Label
        bottom_label= Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1,rely=0.825)

        #Message Entry Box
        self.msg_entry= Entry(bottom_label,bg='#2C3E50', fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008,relx=0.011)
        self.msg_entry.focus()  #Whenever we start the appplication, this widget is in focus and we can start typing
        self.msg_entry.bind("<Return>", self._on_enter_pressed)  #We need to define this function "_on_enter_pressed"

        #Send Button
        send_button= Button(bottom_label, text='Send',font=FONT_BOLD, width=20, bg=BG_GRAY,
                            command= lambda: self._on_enter_pressed(None)) #Usually for the function, there would be an event. But since it is already a button, we pass it as None
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)


    def _on_enter_pressed(self, event):
        msg= self.msg_entry.get()
        self._insert_message(msg,'YOU')

    def _insert_message(self,msg, sender):
        if not msg:  #Suppose we put in a text without typing anything
            return

        self.msg_entry.delete(0, END)  #If there is a message, then we can delete it
        msg1= f'{sender}: {msg} \n\n'
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END,msg1)
        self.text_widget.configure(state=DISABLED) #After we have entered the message, we can disable it

        #Response from Chatbot
        msg2 = f'{bot_name}: {get_response(msg)} \n\n'
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)  # After we have entered the message, we can disable it

        self.text_widget.see(END)  #This means it is always scrolled to the end and we would always see the last msg

if __name__=='__main__':
    app=ChatApplication()
    app.run()