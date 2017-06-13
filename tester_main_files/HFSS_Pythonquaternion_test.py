from HFSSLibrary import *
from EmagDevices import rectangular_patch
import DualQuaternion as dq

[oAnsys, oDesktop]=openHFSS()


#Create Project, Design, and Editor Objects to use as needed.
oProject=oDesktop.NewProject()
oDesktop.RestoreWindow()
oDesign=oProject.InsertDesign("HFSS","HFSS_Script_Test", "DrivenModal", "")

# Patch Dimensions (All in mm)
patchL = 28.6
patchW = 38
subW = 71
subL = 60
subH = 1.5748
probeY = 0
probeX = .5 * patchL - 6

x = -516.94
y = -347.28
z = -62.25

x_rotation = -10.8657
y_rotation = 0
z_rotation = -84.654

rotation_matrix = np.array([[ 0.09316998, 0.97779994,  0.18768759, x],[-0.99565022, 0.0914996,   0.01756325, y], [ 0.,-0.18850756,  0.98207174, z], [0, 0, 0, 1]])
dq_object = dq.mat2DualQuat(rotation_matrix)

dualQuaternionCS(oDesign,dq_object,'mm','DualQuaternionCS')
rectangular_patch(oDesign,patchL,patchW,probeX,probeY,subL,subW,subH,"FR4_epoxy","mm",'DualQuaternionCS','dq_Patch')
globalCS(oDesign)
rotatedCS(oDesign,x,y,z,x_rotation,y_rotation,z_rotation,'mm','test_rotated_cs')
