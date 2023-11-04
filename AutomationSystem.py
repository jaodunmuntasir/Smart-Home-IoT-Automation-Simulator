from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera

class AutomationSystem:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)
        print(f"Device {device.device_id} added to the automation system.")
        device.automation_system = self  # Pass the automation system instance to the devices

    def discover_devices(self):
        print("Discovering devices...")
        for device in self.devices:
            print(f"Device ID: {device.device_id}, Type: {type(device).__name__}")

    def run_simulation(self):
        print("Running simulation...")
        for device in self.devices:

            if isinstance(device, SmartLight) and device.status == "on" and device.brightness < 50:
                for cam in self.devices:
                    if isinstance(cam, SecurityCamera):
                        cam.enable_infrared()
                        cam.status_var.set(
                            f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")

            if isinstance(device, Thermostat) and device.status == "off":
                lights_off = all(isinstance(light, SmartLight) and light.status == "off" for light in self.devices)
                if lights_off:
                    for cam in self.devices:
                        if isinstance(cam, SecurityCamera) and cam.status == "on":
                            cam.start_recording()
                            cam.status_var.set(
                                f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")

            lights_off = all(isinstance(device, SmartLight) and device.status == "off" for device in self.devices)
            thermostat_off = all(isinstance(device, Thermostat) and device.status == "off" for device in self.devices)

            if lights_off and thermostat_off:
                for cam in self.devices:
                    if isinstance(cam, SecurityCamera) and cam.status == "on" and not cam.recording:
                        cam.start_recording()

    def check_and_start_recording(self):
        lights_on = any(isinstance(device, SmartLight) and device.status == "on" for device in self.devices)
        thermostat_on = any(isinstance(device, Thermostat) and device.status == "on" for device in self.devices)

        print("Checking conditions...")
        if not lights_on and not thermostat_on:
            print("Both lights and thermostat are off.")
            for cam in self.devices:
                if isinstance(cam, SecurityCamera):
                    print("Found a security camera.")
                    if cam.status == "off":
                        print("Camera is off. Turning on...")
                        cam.turn_on()
                    if not cam.recording:
                        print("Camera is not recording. Starting recording...")
                        cam.start_recording()
                    cam.status_var.set(f"Status: {cam.status}, Recording: {cam.recording}, Infrared: {cam.infrared}")
        else:
            print("Not all lights and thermostat are off.")

    def run_automation_rules(self):
        print("Checking conditions for automation rules...")
        lights_off = all(isinstance(device, SmartLight) and device.status == "off" for device in self.devices)
        thermostats_off = all(isinstance(device, Thermostat) and device.status == "off" for device in self.devices)

        if lights_off and thermostats_off:
            print("Both lights and thermostats are off.")
            for device in self.devices:
                if isinstance(device, SecurityCamera):
                    if device.status == "off":
                        print("Camera is off. Turning on the camera...")
                        device.turn_on()
                    print("Starting recording...")
                    device.start_recording()
        else:
            print("Conditions not met for starting camera recording.")
