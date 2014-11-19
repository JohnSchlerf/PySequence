from Tkinter import *
import os

kNullCursorData="""
  #define t_cur_width 1
  #define t_cur_height 1
  #define t_cur_x_hot 0
  #define t_cur_y_hot 0
  static unsigned char t_cur_bits[] = { 0x00};
  """

class Display:
    """ Implements my generic TK frame? """

    def __init__(self,width=800,height=600,background="black",fontColor="white"):
        try:
            self.root = Toplevel()
        except:
            self.root = Tk()
        """
        # This used to work, but it seem that self.root.state("zoomed") is
        # now a bad way to do this. self.root.geometry still works fine, though.
        if width==-1 and height==-1:
            self.root.state("zoomed")
        else:
            if width==-1: width = self.root.winfo_screenwidth()
            if height==-1: height = self.root.winfo_screenheight()
            self.root.geometry("%dx%d+0+0" % (width, height))
        """
        if width==-1: width = self.root.winfo_screenwidth()
        if height==-1: height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (width, height))
        self.root.overrideredirect(1)
        self.root.focus_set()
        self.killCursor()
        self.root.bind_all("<Key>", self._kbCallback)
        self.root.bind("<Escape>", lambda e: e.widget.quit())
        self.root.configure(background=background)
        self.IsRunning = True
        self.clearKey()
        #self.root.update()
        self.myText = StringVar()
        self.myFont = ('Arial',18,'bold')
        self.fontColor=fontColor
        self.myLabel = Label(self.root, textvariable=self.myText, font=self.myFont, fg=self.fontColor, bg=background)
        self.myText.set("")
        self.myLabel.pack(expand=YES)
        self.root.update()

    def killCursor(self):
        self.root.configure(cursor="none")

    def _kbCallback(self,event):
        """ Close on Escape, otherwise save the keypress """
        if event.keysym == 'Escape': self.Close()
        if not self.keyPress:
            self.keyPress=event.char

    def SetSize(self,size=18):
        self.myFont = (self.myFont[0], size, self.myFont[2])

    def SetColor(self,color="white"):
        self.fontColor=color

    def SetText(self,text):
        if self.IsRunning:
            self.myText.set(text)
            self.myLabel.configure(font=self.myFont,fg=self.fontColor)

    def MoveText(self,newX=0,newY=0):
        if self.IsRunning:
            self.myLabel.place(x=self.myLabel.winfo_x()+newX,
                               y=self.myLabel.winfo_y()+newY)

    def SetImage(self,imageFile):
        None

    def ClearImage(self):
        None

    def Close(self):
        if self.IsRunning:
            self.IsRunning = False
            self.root.destroy()

    def update(self):
        if self.IsRunning:
            self.root.update()

    def clearKey(self):
        self.keyPress = None

    def __cmp__(self,other):
        """ I may not need this... but... """
        if self.lastKey == other:
            return 0
        if self.lastKey > other:
            return 1
        if self.lastKey < other:
            return -1

    def __getitem__(self,key):
        return self.IsRunning
