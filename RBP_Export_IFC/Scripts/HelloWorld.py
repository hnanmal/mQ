"""Output "Hello Revit world!" to the console / log."""

# This section is common to all Python task scripts.
import clr
import System

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.DB import *

import revit_script_util
from revit_script_util import Output

sessionId = revit_script_util.GetSessionId()
uiapp = revit_script_util.GetUIApplication()

doc = revit_script_util.GetScriptDocument()
revitFilePath = revit_script_util.GetRevitFilePath()

# The code above is boilerplate, everything below is all yours.
# You can use almost any part of the Revit API here!

# Output()
Output("Hello Revit world!")
