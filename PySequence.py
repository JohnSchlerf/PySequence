#!/usr/bin/python

###########################################
# Simple Sequence task
#
# Designed for simple button pressing
# tasks.
#
# - John Schlerf
#
# See:
# http://github.com/JohnSchlerf/PySequence
###########################################

# This is the library stored here:
from helperfunctions import *

# Pandas is a great library for working with CSV files,
# storing data, etc:
import pandas as pd

###########################################
# I should make this a library someday:

def GridLabel(Parent,Text,Row,Column):
    """
    This is a helper function which adds a label to a grid.
    This is normally a couple of lines, so multiple labels
    gets a little cumbersome...
    """
    L = Label(Parent,text=Text)
    L.grid(row=Row,column=Column)
    return L

def GridEntry(Parent,DefaultText,Row,Column):
    """
    This is a helper function which adds an Entry widget
    to a grid.  Also sets default text.
    """
    E = Entry(Parent)
    E.insert(0,DefaultText)
    E.grid(row=Row,column=Column)
    return E


class setupGUI():
   def __init__(self):
      self.AllData = DataDict()

      # Define my Tkinter window:
      self.win = Tk()
      self.win.update()

      # This is a helper variable for packing widgets in:
      nextRow = 0

      # Enter the subject ID:
      GridLabel(self.win,"Subject ID:",nextRow,0)
      self.__subjIdEntry = GridEntry(self.win,"",nextRow,1)
      nextRow += 1

      # Enter the session number:
      GridLabel(self.win,"Current Session:",nextRow,0)
      self.__sessionEntry = GridEntry(self.win,"",nextRow,1)
      nextRow += 1

      # Insert a blank line:
      GridLabel(self.win,"",nextRow,0)
      nextRow += 1

      # Make Run/Quit buttons:
      self.__runButton = Button(self.win,text="Begin",command=self.runBlock)
      self.__runButton.grid(row=nextRow,column=1,pady=5,sticky=E+W)
      self.__quitButton = Button(self.win,text="Quit",command=self.CleanUp)
      self.__quitButton.grid(row=nextRow,column=0,pady=5,sticky=E+W)
      
      # Run the loop (shows the GUI):
      self.win.mainloop()


   def CleanUp(self):
      # This is called when the Quit button is pressed:
      self.AllData.writePandasOutput(self.fileName)
      self.win.quit()

   def runBlock(self):
      # This is called when the Run button is pressed:
      self.subjID = eval(self.__subjIdEntry.get())
      self.session = eval(self.__sessionEntry.get())

      # see if the session file exists:
      sessionFile = str(self.subjID) + "_" + str(self.session) + ".csv"
      
      if self.BlockNumber == 1:
         self.fileName = SafeFile(self.__fileNameEntry.get(),'.ana')
         
      self.AllData = runSternbergBlock(self.BlockNumber,optDic,self.AllData)
      
      self.__fileNameEntry.delete(0,END)
      self.__fileNameEntry.insert(0,self.fileName)
      self.BlockNumber+=1
      GridLabel(self.win,str(self.BlockNumber),0,1)
