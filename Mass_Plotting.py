import HFSSLibrary as hfss
import pandas as pd
import matplotlib.pyplot as plt


[oAnsys, oDesktop] = hfss.openHFSS()


oProject = oDesktop.SetActiveProject("ECEN641_Homework2")

Segments = [3,8,10,20,60]
for N in Segments:

    for problem_num in ["4.18","4.19"]:


        # oDesign = oProject.SetActiveDesign("Problem {1} N = {0}".format(N,problem_num))
        # oModule = oDesign.GetModule("ReportSetup")
        # oModule.ExportToFile("Reflection", "C:/Users/joshruff/PycharmProjects/HFSS_Python/{1}_Reflection_N_{0}.csv".format(N,problem_num))
        # oModule.ExportToFile("Transmission","C:/Users/joshruff/PycharmProjects/HFSS_Python/{1}_Transmission_N_{0}.csv".format(N,problem_num))
        # oModule.ExportToFile("Zin_Mag","C:/Users/joshruff/PycharmProjects/HFSS_Python/{1}_Input_Impedance_mag_N_{0}.csv".format(N,problem_num))
        # oModule.ExportToFile("Zin_Phase","C:/Users/joshruff/PycharmProjects/HFSS_Python/{1}_Input_Impedance_phase_N_{0}.csv".format(N,problem_num))

        reflection_df = pd.read_csv("{1}_Reflection_N_{0}.csv".format(N,problem_num))
        transmission_df = pd.read_csv("{1}_Transmission_N_{0}.csv".format(N,problem_num))
        input_impedance_mag_df = pd.read_csv("{1}_Input_Impedance_mag_N_{0}.csv".format(N,problem_num))
        input_impedance_phase_df = pd.read_csv("{1}_Input_Impedance_phase_N_{0}.csv".format(N,problem_num))

        if problem_num == '4.18':
            variation = ' - C_pul=\'0.4244pF\' L_pul=\'1.06nH\''
            print(variation)
            impedance_mag_string = 'mag(Z(Port1,Port1)) [ohm] - C_pul=\'0.4244pF\' L_pul=\'1.06nH\''
            impedance_phase_string = 'cang_deg(Z(Port1,Port1)) [deg] - C_pul=\'0.4244pF\' L_pul=\'1.06nH\''
        else:
            print(variation)
            variation = ''#'' - C_pul=\'0.21pF\' L_pul=\'0.531nH\''
            impedance_mag_string = 'mag(Z(Port1,Port1)) [ohm]'
            impedance_phase_string = 'cang_deg(Z(Port1,Port1)) [deg]'
        print(N)
        linestyle = '-'

        plt.figure()
        plt.title("Reflection Coefficient (S11)")
        test = reflection_df['F [GHz]']
        # print(reflection_df.head())
        plt.plot(reflection_df['F [GHz]'],reflection_df['dB(S(Port1,Port1)) []{0}'.format(variation)],label="N={0}".format(N),linestyle = linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("S11 Magnitude [dB]")
        plt.legend()
        plt.savefig("{0}_N_{1}_S11_Magnitude".format(problem_num, N) + ".png", dpi=300)

        plt.title("Reflection Coefficient (S11)")
        test = reflection_df['F [GHz]']
        # print(reflection_df.head())
        plt.plot(reflection_df['F [GHz]'], reflection_df['cang_deg(S(Port1,Port1)) [deg]{0}'.format(variation)],
                 label="N={0}".format(N), linestyle=linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("S11 Phase [deg]")
        plt.legend()
        plt.savefig("{0}_N_{1}_S11_Phase".format(problem_num, N) + ".png", dpi=300)

        plt.figure()
        plt.title("Transmission Coefficient (S21)")
        plt.plot(transmission_df['F [GHz]'], transmission_df['dB(S(Port2,Port1)) []{0}'.format(variation)], label="N={0}".format(N),
                 linestyle=linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("S21 [dB]")
        plt.legend()
        plt.savefig("{0}_N_{1}_S21_Magnitude".format(problem_num, N) + ".png", dpi=300)

        plt.figure()
        plt.title("Transmission Coefficient (S21)")
        plt.plot(transmission_df['F [GHz]'], transmission_df['cang_deg(S(Port2,Port1)) [deg]{0}'.format(variation)],
                 label="N={0}".format(N),
                 linestyle=linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("S21 Phase [deg]")
        plt.legend()
        plt.savefig("{0}_N_{1}_S21_Phase".format(problem_num, N) + ".png", dpi=300)

        plt.figure()
        plt.title("Zin Magnitude")
        plt.plot(input_impedance_mag_df['F [GHz]'],input_impedance_mag_df[impedance_mag_string],label="N={0}".format(N), linestyle = linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("mag(Zin) [kOhm]")
        plt.legend()
        # plt.ylim([-20, 2
        plt.savefig("{0}_N_{1}_Zin_Magnitude".format(problem_num, N) + ".png", dpi=300)

        plt.figure()
        plt.title("Zin Phase")
        plt.plot(input_impedance_mag_df['F [GHz]'], input_impedance_phase_df[impedance_phase_string],
                 label="N={0}".format(N), linestyle=linestyle)
        plt.xlabel("Frequency [GHz]")
        plt.ylabel("cang(Zin) [degrees]")
        plt.legend()
            # plt.ylim([-20, 2
        plt.savefig("{0}_N_{1}_Zin_Phase".format(problem_num,N)+ ".png", dpi=300)
plt.show()