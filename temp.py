import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants declaration
delta_t = 0.0001
#k_const = 1.4
P_atm = float(1*101325)
#Rs = 287
'''
# Fuction to change constants values for selected gas
def change_gas(event):
    global k_const
    global Rs
    gas_name = choosen_gas.get()

    if(gas_name == "Air"):
        k_const = 1.4
        Rs = 287
    if(gas_name == "Argon"):
        k_const = 1.67
        Rs = 208
    if(gas_name == "Helium"):
        k_const = 1.66
        Rs = 2077
    if(gas_name == "Hydrogen"):
        k_const = 1.41
        Rs = 4124
    if(gas_name == "Nitrogen"):
        k_const = 1.4
        Rs = 297 
    if(gas_name == "CO2"):
        k_const = 1.3
        Rs = 188
    if(gas_name == "Xenon"):
        k_const = 1.65
        Rs = 208
'''


# Array declaration
array_time = []
array_h = []
array_Ft = []
array_mass = []
array_temperature = []
array_pressure = []
array_V_water = []
array_V_air = []
'''
# Output variables declaration
Ic = float(0)
max_h = float(0)
total_time = float(0)
delta_v = float(0)
'''
# Optimalization output data
array_opt_x = []
array_opt_Ic = []
array_opt_tc = []
array_opt_delta_v = []
array_opt_Ist = []
opt_variable_name = ""

# Simulation for optimalization loop
def opt_sim(k_const, Rs, water_density, P_ins, At, V_air, V_water, Roc_mass, T, rod_lenght, rod_inside_diameter):
    try:
        #print(str(k_const) + " " + str(Rs) + " " + str(water_density) + " "+ str(P_ins) + " " + str(At) + " " + str(V_water) + " " + str(V_air) + " " + str(Roc_mass) +" "+ str(T) + " " + str(rod_lenght) + " " + str(rod_inside_diameter)+ "\n")
        # Output variables declaration
        Ic = float(0)
        max_h = float(0)
        total_time = float(0)
        delta_v = float(0)

        s = float(0.0)
        vrod = float(0.0)

        

        # Define adiabatic constant
        C_const = P_ins * pow(V_air, k_const)

        
        # Calculate mass of air
        mass_air = P_ins * V_air / (T * Rs)
        mass_propelant = mass_air + V_water * water_density
        total_time = 0

        # V_air fix for existing rod
        V_air = V_air - At * rod_lenght

        if(rod_inside_diameter > 0 and rod_lenght > 0):
            while(s < rod_lenght):
                # Array update
                #array_time.append(total_time)
                total_time = total_time + delta_t
                
                #array_V_water.append(V_water)
                #array_V_air.append(V_air)

                #array_mass.append(Roc_mass)
                #array_pressure.append(P_ins)
                #array_temperature.append(T)

                # Calculate Ft and Ic
                Ft = P_ins * At
                #array_Ft.append(Ft)
                Ic += Ft * delta_t

                arod = Ft / Roc_mass
                vrod += delta_t * arod
                delta_v += vrod

                s += vrod * delta_t + 0.5 * arod * delta_t * delta_t

        if(rod_inside_diameter == 0 and rod_lenght > 0):
            while(s < rod_lenght):
                # Array update
                #array_time.append(total_time)
                total_time = total_time + delta_t

                #array_mass.append(Roc_mass)
                #array_V_air.append(V_air)
                #array_V_water.append(V_water)
                
                #array_pressure.append(P_ins)
                #array_temperature.append(T)

                # Calculate Ft and Ic
                Ft = P_ins * At
                #array_Ft.append(Ft)
                Ic += Ft * delta_t

                arod = Ft / Roc_mass
                vrod += delta_t * arod
                delta_v += vrod

                s += vrod * delta_t + 0.5 * arod * delta_t * delta_t

                delta_V = At * vrod * delta_t
                V_air += delta_V

                P_ins = C_const / pow(V_air, k_const)

                T = (P_ins * V_air) / (mass_air * Rs)



        # Main loop of simulation, handles models that push out only fraction of water inside
        while(float(V_water) > float(0) and float(P_ins) > float(P_atm)):  
            # Update time array for plot
            #array_time.append(total_time)
            total_time = total_time + delta_t 

            # Calculate thurst
            Ft = 2 * At * (P_ins - P_atm)
            #array_Ft.append(Ft)
            Ic += Ft * delta_t

            ve = math.sqrt(2 * (P_ins - P_atm) / water_density)

            # Calculate change of volume
            delta_V = At * ve * delta_t

            # Update volume arrays
            #array_V_water.append(V_water)
            #array_V_air.append(V_air)

            # Calculate temperature
            T = P_ins * V_air / (mass_air * Rs)
            #array_temperature.append(T)

            # Update mass array
            #array_mass.append(Roc_mass)
            Roc_mass = Roc_mass - delta_V * water_density

            # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass


            # Update volume values
            V_air = V_air + delta_V
            V_water = V_water - delta_V
            
            # Calculate pressure and update array
            #array_pressure.append(P_ins)
            P_ins = C_const * pow(V_air, -k_const)
            
        # Loop for Mach 1 on exit
        while(P_ins > P_atm and P_ins/P_atm >= pow((k_const+1)/2, k_const/(k_const-1))):
            # Update time array for plot
            #array_time.append(total_time)
            total_time = total_time + delta_t 

            # Add values that are not changing for plot            
            #array_V_water.append(V_water)
            #array_V_air.append(V_air)


            Tt = T * 2 / (k_const + 1)

            dot_m = P_ins * At * pow(2/(k_const+1), 0.5 * (k_const+1)/(k_const-1)) * math.sqrt(k_const/(Rs*Tt))
            
            ve_air = math.sqrt(k_const * Rs * Tt)

            P_throat = pow(2 / (k_const + 1), k_const / (k_const - 1)) * P_ins
            Ft = dot_m * ve_air + At * (P_throat - P_atm)
            array_Ft.append(Ft)
            Ic += Ft * delta_t
            
            delta_m = dot_m * delta_t
            
            # Update rocket mass
            Roc_mass = Roc_mass - delta_m
            #array_mass.append(Roc_mass)

             # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass

            mass_air = mass_air - delta_m


            T = (P_ins / Rs) * pow(V_air / (mass_air + delta_m), k_const) * pow(V_air / mass_air, 1 - k_const)
            #array_temperature.append(T)

            P_ins = mass_air * Rs * T / V_air
            #array_pressure.append(P_ins)

        while(P_ins > P_atm):     
            # Update time array for plot
            #array_time.append(total_time)
            total_time = total_time + delta_t 

            # Add values that are not changing for plot           
            #array_V_water.append(V_water)
            #array_V_air.append(V_air)

            Mach = math.sqrt(2 / (k_const-1) * (pow(P_ins / P_atm, (k_const-1) / k_const) - 1))

            Tt = T / (1 + 0.5 * (k_const-1) * Mach * Mach)

            ve_air = Mach * math.sqrt(k_const * Rs * Tt)

            density_chamber = mass_air / V_air
            density_throat = density_chamber / pow(1 + 0.5 * (k_const - 1) * Mach * Mach, 1 / (k_const-1))

            dot_m = At * density_throat * ve_air

            Ft = dot_m * ve_air
            #array_Ft.append(Ft)
            Ic += Ft * delta_t

            delta_m = dot_m * delta_t

            # Update rocket mass
            Roc_mass = Roc_mass - delta_m
            #array_mass.append(Roc_mass)

            # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass

            mass_air = mass_air - delta_m

            T = (P_ins / Rs) * pow(V_air / (mass_air + delta_m), k_const) * pow(V_air / mass_air, 1 - k_const)
            #array_temperature.append(T)

            P_ins = mass_air * Rs * T / V_air
            #array_pressure.append(P_ins)
        
        #print(str(Ic) + "\n")
        return [Ic, total_time, Ic / (mass_propelant * 9.81), delta_v]
    except ValueError:
        # Handle the case where entered value is not valid
        error_label_r.config(text="Invalid input.")



# MAIN OPTIMALIZATION FUNCTION
def optimalize():
    global opt_variable_name

    array_opt_x.clear()
    array_opt_Ic.clear()
    array_opt_tc.clear()
    array_opt_delta_v.clear()
    array_opt_Ist.clear()

    gas_name = choosen_gas_opt.get()

    if(gas_name == "Air"):
        k_const = 1.4
        Rs = 287
    if(gas_name == "Argon"):
        k_const = 1.67
        Rs = 208
    if(gas_name == "Helium"):
        k_const = 1.66
        Rs = 2077
    if(gas_name == "Hydrogen"):
        k_const = 1.41
        Rs = 4124
    if(gas_name == "Nitrogen"):
        k_const = 1.4
        Rs = 297 
    if(gas_name == "CO2"):
        k_const = 1.3
        Rs = 188
    if(gas_name == "Xenon"):
        k_const = 1.65
        Rs = 208
    if(gas_name == "Custom"):
        k_const = float(entry_combobox1_opt.get())
        Rs = float(entry_combobox2_opt.get())

    water_density = float(entry_6_r.get())

    try:
        # Entry values read
        P_ins = float(entry_0_r.get())*100000
        At = 3.1415*pow(0.001*float(entry_1_r.get())/2, 2)
        V_total = float(entry_2_r.get())*0.001
        water_content = float(entry_3_r.get()) * 0.01
        V_air = float(V_total - water_content * V_total)
        V_water = float(water_content * V_total)
        Roc_mass = float(entry_4_r.get())
        T = float(entry_5_r.get())+273.15
        rod_lenght = float(entry_launch_lenght_opt.get()) * 0.001
        rod_inside_diameter = float(entry_launch_diameter_opt.get()) * 0.001
        
        s = float(0.0)
        vrod = float(0.0)

        # V_air fix for existing rod
        V_air = V_air - At * rod_lenght

        # Define adiabatic constant
        C_const = P_ins * pow(V_air, k_const)

        
        # Calculate mass of air
        mass_air = P_ins * V_air / (T * Rs)
        mass_propelant = mass_air + V_water * water_density

        # Get Optimalization variables
        opt_var = choosen_opt_variable.get()
        opt_range_min = float(entry_opt_min.get())
        opt_range_max = float(entry_opt_max.get())
        opt_it = int(entry_opt_itteration.get())

        opt_variable_name = opt_var

        if(opt_var == "Pressure"):
            opt_range_min *= 100000
            opt_range_max *= 100000
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                temp_data_opt = opt_sim(k_const, Rs, water_density, opt_range_min, At, V_air, V_water, Roc_mass, T, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps

        if(opt_var == "Throat"):
            opt_range_min = 3.1415*pow(0.001*opt_range_min/2, 2)
            opt_range_max = 3.1415*pow(0.001*opt_range_max/2, 2)
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                temp_data_opt = opt_sim(k_const, Rs, water_density, P_ins, opt_range_min, V_air, V_water, Roc_mass, T, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps

        if(opt_var == "Volume"):
            opt_range_min *= 0.001
            opt_range_max *= 0.001
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                V_air = opt_range_min - water_content * opt_range_min
                V_water = water_content * opt_range_min

                temp_data_opt = opt_sim(k_const, Rs, water_density, P_ins, At, V_air, V_water, Roc_mass, T, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps
        if(opt_var == "Water content"):
            opt_range_min *= 0.01
            opt_range_max *= 0.01
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                V_air = float(V_total - opt_range_min * V_total)
                V_water = float(opt_range_min * V_total)

                temp_data_opt = opt_sim(k_const, Rs, water_density, float(P_ins), At, V_air, V_water, Roc_mass, T, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps

        if(opt_var == "Dry mass"):
            #opt_range_max *= 0.01
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                temp_data_opt = opt_sim(k_const, Rs, water_density, float(P_ins), At, V_air, V_water, opt_range_min, T, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps

        if(opt_var == "Gas temperature"):
            opt_range_min += 273.15
            opt_range_max += 273.15
            opt_eps = (opt_range_max - opt_range_min) / float(opt_it)
            
            for i in range(opt_it + 1):
                array_opt_x.append(opt_range_min)
                #print(str(opt_range_min) + "\n")

                temp_data_opt = opt_sim(k_const, Rs, water_density, float(P_ins), At, V_air, V_water, Roc_mass, opt_range_min, rod_lenght, rod_inside_diameter)
                array_opt_Ic.append(temp_data_opt[0])
                array_opt_tc.append(temp_data_opt[1])
                array_opt_Ist.append(temp_data_opt[2])
                array_opt_delta_v.append(temp_data_opt[3])

                opt_range_min += opt_eps



        plot_opt_Ic()

        # Erase error message
        error_label_r.config(text="")
    except ValueError:
        # Handle the case where entered value is not valid
        error_label_r.config(text="Invalid input.")


def plot_opt_Ic():
    try:
        # Clear the previous plot
        ax_right.clear()

        # Plot the new data
        ax_right.plot(array_opt_x, array_opt_Ic, linestyle='-', color='b')

        # Set labels and title
        ax_right.set_xlabel(opt_variable_name)
        ax_right.set_ylabel('Ic[Ns]')
        ax_right.set_title('Graph of ')

        # Update the canvas
        canvas_right.draw()

        # Erase error message
        error_label_r.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label_r.config(text="Invalid input.")

def plot_opt_tc():
    try:
        # Clear the previous plot
        ax_right.clear()

        # Plot the new data
        ax_right.plot(array_opt_x, array_opt_tc, linestyle='-', color='b')

        # Set labels and title
        ax_right.set_xlabel(opt_variable_name)
        ax_right.set_ylabel('Total time[s]')
        ax_right.set_title('Graph of ')

        # Update the canvas
        canvas_right.draw()

        # Erase error message
        error_label_r.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label_r.config(text="Invalid input.")

def plot_opt_Ist():
    try:
        # Clear the previous plot
        ax_right.clear()

        # Plot the new data
        ax_right.plot(array_opt_x, array_opt_Ist, linestyle='-', color='b')

        # Set labels and title
        ax_right.set_xlabel(opt_variable_name)
        ax_right.set_ylabel('Specific impuls[s]')
        ax_right.set_title('Graph of ')

        # Update the canvas
        canvas_right.draw()

        # Erase error message
        error_label_r.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label_r.config(text="Invalid input.")

def plot_opt_delta_v():
    try:
        # Clear the previous plot
        ax_right.clear()

        # Plot the new data
        ax_right.plot(array_opt_x, array_opt_delta_v, linestyle='-', color='b')

        # Set labels and title
        ax_right.set_xlabel(opt_variable_name)
        ax_right.set_ylabel('Delta v[m/s]')
        ax_right.set_title('Graph of ')

        # Update the canvas
        canvas_right.draw()

        # Erase error message
        error_label_r.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label_r.config(text="Invalid input.")


# MAIN SIMULATION FUNCTION
def simulate():
    # Output variables declaration
    Ic = float(0)
    max_h = float(0)
    total_time = float(0)
    delta_v = float(0)

    gas_name = choosen_gas.get()

    try:
        if(gas_name == "Air"):
            k_const = 1.4
            Rs = 287
        if(gas_name == "Argon"):
            k_const = 1.67
            Rs = 208
        if(gas_name == "Helium"):
            k_const = 1.66
            Rs = 2077
        if(gas_name == "Hydrogen"):
            k_const = 1.41
            Rs = 4124
        if(gas_name == "Nitrogen"):
            k_const = 1.4
            Rs = 297 
        if(gas_name == "CO2"):
            k_const = 1.3
            Rs = 188
        if(gas_name == "Xenon"):
            k_const = 1.65
            Rs = 208
        if(gas_name == "Custom"):
            k_const = float(entry_combobox1.get())
            Rs = float(entry_combobox2.get())

        water_density = float(entry_6.get())
    
        # Clear total_time value
        total_time = 0
        Ic = 0
        delta_v = 0

        # Clear all arrays
        array_time.clear()
        array_h.clear()
        array_Ft.clear()
        array_mass.clear()
        array_temperature.clear()
        array_pressure.clear()
        array_V_water.clear()
        array_V_air.clear()

        # Entry values read
        P_ins = float(entry_0.get())*100000
        At = 3.1415*pow(0.001*float(entry_1.get())/2, 2)
        V_total = float(entry_2.get())*0.001
        water_content = float(entry_3.get()) * 0.01
        V_air = V_total - water_content * V_total
        V_water = water_content * V_total
        Roc_mass = float(entry_4.get())
        T = float(entry_5.get())+273.15
        rod_lenght = float(entry_launch_lenght.get()) * 0.001
        rod_inside_diameter = float(entry_launch_diameter.get()) * 0.001
        
        s = float(0.0)
        vrod = float(0.0)

        # Define adiabatic constant
        C_const = P_ins * pow(V_air, k_const)

        
        # Calculate mass of air
        mass_air = P_ins * V_air / (T * Rs)
        mass_propelant = mass_air + V_water * water_density

        # V_air fix for existing rod
        V_air = V_air - At * rod_lenght

        if(rod_inside_diameter > 0 and rod_lenght > 0):
            while(s < rod_lenght):
                # Array update
                array_time.append(total_time)
                total_time = total_time + delta_t
                
                array_V_water.append(V_water)
                array_V_air.append(V_air)

                array_mass.append(Roc_mass)
                array_pressure.append(P_ins)
                array_temperature.append(T)

                # Calculate Ft and Ic
                Ft = P_ins * At
                array_Ft.append(Ft)
                Ic += Ft * delta_t

                arod = Ft / Roc_mass
                vrod += delta_t * arod
                delta_v += vrod

                s += vrod * delta_t + 0.5 * arod * delta_t * delta_t

        if(rod_inside_diameter == 0 and rod_lenght > 0):
            while(s < rod_lenght):
                # Array update
                array_time.append(total_time)
                total_time = total_time + delta_t

                array_mass.append(Roc_mass)
                array_V_air.append(V_air)
                array_V_water.append(V_water)
                
                array_pressure.append(P_ins)
                array_temperature.append(T)

                # Calculate Ft and Ic
                Ft = P_ins * At
                array_Ft.append(Ft)
                Ic += Ft * delta_t

                arod = Ft / Roc_mass
                vrod += delta_t * arod
                delta_v += vrod

                s += vrod * delta_t + 0.5 * arod * delta_t * delta_t

                delta_V = At * vrod * delta_t
                V_air += delta_V

                P_ins = C_const / pow(V_air, k_const)

                T = (P_ins * V_air) / (mass_air * Rs)



        # Main loop of simulation, handles models that push out only fraction of water inside
        while(V_water > 0 and P_ins > P_atm):  
            # Update time array for plot
            array_time.append(total_time)
            total_time = total_time + delta_t 

            # Calculate thurst
            Ft = 2 * At * (P_ins - P_atm)
            array_Ft.append(Ft)
            Ic += Ft * delta_t

            ve = math.sqrt(2 * (P_ins - P_atm) / water_density)

            # Calculate change of volume
            delta_V = At * ve * delta_t

            # Update volume arrays
            array_V_water.append(V_water)
            array_V_air.append(V_air)

            # Calculate temperature
            T = P_ins * V_air / (mass_air * Rs)
            array_temperature.append(T)

            # Update mass array
            array_mass.append(Roc_mass)
            Roc_mass = Roc_mass - delta_V * water_density

            # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass


            # Update volume values
            V_air = V_air + delta_V
            V_water = V_water - delta_V
            
            # Calculate pressure and update array
            array_pressure.append(P_ins)
            P_ins = C_const * pow(V_air, -k_const)
            
        # Loop for Mach 1 on exit
        while(P_ins > P_atm and P_ins/P_atm >= pow((k_const+1)/2, k_const/(k_const-1))):
            # Update time array for plot
            array_time.append(total_time)
            total_time = total_time + delta_t 

            # Add values that are not changing for plot            
            array_V_water.append(V_water)
            array_V_air.append(V_air)


            Tt = T * 2 / (k_const + 1)

            dot_m = P_ins * At * pow(2/(k_const+1), 0.5 * (k_const+1)/(k_const-1)) * math.sqrt(k_const/(Rs*Tt))
            
            ve_air = math.sqrt(k_const * Rs * Tt)

            P_throat = pow(2 / (k_const + 1), k_const / (k_const - 1)) * P_ins
            Ft = dot_m * ve_air + At * (P_throat - P_atm)
            array_Ft.append(Ft)
            Ic += Ft * delta_t
            
            delta_m = dot_m * delta_t
            
            # Update rocket mass
            Roc_mass = Roc_mass - delta_m
            array_mass.append(Roc_mass)

             # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass

            mass_air = mass_air - delta_m


            T = (P_ins / Rs) * pow(V_air / (mass_air + delta_m), k_const) * pow(V_air / mass_air, 1 - k_const)
            array_temperature.append(T)

            P_ins = mass_air * Rs * T / V_air
            array_pressure.append(P_ins)

        while(P_ins > P_atm):     
            # Update time array for plot
            array_time.append(total_time)
            total_time = total_time + delta_t 

            # Add values that are not changing for plot           
            array_V_water.append(V_water)
            array_V_air.append(V_air)

            Mach = math.sqrt(2 / (k_const-1) * (pow(P_ins / P_atm, (k_const-1) / k_const) - 1))

            Tt = T / (1 + 0.5 * (k_const-1) * Mach * Mach)

            ve_air = Mach * math.sqrt(k_const * Rs * Tt)

            density_chamber = mass_air / V_air
            density_throat = density_chamber / pow(1 + 0.5 * (k_const - 1) * Mach * Mach, 1 / (k_const-1))

            dot_m = At * density_throat * ve_air

            Ft = dot_m * ve_air
            array_Ft.append(Ft)
            Ic += Ft * delta_t

            delta_m = dot_m * delta_t

            # Update rocket mass
            Roc_mass = Roc_mass - delta_m
            array_mass.append(Roc_mass)

            # Update delta_v
            delta_v = delta_v + delta_t * Ft / Roc_mass

            mass_air = mass_air - delta_m

            T = (P_ins / Rs) * pow(V_air / (mass_air + delta_m), k_const) * pow(V_air / mass_air, 1 - k_const)
            array_temperature.append(T)

            P_ins = mass_air * Rs * T / V_air
            array_pressure.append(P_ins)



        # Erase error message
        error_label.config(text="")

        # Print  output values
        text_widget.insert(tk.END, "Ic = ")
        text_widget.insert(tk.END, Ic) 
        text_widget.insert(tk.END, "\n")

        text_widget.insert(tk.END, "tc = ")
        text_widget.insert(tk.END, total_time) 
        text_widget.insert(tk.END, "\n")
        
        text_widget.insert(tk.END, "Ist = ")
        text_widget.insert(tk.END, Ic / (mass_propelant * 9.81)) 
        text_widget.insert(tk.END, "\n")

        text_widget.insert(tk.END, "delta_v = ")
        text_widget.insert(tk.END, delta_v) 
        text_widget.insert(tk.END, "\n\n")

        
        plot_Ft()

    except ValueError:
        # Handle the case where entered value is not valid
        error_label.config(text="Invalid input.")

def plot_Ft():
    try:
        # Clear the previous plot
        ax_left.clear()

        # Plot the new data
        ax_left.plot(array_time, array_Ft, linestyle='-', color='b')

        # Set labels and title
        ax_left.set_xlabel('Time[t]')
        ax_left.set_ylabel('Thrust[N]')
        ax_left.set_title('Graph of thrust')

        # Update the canvas
        canvas_left.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input.")


def plot_mass():
    try:
        # Clear the previous plot
        ax_left.clear()

        # Plot the new data
        ax_left.plot(array_time, array_mass, linestyle='-', color='b')

        # Set labels and title
        ax_left.set_xlabel('Time[t]')
        ax_left.set_ylabel('Mass[kg]')
        ax_left.set_title('Graph of mass')

        # Update the canvas
        canvas_left.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input.")

def plot_temperature():
    try:
        # Clear the previous plot
        ax_left.clear()

        # Plot the new data
        ax_left.plot(array_time, array_temperature, linestyle='-', color='b')

        # Set labels and title
        ax_left.set_xlabel('Time[t]')
        ax_left.set_ylabel('Temperature[K]')
        ax_left.set_title('Graph of temperature')

        # Update the canvas
        canvas_left.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input.")


def plot_pressure():
    try:
        # Clear the previous plot
        ax_left.clear()

        # Change pressure unit to bar
        for i in range(len(array_pressure)):
            array_pressure[i] /= 100000

        # Plot the new data
        ax_left.plot(array_time, array_pressure, linestyle='-', color='b')

        # Set labels and title
        ax_left.set_xlabel('Time[s]')
        ax_left.set_ylabel('Pressure[bar]')
        ax_left.set_title('Graph of pressure')

        # Update the canvas
        canvas_left.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input.")


def plot_volume():
    try:
        # Clear the previous plot
        ax_left.clear()

        # Plot the new data
        ax_left.plot(array_time, array_V_water, linestyle='-', color='b', label = "Water")
        ax_left.plot(array_time, array_V_air, linestyle='-', color='c', label = "Air")
        
        # Set labels and title
        ax_left.set_xlabel('Time[t]')
        ax_left.set_ylabel('Volume in m^3')
        ax_left.set_title('Graph of thrust')
        ax_left.legend()
        # Update the canvas
        canvas_left.draw()  

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input.")


# Create the main Tkinter window
root = tk.Tk()
root.title("Water Rocket Simulator")

# Set the window size to full screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

frame_simulate = ttk.Frame(root, padding="10")
frame_simulate.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

simulate_button = ttk.Button(frame_simulate, text="Simulate", command=simulate)
simulate_button.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

# Create a label for displaying the selected option
label_gas = ttk.Label(frame_simulate, text="Choose a gas:")
label_gas.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

# Create a StringVar to hold the selected value from the combobox
default_option = "Air"
choosen_gas = tk.StringVar(value=default_option)

# Create a combobox (dropdown menu)
options = ["Air", "Argon", "Helium", "Hydrogen", "Nitrogen", "CO2", "Xenon", "Custom"]
combobox = ttk.Combobox(frame_simulate, textvariable=choosen_gas, values=options, state="readonly", width=7)
combobox.grid(row=1, column=2, columnspan=2, pady=5, sticky="w")

label_custom_gas_info = ttk.Label(frame_simulate, text="Custom gas data:")
label_custom_gas_info.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

label_combobox1 = ttk.Label(frame_simulate, text="Specific heat ratio:")
label_combobox1.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_combobox1 = ttk.Entry(frame_simulate, width=10)
entry_combobox1.grid(row=4, column=2, pady=5)
entry_combobox1.insert(0, "0")  # Initialize with a default value
# combobox.bind("<<ComboboxSelected>>", change_gas)

label_combobox2 = ttk.Label(frame_simulate, text="Specific gas constant:")
label_combobox2.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

entry_combobox2 = ttk.Entry(frame_simulate, width=10)
entry_combobox2.grid(row=5, column=2, pady=5)
entry_combobox2.insert(0, "0")  # Initialize with a default value

# Launch rod data
label_launch_lenght = ttk.Label(frame_simulate, text="Launch rod lenght:")
label_launch_lenght.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

entry_launch_lenght = ttk.Entry(frame_simulate, width=10)
entry_launch_lenght.grid(row=6, column=2, pady=5)
entry_launch_lenght.insert(0, "0")  # Initialize with a default value

label_launch_diameter = ttk.Label(frame_simulate, text="Rod inside diameter:")
label_launch_diameter.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

entry_launch_diameter = ttk.Entry(frame_simulate, width=10)
entry_launch_diameter.grid(row=7, column=2, pady=5)
entry_launch_diameter.insert(0, "0")  # Initialize with a default value

# Create and pack widgets on the left side
frame_left = ttk.Frame(root, padding="10")
frame_left.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

label_0 = ttk.Label(frame_left, text="Pressure[bar]:")
label_0.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

entry_0 = ttk.Entry(frame_left, width=10)
entry_0.grid(row=0, column=2, pady=5)
entry_0.insert(0, "0")  # Initialize with a default value

label_1 = ttk.Label(frame_left, text="Throat diameter[mm]:")
label_1.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

entry_1 = ttk.Entry(frame_left, width=10)
entry_1.grid(row=1, column=2, pady=5)
entry_1.insert(0, "0")  # Initialize with a default value

label_2 = ttk.Label(frame_left, text="Total volume[l]:")
label_2.grid(row=2, column=0, columnspan=2,  pady=5, sticky="w")

entry_2 = ttk.Entry(frame_left, width=10)
entry_2.grid(row=2, column=2, pady=5)
entry_2.insert(0, "0")  # Initialize with a default value

label_3 = ttk.Label(frame_left, text="Water content[%]:")
label_3.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_3 = ttk.Entry(frame_left, width=10)
entry_3.grid(row=3, column=2, pady=5)
entry_3.insert(0, "0")  # Initialize with a default value

label_4 = ttk.Label(frame_left, text="Mass of rocket[kg]:")
label_4.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_4 = ttk.Entry(frame_left, width=10)
entry_4.grid(row=4, column=2, pady=5)
entry_4.insert(0, "0")  # Initialize with a default value

# Updated row number for Label and Entry
label_5 = ttk.Label(frame_left, text="Temperature[C]:")
label_5.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

entry_5 = ttk.Entry(frame_left, width=10)
entry_5.grid(row=5, column=2, pady=5)
entry_5.insert(0, "0")  # Initialize with a default value

# Custom water_density
label_6 = ttk.Label(frame_left, text="Liquid density[kg/m^3]:")
label_6.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

entry_6 = ttk.Entry(frame_left, width=10)
entry_6.grid(row=6, column=2, pady=5)
entry_6.insert(0, "1000")  # Initialize with a default value

frame_button = ttk.Frame(root, padding="10")
frame_button.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

# Adjusted row numbers for the following buttons
plot_button = ttk.Button(frame_button, text="Plot Thrust", command=plot_Ft)
plot_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

plot_button = ttk.Button(frame_button, text="Plot Pressure", command=plot_pressure)
plot_button.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

plot_button = ttk.Button(frame_button, text="Plot Volume", command=plot_volume)
plot_button.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

plot_button = ttk.Button(frame_button, text="Plot Mass", command=plot_mass)
plot_button.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

plot_button = ttk.Button(frame_button, text="Plot Temperature", command=plot_temperature)
plot_button.grid(row=5, column=0, columnspan=2, pady=5,sticky="w")

# ERROR
error_label = ttk.Label(frame_simulate, text="", foreground="red")
error_label.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

frame_text_widget = ttk.Frame(root, padding="10")
frame_text_widget.grid(row=1, column=3, sticky=(tk.W, tk.E, tk.N, tk.S))

text_widget = tk.Text(frame_text_widget, height=11, width=30)
text_widget.grid(row=0, column=0, sticky="w")

# Dupa
frame_plot_left = ttk.Frame(root, padding="10")
frame_plot_left.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a Matplotlib figure and a canvas to embed it in the Tkinter window
fig_left, ax_left = plt.subplots(figsize=(screen_width / 200, screen_height / 150))
canvas_left = FigureCanvasTkAgg(fig_left, master=frame_plot_left)
canvas_widget = canvas_left.get_tk_widget()
canvas_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


##########################################################################
# RIGHT
##########################################################################

frame_simulate_r = ttk.Frame(root, padding="10")
frame_simulate_r.grid(row=1, column=4, sticky=(tk.W, tk.E, tk.N, tk.S))

simulate_button = ttk.Button(frame_simulate_r, text="Optimalize", command=optimalize)
simulate_button.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

# Create a label for displaying the selected option
label_choose_opt = ttk.Label(frame_simulate_r, text="Choose variable to optimalize")
label_choose_opt.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

# Create a StringVar to hold the selected value from the combobox
choosen_opt_variable = tk.StringVar()

# Create a combobox (dropdown menu)
options_variable_opt = ["Pressure", "Throat", "Volume", "Water content", "Dry mass", "Gas temperature"]
combobox_variable_opt = ttk.Combobox(frame_simulate_r, textvariable=choosen_opt_variable, values=options_variable_opt, state="readonly", width=7)
combobox_variable_opt.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
# combobox_variable_opt.bind("<<ComboboxSelected>>", change_gas)

# Optimalization range
label_opt_range = ttk.Label(frame_simulate_r, text="Optimalization range:")
label_opt_range.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_opt_min = ttk.Entry(frame_simulate_r, width=10)
entry_opt_min.grid(row=4, column=0, sticky="w", pady=5)
entry_opt_min.insert(0, "min")  # Initialize with a default value

entry_opt_max = ttk.Entry(frame_simulate_r, width=10)
entry_opt_max.grid(row=5, column=0, sticky="w", pady=5)
entry_opt_max.insert(0, "max")  # Initialize with a default value

# Itteration number
label_opt_itteration = ttk.Label(frame_simulate_r, text="Itterations:")
label_opt_itteration.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

entry_opt_itteration = ttk.Entry(frame_simulate_r, width=6)
entry_opt_itteration.grid(row=6, column=1, sticky="w", pady=5)
entry_opt_itteration.insert(0, "1")  # Initialize with a default value

# 2nd frame on right
frame_overall_data_right = ttk.Frame(root, padding="10")
frame_overall_data_right.grid(row=1, column=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a label for displaying the selected option
label_gas_r = ttk.Label(frame_overall_data_right, text="Choose a gas")
label_gas_r.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

# Create a StringVar to hold the selected value from the combobox
choosen_gas_opt = tk.StringVar(value=default_option)

# Create a combobox (dropdown menu)
options_gas_opt = ["Air", "Argon", "Helium", "Hydrogen", "Nitrogen", "CO2", "Xenon", "Custom"]
combobox_gas_opt = ttk.Combobox(frame_overall_data_right, textvariable=choosen_gas, values=options, state="readonly", width=7)
combobox_gas_opt.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

label_custom_gas_info_opt = ttk.Label(frame_overall_data_right, text="Custom gas data:")
label_custom_gas_info_opt.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

label_combobox1_opt = ttk.Label(frame_overall_data_right, text="Specific heat ratio:")
label_combobox1_opt.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_combobox1_opt = ttk.Entry(frame_overall_data_right, width=10)
entry_combobox1_opt.grid(row=4, column=2, pady=5)
entry_combobox1_opt.insert(0, "0")  # Initialize with a default value

label_combobox2_opt = ttk.Label(frame_overall_data_right, text="Specific gas constant:")
label_combobox2_opt.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

entry_combobox2_opt = ttk.Entry(frame_overall_data_right, width=10)
entry_combobox2_opt.grid(row=5, column=2, pady=5)
entry_combobox2_opt.insert(0, "0")  # Initialize with a default value

# Launch rod data
label_launch_lenght_opt = ttk.Label(frame_overall_data_right, text="Launch rod lenght:")
label_launch_lenght_opt.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

entry_launch_lenght_opt = ttk.Entry(frame_overall_data_right, width=10)
entry_launch_lenght_opt.grid(row=6, column=2, pady=5)
entry_launch_lenght_opt.insert(0, "0")  # Initialize with a default value

label_launch_diameter_opt = ttk.Label(frame_overall_data_right, text="Rod inside diameter:")
label_launch_diameter_opt.grid(row=7, column=0, columnspan=2, pady=5, sticky="w")

entry_launch_diameter_opt = ttk.Entry(frame_overall_data_right, width=10)
entry_launch_diameter_opt.grid(row=7, column=2, pady=5)
entry_launch_diameter_opt.insert(0, "0")  # Initialize with a default value



# Create and pack widgets on the right side
frame_right = ttk.Frame(root, padding="10")
frame_right.grid(row=1, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

label_0_r = ttk.Label(frame_right, text="Pressure[bar]:")
label_0_r.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

entry_0_r = ttk.Entry(frame_right, width=10)
entry_0_r.grid(row=0, column=2, pady=5)
entry_0_r.insert(0, "0")  # Initialize with a default value

label_1_r = ttk.Label(frame_right, text="Throat diameter[mm]:")
label_1_r.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

entry_1_r = ttk.Entry(frame_right, width=10)
entry_1_r.grid(row=1, column=2, pady=5)
entry_1_r.insert(0, "0")  # Initialize with a default value

label_2_r = ttk.Label(frame_right, text="Total volume[l]:")
label_2_r.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

entry_2_r = ttk.Entry(frame_right, width=10)
entry_2_r.grid(row=2, column=2, pady=5)
entry_2_r.insert(0, "0")  # Initialize with a default value

label_3_r = ttk.Label(frame_right, text="Water content[%]:")
label_3_r.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_3_r = ttk.Entry(frame_right, width=10)
entry_3_r.grid(row=3, column=2, pady=5)
entry_3_r.insert(0, "0")  # Initialize with a default value

label_4_r = ttk.Label(frame_right, text="Mass of rocket[kg]:")
label_4_r.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_4_r = ttk.Entry(frame_right, width=10)
entry_4_r.grid(row=4, column=2, pady=5)
entry_4_r.insert(0, "0")  # Initialize with a default value

label_5_r = ttk.Label(frame_right, text="Temperature[C]:")
label_5_r.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

entry_5_r = ttk.Entry(frame_right, width=10)
entry_5_r.grid(row=5, column=2, pady=5)
entry_5_r.insert(0, "0")  # Initialize with a default value

# Custom water_density
label_6_r = ttk.Label(frame_right, text="Liquid density[kg/m^3]:")
label_6_r.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

entry_6_r = ttk.Entry(frame_right, width=10)
entry_6_r.grid(row=6, column=2, pady=5)
entry_6_r.insert(0, "1000")  # Initialize with a default value

# ... (continue with other labels and entries in frame_right)

frame_button_r = ttk.Frame(root, padding="10")
frame_button_r.grid(row=1, column=7, sticky=(tk.W, tk.E, tk.N, tk.S))

# Adjusted row numbers for the following buttons in frame_button_r
plot_button_r = ttk.Button(frame_button_r, text="Plot Ic", command=plot_opt_Ic)
plot_button_r.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

plot_button_r = ttk.Button(frame_button_r, text="Plot tc", command=plot_opt_tc)
plot_button_r.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

plot_button_r = ttk.Button(frame_button_r, text="Plot delta_v", command=plot_opt_delta_v)
plot_button_r.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

plot_button_r = ttk.Button(frame_button_r, text="Plot Ist", command=plot_opt_Ist)
plot_button_r.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

# ERROR
error_label_r = ttk.Label(frame_simulate, text="", foreground="red")
error_label_r.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

# Dupa
frame_plot_right = ttk.Frame(root, padding="10")
frame_plot_right.grid(row=0, column=4, columnspan=5, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a Matplotlib figure and a canvas to embed it in the Tkinter window
fig_right, ax_right = plt.subplots(figsize=(screen_width / 200, screen_height / 150))
canvas_right = FigureCanvasTkAgg(fig_right, master=frame_plot_right)
canvas_widget_right = canvas_right.get_tk_widget()
canvas_widget_right.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

################################################

# Run the Tkinter event loop
root.mainloop()

