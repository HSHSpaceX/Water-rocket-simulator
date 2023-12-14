import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Constants declaration
delta_t = 0.001
k_const = 1.4
P_atm = 1*101325
water_density = 1000
Rs = 287

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
delta_v = float(0)


def simulate():
    global total_time
    global Ic
    global delta_v

    try:
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

        # Define adiabatic constant
        C_const = P_ins * pow(V_air, k_const)

        # Calculate mass of air
        mass_air = P_ins * V_air / (T * Rs)
        mass_propelant = mass_air + V_water * water_density

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
label_gas = ttk.Label(frame_simulate, text="Choose a gas")
label_gas.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

# Create a StringVar to hold the selected value from the combobox
default_option = "Air"
choosen_gas = tk.StringVar(value=default_option)

# Create a combobox (dropdown menu)
options = ["Air", "Argon", "Helium", "Hydrogen", "Nitrogen", "CO2", "Xenon"]
combobox = ttk.Combobox(frame_simulate, textvariable=choosen_gas, values=options, state="readonly", width=7)
combobox.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
combobox.bind("<<ComboboxSelected>>", change_gas)

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

text_widget = tk.Text(frame_text_widget, height=11, width=40)
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

simulate_button = ttk.Button(frame_simulate_r, text="Optimalize", command=simulate)
simulate_button.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

# Create a label for displaying the selected option
label_choose_opt = ttk.Label(frame_simulate_r, text="Choose variable to optimalize")
label_choose_opt.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

# Create a StringVar to hold the selected value from the combobox
choosen_opt_variable = tk.StringVar()

# Create a combobox (dropdown menu)
options_variable_opt = ["Air", "Argon", "Helium", "Hydrogen", "Nitrogen", "CO2", "Xenon"]
combobox_variable_opt = ttk.Combobox(frame_simulate_r, textvariable=choosen_opt_variable, values=options_variable_opt, state="readonly", width=7)
combobox_variable_opt.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
# combobox_variable_opt.bind("<<ComboboxSelected>>", change_gas)

# Optimalization range
label_opt_range = ttk.Label(frame_simulate_r, text="Optimalization range: (min) (max)")
label_opt_range.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

entry_opt_min = ttk.Entry(frame_simulate_r, width=10)
entry_opt_min.grid(row=4, column=0, sticky="w", pady=5)
entry_opt_min.insert(0, "min")  # Initialize with a default value

entry_opt_max = ttk.Entry(frame_simulate_r, width=10)
entry_opt_max.grid(row=5, column=0, sticky="w", pady=5)
entry_opt_max.insert(0, "max")  # Initialize with a default value

# Create and pack widgets on the right side
frame_right = ttk.Frame(root, padding="10")
frame_right.grid(row=1, column=5, sticky=(tk.W, tk.E, tk.N, tk.S))

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

# ... (continue with other labels and entries in frame_right)

frame_button_r = ttk.Frame(root, padding="10")
frame_button_r.grid(row=1, column=6, sticky=(tk.W, tk.E, tk.N, tk.S))

# Adjusted row numbers for the following buttons in frame_button_r
plot_button_r = ttk.Button(frame_button_r, text="Plot Ic")
plot_button_r.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

plot_button_r = ttk.Button(frame_button_r, text="Plot tc")
plot_button_r.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")

plot_button_r = ttk.Button(frame_button_r, text="Plot delta_v")
plot_button_r.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

# ERROR
error_label_r = ttk.Label(frame_simulate, text="", foreground="red")
error_label_r.grid(row=6, column=0, columnspan=2, pady=5, sticky="w")

# Dupa
frame_plot_right = ttk.Frame(root, padding="10")
frame_plot_right.grid(row=0, column=4, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create a Matplotlib figure and a canvas to embed it in the Tkinter window
fig_right, ax_right = plt.subplots(figsize=(screen_width / 200, screen_height / 150))
canvas_right = FigureCanvasTkAgg(fig_right, master=frame_plot_right)
canvas_widget_right = canvas_right.get_tk_widget()
canvas_widget_right.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))

################################################

# Run the Tkinter event loop
root.mainloop()

