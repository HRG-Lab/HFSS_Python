import pandas as pd
import numpy as np
import HFSSLibrary as hfss



precision_frequency = 10.0050125313283 # GHz
N = 8
# beam_ports = np.array([0,1])
beam_ports = np.arange(N)

# N=8
#Open Circular Array File Before running script
[oAnsys, oDesktop] = hfss.openHFSS()
oProject = oDesktop.setActiveProject('cyl_array') #cyl_array
phases_df = None

# Read in CSV file and Set active design
if N == 4:
    oDesign = oProject.SetActiveDesign('4_Element_Radius')
    phases_df = pd.read_csv('4x4_phase.csv')
else:
    oDesign = oProject.SetActiveDesign('8_Element_Radius')
    phases_df = pd.read_csv('8x8_phase.csv')



row = phases_df.index[phases_df['Freq [GHz]']==10].tolist()

S_Phase = np.zeros((2*N, 2*N)) # Store Phases indexed by s parameter
print(S_Phase)
# row = freq_list.index[freq_list==].tolist()
print(row)
# print(freq_list.head())

# Loop Through S Paramanters in CSV, Read values from Dataframe into ndarray
for i in range(2*N):
    for j in range(2*N):
        column_string = 'cang_deg(S({0},{1})) [deg]'.format(i+1,j+1)
        # print(column_string)
        # print(phases_df[column_string].iloc[row])
        S_Phase[i, j] = phases_df[column_string].iloc[row]
        # Get only one frequency




modes = np.ones((N,1))
amplitudes = np.ones((N,1))
phases = np.zeros((N,1))
# print(phases)
source_list = []

# Add phase contributions from Each active Beam port into array port
for array_port in range(N):
    source_list.append(str(array_port+1))
    for beam_port in beam_ports:
        # print(N+1+array_port,beam_port+1)
        # print(S_Phase[N+array_port,beam_port])
        phases[array_port] += S_Phase[N+array_port,beam_port]
# print(phases)

i = 0
# fixed_phase = [ 264.34337681,   57.65556644,  257.34443356,  680.70074766]
fixed_phase = [311.22491017 ,  216.35612484,   113.93161896,    16.9062831,    264.4062831,   628.57866275,  1021.16389506,  1263.95080223]
for phase in phases:
    print(phase+fixed_phase[i])
    i += 1

# hfss.edit_sources(oDesign,source_list,modes,amplitudes,phases,'W','deg')