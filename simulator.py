import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants declaration
delta_t = 0.01
k_const = 1.4
P_atm = 1*101325
water_density = 1000
Rs = 287


# Array declaration
array_time = []
array_h = []
array_Ft = []
array_mass = []
array_temperature = []
array_pressure = []
array_V_water = []
array_V_air = []

#Output variables declaration
Ic = float(0)
max_h = float(0)
total_time = float(0)


def simulate():
    global total_time
    try:
        # Clear total_time value
        total_time = 0

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
        At = 3.1415*pow(0.01*float(entry_1.get())/2, 2)
        V_air = float(entry_2.get())*0.001
        V_water = float(entry_3.get())*0.001
        Roc_mass = float(entry_4.get())
        T = float(entry_5.get())+273.15

        # Define adiabatic constant
        C_const = P_ins * pow(V_air, k_const)

        # Calculate mass of air
        mass_air = P_ins * V_air / (T * Rs)

        # Main loop of simulation, handles models that push out only fraction of water inside
        while(V_water > 0 and P_ins > P_atm):  
            # Update time array for plot
            array_time.append(total_time)
            total_time = total_time + delta_t 

            # Calculate thurst
            Ft = 2 * At * (P_ins - P_atm)
            array_Ft.append(Ft)

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
            array_mass.append(Roc_mass)            
            array_V_water.append(V_water)
            array_V_air.append(V_air)


            Tt = T * 2 / (k_const + 1)

            dot_m = P_ins * At * pow(2/(k_const+1), 0.5 * (k_const+1)/(k_const-1)) * math.sqrt(k_const/(Rs*Tt))
            
            ve_air = math.sqrt(k_const * Rs * Tt)

            P_throat = pow(2 / (k_const + 1), k_const / (k_const - 1)) * P_ins
            Ft = dot_m * ve_air + At * (P_throat - P_atm)
            array_Ft.append(Ft)

            delta_m = dot_m * delta_t
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
            array_mass.append(Roc_mass)            
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

            delta_m = dot_m * delta_t

            mass_air = mass_air - delta_m

            T = (P_ins / Rs) * pow(V_air / (mass_air + delta_m), k_const) * pow(V_air / mass_air, 1 - k_const)
            array_temperature.append(T)

            P_ins = mass_air * Rs * T / V_air
            array_pressure.append(P_ins)



        # Erase error message
        error_label.config(text="")
        plot_Ft()

    except ValueError:
        # Handle the case where entered value is not valid
        error_label.config(text="Invalid input.")

def plot_Ft():
    try:
        # Clear the previous plot
        ax.clear()

        # Plot the new data
        ax.plot(array_time, array_Ft, marker='o', linestyle='-', color='b')

        # Set labels and title
        ax.set_xlabel('Time[t]')
        ax.set_ylabel('Thrust[N]')
        ax.set_title('Graph of thrust')

        # Update the canvas
        canvas.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")


def plot_mass():
    try:
        # Clear the previous plot
        ax.clear()

        # Plot the new data
        ax.plot(array_time, array_mass, marker='o', linestyle='-', color='b')

        # Set labels and title
        ax.set_xlabel('Time[t]')
        ax.set_ylabel('Mass[kg]')
        ax.set_title('Graph of mass')

        # Update the canvas
        canvas.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")

def plot_temperature():
    try:
        # Clear the previous plot
        ax.clear()

        # Plot the new data
        ax.plot(array_time, array_temperature, marker='o', linestyle='-', color='b')

        # Set labels and title
        ax.set_xlabel('Time[t]')
        ax.set_ylabel('Temperature[K]')
        ax.set_title('Graph of temperature')

        # Update the canvas
        canvas.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")


def plot_pressure():
    try:
        # Clear the previous plot
        ax.clear()

        # Change pressure unit to bar
        for i in range(len(array_pressure)):
            array_pressure[i] /= 100000

        # Plot the new data
        ax.plot(array_time, array_pressure, marker='o', linestyle='-', color='b')

        # Set labels and title
        ax.set_xlabel('Time[s]')
        ax.set_ylabel('Pressure[bar]')
        ax.set_title('Graph of pressure')

        # Update the canvas
        canvas.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")


def plot_volume():
    try:
        # Clear the previous plot
        ax.clear()

        # Plot the new data
        ax.plot(array_time, array_V_water, marker='o', linestyle='-', color='b', label = "Water")
        ax.plot(array_time, array_V_air, marker='o', linestyle='-', color='c', label = "Air")
        
        # Set labels and title
        ax.set_xlabel('Time[t]')
        ax.set_ylabel('Volume in m^3')
        ax.set_title('Graph of thrust')
        ax.legend()
        # Update the canvas
        canvas.draw()

        # Erase error message
        error_label.config(text="")

    except ValueError:
        # Handle the case where the entered value is not a valid float
        error_label.config(text="Invalid input. Please enter a numeric value.")


# Create the main Tkinter window
root = tk.Tk()
root.title("Water Rocket Simulator")

# Create and pack widgets on the left side
frame_left = ttk.Frame(root, padding="10")
frame_left.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

label_0 = ttk.Label(frame_left, text="Enter pressure value:")
label_0.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

entry_0 = ttk.Entry(frame_left, width=10)
entry_0.grid(row=0, column=2, pady=5)
entry_0.insert(0, "0")  # Initialize with a default value

label_1 = ttk.Label(frame_left, text="Enter area throat value:")
label_1.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

entry_1 = ttk.Entry(frame_left, width=10)
entry_1.grid(row=1, column=2, pady=5)
entry_1.insert(0, "0")  # Initialize with a default value

label_2 = ttk.Label(frame_left, text="Enter air volume value:")
label_2.grid(row=2, column=0, columnspan=2,  pady=5, sticky="w")

entry_2 = ttk.Entry(frame_left, width=10)
entry_2.grid(row=2, column=2, pady=5)
entry_2.insert(0, "0")  # Initialize with a default value

label_3 = ttk.Label(frame_left, text="Enter water volume value:")
label_3.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_3 = ttk.Entry(frame_left, width=10)
entry_3.grid(row=3, column=2, pady=5)
entry_3.insert(0, "0")  # Initialize with a default value

label_4 = ttk.Label(frame_left, text="Enter mass of rocket value:")
label_4.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")

entry_4 = ttk.Entry(frame_left, width=10)
entry_4.grid(row=4, column=2, pady=5)
entry_4.insert(0, "0")  # Initialize with a default value

# Updated row number for Label and Entry
label_5 = ttk.Label(frame_left, text="Enter another value:")
label_5.grid(row=5, column=0, columnspan=2, pady=5, sticky="w")

entry_5 = ttk.Entry(frame_left, width=10)
entry_5.grid(row=5, column=2, pady=5)
entry_5.insert(0, "0")  # Initialize with a default value

# Adjusted row numbers for the following buttons
plot_button = ttk.Button(frame_left, text="Simulate", command=simulate)
plot_button.grid(row=6, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(frame_left, text="Plot Thrust", command=plot_Ft)
plot_button.grid(row=7, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(frame_left, text="Plot Pressure", command=plot_pressure)
plot_button.grid(row=8, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(frame_left, text="Plot Volume", command=plot_volume)
plot_button.grid(row=9, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(frame_left, text="Plot Mass", command=plot_mass)
plot_button.grid(row=10, column=0, columnspan=2, pady=10)

plot_button = ttk.Button(frame_left, text="Plot Temperature", command=plot_temperature)
plot_button.grid(row=11, column=0, columnspan=2, pady=10)

error_label = ttk.Label(frame_left, text="", foreground="red")
error_label.grid(row=12, column=0, columnspan=2, pady=5)


# Create a Matplotlib figure and a canvas to embed it in the Tkinter window
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

# Run the Tkinter event loop
root.mainloop()

