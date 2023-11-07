from SmartLight import SmartLight
from datetime import datetime
import random

class SecurityCameraError(Exception):
    """ Custom exception for security camera errors. """
    pass

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
        self.motion_detected = True
        self._log(f"SecurityCamera {self.device_id} is turned on.")
        self._update_status_var()

    def turn_off(self):
        self.status = "off"
        self.recording = False
        self.infrared = False
        self._log(f"SecurityCamera {self.device_id} is turned off.")
        self._update_status_var()

    def start_recording(self):
        if self.status == "on":
            self.recording = True
            self._log(f"SecurityCamera {self.device_id} is recording.")
            self._update_status_var()
        else:
            self._log(f"SecurityCamera {self.device_id} is off. Cannot start recording.")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self._log(f"SecurityCamera {self.device_id} stopped recording.")
            self._update_status_var()
        else:
            self._log(f"SecurityCamera {self.device_id} is not recording. Cannot stop.")

    def enable_infrared(self):
        if self.status == "on":
            self.infrared = True
            self._log(f"SecurityCamera {self.device_id} infrared enabled.")
            self._update_status_var()
        else:
            self._log(f"SecurityCamera {self.device_id} is off. Cannot enable infrared.")

    def disable_infrared(self):
        if self.infrared:
            self.infrared = False
            self._log(f"SecurityCamera {self.device_id} infrared disabled.")
            self._update_status_var()
        else:
            self._log(f"SecurityCamera {self.device_id} infrared is not enabled. Cannot disable.")

    def detect_motion(self):
        self._log(f"SecurityCamera {self.device_id} detected motion.")
        if self.status == "off":
            self.turn_on()
        if not self.recording:
            try:
                self.start_recording()
            except SecurityCameraError as e:
                self._log(f"Error: {e}")
        return True

    def _update_status_var(self):
        """ Update the status variable if it's defined. """
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Recording: {self.recording}, Infrared: {self.infrared}")

    def _log(self, message):
        """ Log message with timestamp. """
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        full_message = f"{timestamp} {message}"
        print(full_message)