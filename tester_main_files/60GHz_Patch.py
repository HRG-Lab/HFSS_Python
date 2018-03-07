from EmagDevices import *

[oAnsys, oDesktop] = openHFSS()

# Create Project, Design, and Editor Objects to use as needed.
oProject = oDesktop.NewProject()
oDesktop.RestoreWindow()
oDesign = oProject.InsertDesign("HFSS", "HFSS_Script_Test", "DrivenModal", "")

#Constants
c=3e8
f=10e9
wavelength = c/f



excitations = []
object_names = []
globalCS(oDesign)  # Ensures that all relative CS are created based off global CS's
name = "Patch%d" % (1)
# [temp_excitation, temp_object_names] = rectangular_patch(oDesign, patchL, patchW, probeX, probeY, subL, subW, subH,
# 								"FR4_epoxy", "mm", "Global", name)


[temp_excitation,temp_object_names] =design_rectangular_patch(oDesign, f, 50, 20,
        2.2, "Rogers RT/duroid 5880 (tm)", "mil","global", name)
r = wavelength
max_r = r + 10


globalCS(oDesign)
drawSphere(oDesign, 0, 0, 0, max_r+wavelength/3, "mm", "vacuum", "Global", "radiation_boundary", .55)
# binarySubtraction(oDesign, "radiation_boundary", object_names,True)
insertSetup(oDesign, 2.45e9,"Test_Setup")
LinearFrequencySweep(oDesign,2e9,4e9, .01e7, "Test_Setup", "Test_Sweep")
AssignRadiationBoundary(oDesign, "radiation_boundary", "radiation_boundary")
