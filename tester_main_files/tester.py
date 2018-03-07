from EmagDevices import *
from xlrd import open_workbook
from numpy.matlib import zeros

[oAnsys, oDesktop] = openHFSS()

# Create Project, Design, and Editor Objects to use as needed.
oProject = oDesktop.NewProject()
oDesktop.RestoreWindow()
oDesign = oProject.InsertDesign("HFSS", "HFSS_Script_Test", "DrivenModal", "")


# names = ["startx","starty","startz","length","width","Test_Rectangle"]
# drawRectangle(oDesign,"startz*starty","5mm+6mm*length","2*starty+width",5.5,5,"mm","Z","Global",names,0)



spacing = 2
width = 10
turns = 10
width_multiplier = .75
starting_radius = 210

square_spiral_inductor(oDesign,-starting_radius/2, -starting_radius/2, starting_radius, width, width_multiplier,spacing,turns,"um","Global","Test")