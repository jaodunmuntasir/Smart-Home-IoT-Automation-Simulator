from SmartLight import SmartLight
from datetime import datetime
import random

class SecurityCamera:
    def __init__(self, device_id, automation_system):
        self.device_id = device_id
        self.status = "off"
        self.recording = False
        self.infrared = False
        self.motion_detected = False
        self.automation_system = automation_system  # Store the automation system instance
        # Initialize status_var
        self.status_var = None

    def turn_on(self):
        self.status = "on"
        print(f"SecurityCamera {self.device_id} is turned on.")
        self.motion_detected = True
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")

    def turn_off(self):
        self.status = "off"
        self.recording = False
        self.infrared = False
        print(f"SecurityCamera {self.device_id} is turned off.")
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")

    def start_recording(self):
        if self.status == "on":
            self.recording = True
            print(f"SecurityCamera {self.device_id} is recording.")
            # Update status_var if defined
            if self.status_var:
                self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")
        else:
            print(f"SecurityCamera {self.device_id} is off. Cannot start recording.")

    def stop_recording(self):
        self.recording = False
        print(f"SecurityCamera {self.device_id} stopped recording.")
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")

    def enable_infrared(self):
        if self.status == "on":
            self.infrared = True
            print(f"SecurityCamera {self.device_id} infrared enabled.")
            # Update status_var if defined
            if self.status_var:
                self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")
        else:
            print(f"SecurityCamera {self.device_id} is off. Cannot enable infrared.")

    def disable_infrared(self):
        self.infrared = False
        print(f"SecurityCamera {self.device_id} infrared disabled.")
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")

    def detect_motion(self):
        print(f"SecurityCamera {self.device_id} detected motion.")
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight) and device.status == "off":
                device.turn_on()
        return True
