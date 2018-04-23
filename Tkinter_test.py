#! /usr/bin/env python3
#-*- coding:utf-8 -*-

from tkinter import *
import tkinter.messagebox

class Application(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #self.helloLabel = Label(self, text = 'Hello, world')
        #self.helloLabel.pack()          #pack()方法把Widget加入到父容器中，并实现布局
        #self.quitButton = Button(self, text = 'Quit', command = self.quit)
        #self.quitButton.pack()

        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text = 'Hello', command = self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.nameInput.get() or 'world'
        tkinter.messagebox.showinfo('Message', 'Hello, %s' % name)

if __name__ == '__main__':
    app = Application()
    app.master.title('Hello World')
    app.mainloop()