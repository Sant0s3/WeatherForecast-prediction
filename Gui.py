import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
import joblib
import pandas as pd
from PIL import Image, ImageTk
import os
from datetime import datetime

# Load the pre-trained model
model_path = r'D:\Weather api\model\random_forest_weather_predictor.joblib'
model = joblib.load(model_path)

# Create the main window
root = tk.Tk()
root.title("WeatherPredict AI")
root.configure(bg="#f0f5fc")  # Light blue background

# Set the window size and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
root.minsize(800, 600)

# Custom style for widgets
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f0f5fc')
style.configure('TLabel', background='#f0f5fc', font=('Helvetica', 10))
style.configure('Header.TLabel', background='#f0f5fc', font=('Helvetica', 14, 'bold'))
style.configure('Result.TLabel', background='#f0f5fc', font=('Helvetica', 12))
style.configure('TButton', background='#1e88e5', foreground='white', font=('Helvetica', 11, 'bold'))
style.map('TButton', background=[('active', '#0d47a1')])
style.configure('TEntry', padding=5)
style.configure('TCombobox', padding=5)

# Create main frames
header_frame = ttk.Frame(root, style='TFrame')
header_frame.pack(fill='x', padx=20, pady=10)

content_frame = ttk.Frame(root, style='TFrame')
content_frame.pack(fill='both', expand=True, padx=20, pady=10)

input_frame = ttk.Frame(content_frame, style='TFrame', borderwidth=2, relief='groove')
input_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

result_frame = ttk.Frame(content_frame, style='TFrame', borderwidth=2, relief='groove')
result_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

# Header with title and current time
header_label = ttk.Label(header_frame, text="Weather Prediction AI", style='Header.TLabel')
header_label.pack(side='left', pady=10)

def update_time():
    current_time = datetime.now().strftime("%d %b %Y, %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

time_label = ttk.Label(header_frame, text="", style='TLabel')
time_label.pack(side='right', pady=10)
update_time()

# Input section title
input_title = ttk.Label(input_frame, text="Weather Parameters", style='Header.TLabel')
input_title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky='w')

# Function to validate numerical input
def validate_numeric(value):
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False

validate_cmd = root.register(validate_numeric)

# Create the input fields with better layout and validation
ttk.Label(input_frame, text="Wind Speed (km/h):", style='TLabel').grid(row=1, column=0, padx=10, pady=10, sticky='w')
windspeed_entry = ttk.Entry(input_frame, validate="key", validatecommand=(validate_cmd, '%P'))
windspeed_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

ttk.Label(input_frame, text="Wind Direction (°):", style='TLabel').grid(row=2, column=0, padx=10, pady=10, sticky='w')
winddir_entry = ttk.Entry(input_frame, validate="key", validatecommand=(validate_cmd, '%P'))
winddir_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

ttk.Label(input_frame, text="Sea Level Pressure (hPa):", style='TLabel').grid(row=3, column=0, padx=10, pady=10, sticky='w')
sealevelpressure_entry = ttk.Entry(input_frame, validate="key", validatecommand=(validate_cmd, '%P'))
sealevelpressure_entry.grid(row=3, column=1, padx=10, pady=10, sticky='ew')
sealevelpressure_entry.insert(0, "1013")  # Default value

ttk.Label(input_frame, text="Cloud Cover (%):", style='TLabel').grid(row=4, column=0, padx=10, pady=10, sticky='w')
cloudcover_entry = ttk.Entry(input_frame, validate="key", validatecommand=(validate_cmd, '%P'))
cloudcover_entry.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

ttk.Label(input_frame, text="Season:", style='TLabel').grid(row=5, column=0, padx=10, pady=10, sticky='w')
season_var = tk.StringVar(root)
season_var.set("summer")  # Default value
season_combobox = ttk.Combobox(input_frame, textvariable=season_var, 
                               values=["summer", "winter", "spring", "autumn"],
                               state="readonly")
season_combobox.grid(row=5, column=1, padx=10, pady=10, sticky='ew')

# Help text
help_text = ttk.Label(input_frame, text="Enter weather parameters and click 'Predict' to get temperature forecast.", 
                     wraplength=250, foreground="#666666")
help_text.grid(row=6, column=0, columnspan=2, padx=10, pady=(20, 10), sticky='w')

# Create the predict button with modern styling
predict_button = ttk.Button(
    input_frame, 
    text="Predict", 
    command=lambda: predict_weather(),
    style='TButton'
)
predict_button.grid(row=7, column=0, columnspan=2, padx=10, pady=20, sticky='ew')

# Results section title
result_title = ttk.Label(result_frame, text="Prediction Results", style='Header.TLabel')
result_title.pack(anchor='w', padx=20, pady=(10, 20))

# Results content container
results_display = ttk.Frame(result_frame, style='TFrame')
results_display.pack(fill='both', expand=True, padx=20, pady=10)

# Create modern-looking result cards with initial empty values
def create_result_card(parent, title, initial_value="--°C", row=0):
    card_frame = ttk.Frame(parent, style='TFrame', borderwidth=1, relief='groove')
    card_frame.grid(row=row, column=0, padx=10, pady=10, sticky='ew')
    
    title_label = ttk.Label(card_frame, text=title, foreground="#666666")
    title_label.pack(anchor='w', padx=10, pady=(10, 5))
    
    value_label = ttk.Label(card_frame, text=initial_value, style='Result.TLabel')
    value_label.pack(anchor='center', padx=10, pady=(5, 10))
    
    return value_label

temp_min_value = create_result_card(results_display, "Temperature (Min)", row=0)
temp_max_value = create_result_card(results_display, "Temperature (Max)", row=1)
temp_value = create_result_card(results_display, "Current Temperature", row=2)
feels_like_value = create_result_card(results_display, "Feels Like", row=3)

# Results visualization placeholder
viz_frame = ttk.Frame(result_frame, style='TFrame')
viz_frame.pack(fill='x', padx=20, pady=10)

# Configure grid weights to make it responsive
input_frame.grid_columnconfigure(1, weight=1)
results_display.grid_columnconfigure(0, weight=1)

# Function to handle prediction and update the UI
def predict_weather():
    try:
        # Extract inputs from the user
        windspeed = float(windspeed_entry.get())
        winddir = float(winddir_entry.get())
        sealevelpressure = float(sealevelpressure_entry.get())
        season = season_var.get()
        cloudcover = float(cloudcover_entry.get())

        # Validate ranges
        if not (0 <= windspeed <= 200):
            messagebox.showerror("Invalid Input", "Wind speed should be between 0 and 200 km/h")
            return
        if not (0 <= winddir <= 360):
            messagebox.showerror("Invalid Input", "Wind direction should be between 0 and 360 degrees")
            return
        if not (900 <= sealevelpressure <= 1100):
            messagebox.showerror("Invalid Input", "Sea level pressure should be between 900 and 1100 hPa")
            return
        if not (0 <= cloudcover <= 100):
            messagebox.showerror("Invalid Input", "Cloud cover should be between 0 and 100 percent")
            return

        # Prepare the input data
        input_data = pd.DataFrame([[windspeed, winddir, sealevelpressure, season, cloudcover]], 
                                  columns=['windspeed', 'winddir', 'sealevelpressure', 'season', 'cloudcover'])

        # Make prediction
        prediction = model.predict(input_data)

        # Extract prediction results
        tempmin, tempmax, temp, feelslike = prediction[0]

        # Update the prediction labels with values and color coding
        def update_temp_display(label, value, title):
            # Color coding based on temperature
            if value < 0:
                color = "#0d47a1"  # Cold - deep blue
            elif value < 10:
                color = "#2196f3"  # Cool - blue
            elif value < 20:
                color = "#4caf50"  # Mild - green
            elif value < 30:
                color = "#ff9800"  # Warm - orange
            else:
                color = "#f44336"  # Hot - red
                
            label.config(text=f"{value:.1f}°C", foreground=color)

        update_temp_display(temp_min_value, tempmin, "Temperature (Min)")
        update_temp_display(temp_max_value, tempmax, "Temperature (Max)")
        update_temp_display(temp_value, temp, "Current Temperature")
        update_temp_display(feels_like_value, feelslike, "Feels Like")

    except ValueError as e:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values for all fields.")

# Start the Tkinter event loop
root.mainloop()