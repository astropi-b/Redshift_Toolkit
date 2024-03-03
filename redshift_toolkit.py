import tkinter as tk
from tkinter import ttk

def calculate_redshift(is_wavelength, observed, emitted):
    if is_wavelength:
        return (observed - emitted) / emitted
    else:  # frequency
        return (emitted - observed) / observed

def calculate_observed(redshift, emitted, is_wavelength):
    if is_wavelength:
        return emitted * (1 + redshift)
    else:  # frequency
        return emitted / (1 + redshift)

def calculate_emitted(redshift, observed, is_wavelength):
    if is_wavelength:
        return observed / (1 + redshift)
    else:  # frequency
        return observed * (1 + redshift)

def calculate_distance(redshift):
    c = 3.00e5  # speed of light in km/s
    H_0 = 70  # Hubble constant in km/s/Mpc
    return (c / H_0) * redshift

def update_inputs(*args):
    for widget in input_frame.winfo_children():
        widget.grid_remove()
    operation = operation_var.get()
    if operation == "1":  # Calculate Redshift
        observed_label.grid()
        observed_entry.grid()
        emitted_label.grid()
        emitted_entry.grid()
    elif operation in ["2", "3"]:  # Calculate Observed or Emitted Property
        redshift_label.grid()
        redshift_entry.grid()
        property_label.grid()
        property_entry.grid()

def calculate():
    try:
        operation = operation_var.get()
        is_wavelength = unit_var.get() == "Wavelength (m)"
        c = 3.00e8  # speed of light in m/s  

        if operation == "1":
            observed = float(observed_entry.get())
            emitted = float(emitted_entry.get())
            redshift = calculate_redshift(is_wavelength, observed, emitted)
        else:
            redshift = float(redshift_entry.get())
            if operation == "2":
                prop = float(property_entry.get())
                observed = calculate_observed(redshift, prop, is_wavelength)
            else:  # operation == "3"
                prop = float(property_entry.get())
                observed = calculate_emitted(redshift, prop, is_wavelength)

        distance = calculate_distance(redshift)
        obs_wavelength, obs_freq, emitted_wavelength, emitted_freq = None, None, None, None
        if is_wavelength:
            obs_wavelength = observed
            obs_freq = c / observed / 1e6
            emitted_wavelength = emitted if operation == "1" else None
            emitted_freq = c / emitted / 1e6 if operation == "1" else None
        else:
            obs_freq = observed
            obs_wavelength = c / (observed * 1e6)
            emitted_freq = emitted if operation == "1" else None
            emitted_wavelength = c / (emitted * 1e6) if operation == "1" else None

        # Update the result table
        for i, val in enumerate(["Observed Frequency (MHz)", "Observed Wavelength (m)", "Emitted Frequency (MHz)", 
                                 "Emitted Wavelength (m)", "Redshift", "Distance (Mpc)"]):
            ttk.Label(result_frame, text=val).grid(row=i, column=0, sticky="w")
        
        for i, val in enumerate([f"{obs_freq:.2f}", f"{obs_wavelength:.2e}", f"{emitted_freq:.2f}" if emitted_freq else "", 
                                 f"{emitted_wavelength:.2e}" if emitted_wavelength else "", f"{redshift:.4f}", f"{distance:.2f}"]):
            ttk.Label(result_frame, text=val).grid(row=i, column=1, sticky="w")

    except ValueError as e:
        ttk.Label(result_frame, text="Error in input. Please enter valid numbers.").grid(row=0, column=0, sticky="w")

# GUI setup
# GUI setup
root = tk.Tk()
root.title("Redshift Toolkit")

# Adjust the size of the main window
root.geometry("600x800")  # Width x Height

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, fill="both", expand=True)

operation_var = tk.StringVar(value="1")
unit_var = tk.StringVar(value="Wavelength (m)")

ttk.Label(main_frame, text="Select Operation:").grid(row=0, column=0, sticky="w", columnspan=2)
ttk.Radiobutton(main_frame, text="Calculate Redshift", variable=operation_var, value="1").grid(row=1, column=0, sticky="w")
ttk.Radiobutton(main_frame, text="Calculate Observed Wavelength/Frequency(as selected)", variable=operation_var, value="2").grid(row=2, column=0, sticky="w")
ttk.Radiobutton(main_frame, text="Calculate Emitted Wavelength/Frequency(as selected)", variable=operation_var, value="3").grid(row=3, column=0, sticky="w")

ttk.Label(main_frame, text="Select Unit:").grid(row=4, column=0, sticky="w", columnspan=2)
ttk.Radiobutton(main_frame, text="Wavelength (m)", variable=unit_var, value="Wavelength (m)").grid(row=5, column=0, sticky="w")
ttk.Radiobutton(main_frame, text="Frequency (MHz)", variable=unit_var, value="Frequency (MHz)").grid(row=6, column=0, sticky="w")

input_frame = ttk.Frame(main_frame)
input_frame.grid(row=7, column=0, columnspan=2, sticky="ew")

observed_label = ttk.Label(input_frame, text="Observed Wavelength/Frequency(as selected):")
observed_entry = ttk.Entry(input_frame)
emitted_label = ttk.Label(input_frame, text="Emitted Wavelength/Frequency(as selected):")
emitted_entry = ttk.Entry(input_frame)
redshift_label = ttk.Label(input_frame, text="Redshift:")
redshift_entry = ttk.Entry(input_frame)
property_label = ttk.Label(input_frame, text="Observed/Emistted Wavelength/Frequency(as selected):")
property_entry = ttk.Entry(input_frame)

ttk.Button(main_frame, text="Calculate", command=calculate).grid(row=8, column=0, columnspan=2, pady=10)

result_frame = ttk.Frame(main_frame)
result_frame.grid(row=9, column=0, columnspan=2, sticky="ew")

operation_var.trace('w', update_inputs)  # Update inputs when operation changes
update_inputs()  # Initialize inputs based on the default operation

# Additional frame or text widget for displaying formulas and constants
formulas_frame = ttk.Frame(main_frame)
formulas_frame.grid(row=10, column=0, columnspan=2, sticky="ew")

formulas_text = tk.Text(formulas_frame, height=15, wrap="word")
formulas_text.pack(fill="both", expand=True)

# Inserting text into the formulas_text widget
formulas = """
Formulas Used:
- Redshift (z) = (λ_observed - λ_emitted) / λ_emitted [for wavelength]
- Redshift (z) = (f_emitted - f_observed) / f_observed [for frequency]
- Observed λ = λ_emitted * (1 + z) [for wavelength]
- Observed f = f_emitted / (1 + z) [for frequency]
- Distance (D) = (c / H_0) * z

Constants:
- Speed of Light (c) = 3.00e5 km/s
- Hubble Constant (H_0) = 70 km/s/Mpc
"""
formulas_text.insert("1.0", formulas)

# Make the text widget read-only
formulas_text.config(state="disabled")

 
# Label for your name and email
# Use a Label widget to display your name and email, and manage it with `grid`
credits_text = "Anumanchi Agastya Sai Ram Likhit\n astropi.2003@gmail.com"
credits_label = ttk.Label(main_frame, text=credits_text)
credits_label.grid(row=11, column=0, columnspan=2, pady=(10, 0))  # Adjust row index as needed

 

root.mainloop()
 