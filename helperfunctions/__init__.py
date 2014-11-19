# By existing, this file lets me import the directory
# Importing every python file in the directory allows 
# from devices import * statements

#try: from Monitor import *
#except (ImportError): print "Monitor.py not found..."

try: from Clock import *
except (ImportError): print "Problem importing Clock.py"

try: from TKdisplay import *
except (ImportError): print "Problem importing TKdisplay.py"

try: from DataIO import *
except (ImportError): print "Problem importing DataIO.py"
