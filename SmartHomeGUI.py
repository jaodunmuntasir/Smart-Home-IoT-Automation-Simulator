import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
from ttkthemes import ThemedTk
from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera
from AutomationSystem import AutomationSystem
from datetime import datetime

class SmartHomeGUI(ThemedTk):
    def __init__(self, automation_system):
        super().__init__(theme="adapta")

        self.automation_system = automation_system
        self.title("Smart Home IoT Automation Simulator")
        self.geometry("1000x700")

        # Title at the top middle
        tk.Label(self, text="Smart Home IoT Automation Simulator", font=("Bookman Old Style", 16)).pack(pady=10)

        # Set default font to Helvetica
        self.option_add("*Font", "Helvetica 11")

        # Create left and right frames
        self.left_frame = ttk.Frame(self)
        self.right_frame = ttk.Frame(self)

        # Pack the frames into columns
        self.left_frame.pack(side=tk.LEFT, fill="both", expand=True)
        self.right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

        # Add radio buttons for theme selection
        self.theme_var = tk.StringVar(value="Normal Mode")
        ttk.Radiobutton(self.left_frame, text="Normal Mode", variable=self.theme_var,
                        value="Normal Mode", command=self.apply_normal_mode).pack(anchor="w", padx=10, pady=5)
        ttk.Radiobutton(self.left_frame, text="Dark Mode", variable=self.theme_var,
                        value="Dark Mode", command=self.apply_dark_mode).pack(anchor="w", padx=10, pady=5)

        self.light_frame = ttk.LabelFrame(self.right_frame, text="Smart Lights")
        self.thermostat_frame = ttk.LabelFrame(self.right_frame, text="Thermostats")
        self.camera_frame = ttk.LabelFrame(self.right_frame, text="Security Cameras")
        self.log_frame = ttk.LabelFrame(self.left_frame, text="Log")

        self.light_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ttk.Separator(self.right_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=5)  # Separator
        self.thermostat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        ttk.Separator(self.right_frame, orient=tk.HORIZONTAL).pack(fill="x", pady=5)  # Separator
        self.camera_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, width=40, height=10)
        self.log_text.pack(fill="both", expand=True)

        self.add_devices_to_frame()

        # Redirect standard output to log area
        sys.stdout = TextRedirector(self.log_text)

    def apply_normal_mode(self):
        # Set the theme for normal mode
        self.set_theme("adapta")
        self.log_text.config(bg='white', fg='black')

    def apply_dark_mode(self):
        # Set the theme for dark mode
        self.set_theme("black")
        self.log_text.config(bg='black', fg='white')

    def add_devices_to_frame(self):
        # Iterate over devices and add corresponding controls to frames
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight):
                self.add_light_controls(device, self.light_frame)
            elif isinstance(device, Thermostat):
                self.add_thermostat_controls(device, self.thermostat_frame)
            elif isinstance(device, SecurityCamera):
                self.add_camera_controls(device, self.camera_frame)

    def add_light_controls(self, light, frame):
        ttk.Label(frame, text=f"Device: {light.device_id}", font=("Bookman Old Style", 12)).pack(pady=5)
        status_var = tk.StringVar(value=f"Status: {light.status}, Brightness: {light.brightness}%")
        status_label = ttk.Label(frame, textvariable=status_var)
        status_label.pack()

        light.status_var = status_var

        def toggle_light():
            nonlocal status_var
            if light.status == "off":
                light.turn_on()
                brightness_scale.set(light.brightness)  # Set slider to current brightness
            else:
                light.turn_off()
                brightness_scale.set(light.brightness)
            status_var.set(f"Status: {light.status}, Brightness: {light.brightness}%")

        def adjust_brightness(val):
            nonlocal status_var
            light.set_brightness(int(float(val)))
            status_var.set(f"Status: {light.status}, Brightness: {light.brightness}%")

        ttk.Button(frame, text="On/Off", command=toggle_light).pack(padx=10, pady=10)
        brightness_scale = ttk.Scale(frame, from_=0, to=100, command=adjust_brightness)
        brightness_scale.set(light.brightness)
        brightness_scale.pack(padx=10, pady=5)
        ttk.Button(frame, text="Detect Motion Test", command=light.detect_motion).pack(padx=10, pady=10)

    def add_thermostat_controls(self, thermostat, frame):
        ttk.Label(frame, text=f"Device: {thermostat.device_id}", font=("Bookman Old Style", 12)).pack(pady=5)
        status_var = tk.StringVar(value=f"Status: {thermostat.status}, Temperature: {thermostat.temperature}°C")
        status_label = ttk.Label(frame, textvariable=status_var)
        status_label.pack()


        def toggle_thermostat():
            nonlocal status_var
            if thermostat.status == "off":
                thermostat.turn_on()
                temp_scale.set(thermostat.temperature)  # Set slider to current temperature
            else:
                thermostat.turn_off()
                temp_scale.set(thermostat.temperature)  # Set slider to 0 when thermostat is turned off
            status_var.set(f"Status: {thermostat.status}, Temperature: {thermostat.temperature}°C")

        def adjust_temperature(val):
            nonlocal status_var  # Add this line
            thermostat.set_temperature(int(float(val)))
            status_var.set(f"Status: {thermostat.status}, Temperature: {thermostat.temperature}°C")

        ttk.Button(frame, text="On/Off", command=toggle_thermostat).pack(padx=10, pady=10)
        temp_scale = ttk.Scale(frame, from_=10, to=30, command=adjust_temperature)
        temp_scale.set(thermostat.temperature)
        temp_scale.pack(padx=10, pady=5)

    def add_camera_controls(self, camera, frame):
        ttk.Label(frame, text=f"Device: {camera.device_id}", font=("Bookman Old Style", 12)).pack(pady=5)
        # Create a StringVar for the status label and bind it
        camera.status_var = tk.StringVar(
            value=f"Status: {camera.status}, Recording: {camera.recording}, Infrared: {camera.infrared}")
        status_label = ttk.Label(frame, textvariable=camera.status_var)
        status_label.pack()

        def toggle_camera():
            if camera.status == "off":
                camera.turn_on()
            else:
                camera.turn_off()
            camera.status_var.set(
                f"Status: {camera.status}, Recording: {camera.recording}, Infrared: {camera.infrared}")

        def toggle_recording():
            if camera.recording:
                camera.stop_recording()
            else:
                camera.start_recording()
            camera.status_var.set(
                f"Status: {camera.status}, Recording: {camera.recording}, Infrared: {camera.infrared}")

        ttk.Button(frame, text="Camera On/Off", command=toggle_camera).pack(padx=10, pady=10)
        ttk.Button(frame, text="Recording On/Off", command=toggle_recording).pack(padx=10, pady=0)
        ttk.Button(frame, text="Detect Motion Test", command=camera.detect_motion).pack(padx=10, pady=10)

    def simulation_loop(self):
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight) and device.status == "on":
                for cam in self.automation_system.devices:
                    if isinstance(cam, SecurityCamera) and cam.status == "on":
                        if device.brightness < 50 and not cam.infrared:
                            cam.enable_infrared()
                            cam.status_var.set(
                                f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
                            self.log("Infrared enabled.")
                        elif device.brightness >= 50 and cam.infrared:
                            cam.disable_infrared()
                            cam.status_var.set(
                                f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
                            self.log("Infrared disabled.")
        self.update_device_status()
        self.after(1000, self.simulation_loop)

    def update_device_status(self):
        for frame in [self.light_frame, self.thermostat_frame, self.camera_frame]:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Label) and "textvariable" in widget.keys():
                    widget.update_idletasks()

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget
        self.buffer = ""  # Initialize the buffer attribute

    def write(self, str):
        if '\n' in str:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log_message = f"{timestamp} {self.buffer}{str}"
            self.widget.insert(tk.END, log_message)
            self.widget.see(tk.END)
            self.buffer = ""
        else:
            self.buffer += str

    def flush(self):
        pass


# Instantiate devices and automation system
home_automation = AutomationSystem()
light1 = SmartLight("Light1", home_automation)
thermostat1 = Thermostat("Thermostat1", home_automation)
camera1 = SecurityCamera("Camera1", home_automation)

home_automation.add_device(light1)
home_automation.add_device(thermostat1)
home_automation.add_device(camera1)

# Run the GUI
if __name__ == "__main__":
    app = SmartHomeGUI(home_automation)
    app.simulation_loop()
    app.mainloop()


