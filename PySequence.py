#!/usr/bin/python

###########################################
# Simple Sequence task
#
# Designed as an example of a button pressing
# task using Python.
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

   # Options that we may decide to pass to the program:
   optDict = {'WIDTH'   :800,  # set to -1 for fullscreen
              'HEIGHT'  :600,  # set to -1 for fullscreen
              'FONTSIZE':18,
              'INSTRUCTIONFILE':'sequence_files/INSTRUCTIONS.txt',
              'BETWEEN_TRIAL_PAUSE': 50.0/1000.0, # ie, 50 ms
              'RESPONSE_TIMEOUT':None, # Set to None for no timeout
              }

   def __init__(self):

      # Pandas is a great way to save data:
      self.AllData = pd.DataFrame()

      # Define my Tkinter window:
      self.win = Tk()
      self.win.update()
      
      # This is a helper variable for packing widgets in:
      nextRow = 0

      # Enter the subject ID:
      GridLabel(self.win,"Subject ID:",nextRow,0)
      self.__subjIdEntry = GridEntry(self.win,"DEFAULT",nextRow,1)
      nextRow += 1

      # Enter the session number:
      GridLabel(self.win,"Current Session:",nextRow,0)
      self.__sessionEntry = GridEntry(self.win,"1",nextRow,1)
      nextRow += 1

      # Insert a blank line:
      GridLabel(self.win,"",nextRow,0)
      nextRow += 1

      # Make Run/Quit buttons:
      self.__runButton = Button(self.win,text="Begin",command=self.runBlock)
      self.__runButton.grid(row=nextRow,column=1,pady=5,sticky=E+W)
      self.__quitButton = Button(self.win,text="Quit",command=self.cleanUp)
      self.__quitButton.grid(row=nextRow,column=0,pady=5,sticky=E+W)
           
      # Run the loop (shows the GUI):
      self.win.mainloop()

      
   def cleanUp(self):
      # This is called when the Quit button is pressed:
      try:
        self.AllData.to_csv(self.outputFile,index=False)
      except:
        print "Seems there's no data to save."
      self.win.quit()

      
   def runBlock(self):
      # This is called when the Run button is pressed:
      self.subjID = self.__subjIdEntry.get()
      self.session = self.__sessionEntry.get()

      # Session File:
      sessionFile = "sequence_files/" + str(self.subjID) + "_" + str(self.session) + ".csv"
      
      # Check if the session file actually exists:
      try:
        junkFile = open(sessionFile,'r')
        junkFile.close()
      except:
        # If I got here, then trying to open the file raised an error.
        # So, it must not exist! Load the default:
        sessionFile = "sequence_files/SEQUENCE_" + str((eval(self.session) + 1) % 2 + 1) + ".csv"
      
      # Output File:
      self.outputFile = SafeFile("data/" + str(self.subjID) + \
                                 "_" + str(self.session) + "_Data.csv",
                                 ".csv")
      print "Will save data to " + self.outputFile
      self.AllData = runSequenceBlock(sessionFile,self.optDict,self.AllData)

      

###########################################################3
# This will do the work, eventually:
def runSequenceBlock(sessionFile,optDict,theData):
    
    if optDict:
        for key in optDict.keys():
            exec(key + "=optDict['" + key + "']")

    myWindow = Display(width=WIDTH,height=HEIGHT)
    myWindow.setSize(FONTSIZE)
    myWindow.setColor('white')
    
    # Put up some instructions:
    if INSTRUCTIONFILE:
        iFile = open(INSTRUCTIONFILE,'r')
        instructionLines = iFile.readlines()
        iFile.close()
        instructionText = ""
        for line in instructionLines:
            instructionText += line + '\n'
        
        myWindow.setText(instructionText)

        throwThisAway = myWindow.getKeypress()

        # Clear the screen:
        myWindow.setText("")
        myWindow.update()
       
    #myWindow.close()
    #return dataDict
    
    myClocks=Clock(5)
    
    runMe = pd.read_csv(sessionFile)
    
    for i in runMe.index:
        thisTrial = runMe.ix[i]
        
        # Things to save:
        RT = -1
        numBadResponses = 0
        badResponses = ''
        
        TN = i+1
        
        # Change the color to whatever it needs to be:
        myWindow.setColor(thisTrial['color'])
        
        # Move the text to where it needs to be:
        myWindow.moveText(thisTrial['xpos'],-1*thisTrial['ypos'])
        # ...multiplying 'ypos' by -1 means that positive is up.
        
        # Show the text:
        myWindow.setText(thisTrial['letter'])
        myWindow.update()
        
        # Get the response:
        pressedCorrectKey = False
        myClocks.reset(3)
        while not(pressedCorrectKey):
            theKey = myWindow.getKeypress(myClocks,timeout=RESPONSE_TIMEOUT)
            
            if theKey == thisTrial['correct_key']:
                RT = myClocks[3]
                pressedCorrectKey = True
            else:
                print '\a'
                numBadResponses += 1
                badResponses += theKey
        
        # Unmove the text:
        myWindow.moveText(-1*thisTrial['xpos'],thisTrial['ypos'])
        myWindow.setText("")
        myWindow.update()
        
        # Save the data:
        thisRow = pd.Series()
        
        thisRow['TN'] = TN
        thisRow['RT'] = RT
        thisRow['numBadResponses'] = numBadResponses
        thisRow['badResponses'] = badResponses
        # And save everything in the sequence file, just for grins:
        for item in thisTrial.index.values:
            thisRow[item] = thisTrial[item]
   
        theData = theData.append(thisRow,ignore_index=True)
        
        myClocks.reset(2)
        while myClocks[2] < BETWEEN_TRIAL_PAUSE:
            myClocks.update()
    
    myWindow.close()
    
    # Nice to explicitly order the data output sometimes:
    orderedCols = ['TN','RT','numBadResponses','badResponses']
    allCols = theData.columns.values
    
    for col in allCols:
        if col in orderedCols:
            None
        else:
            orderedCols.append(col)
    
    return theData[orderedCols]

setupGUI()