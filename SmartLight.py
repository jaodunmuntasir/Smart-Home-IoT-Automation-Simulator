import random

class SmartLight:
    def __init__(self, device_id, automation_system):
        self.device_id = device_id
        self.status = "off"
        self.brightness = 0
        self.motion_detected = False
        self.automation_system = automation_system  # Store the automation system instance
        # Initialize status_var
        self.status_var = None

    def turn_on(self):
        try:
            self.status = "on"
            self.brightness = 85  # Set brightness to a fixed value when turned on
            print(f"SmartLight {self.device_id} is turned on. Brightness: {self.brightness}%")
            # Update status_var if defined
            if self.status_var:
                self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")
        except Exception as e:
            print(f"Error turning on SmartLight {self.device_id}: {e}")

    def turn_off(self):
        try:
            self.status = "off"
            self.brightness = 0
            print(f"SmartLight {self.device_id} is turned off.")
            # Update status_var if defined
            if self.status_var:
                self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")
            # Check and start recording through the automation system
            if self.automation_system:
                self.automation_system.check_and_start_recording()
        except Exception as e:
            print(f"Error turning off SmartLight {self.device_id}: {e}")

    def set_brightness(self, brightness):
        try:
            if self.status == "on":
                # Ensure brightness is within the allowed range
                if 0 <= brightness <= 100:
                    self.brightness = brightness
                    print(f"SmartLight {self.device_id} brightness set to {self.brightness}%")
                    # Update status_var if defined
                    if self.status_var:
                        self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")
                else:
                    print(f"Invalid brightness level: {brightness}. Must be between 0 and 100.")
            else:
                print(f"SmartLight {self.device_id} is off. Cannot set brightness.")
        except Exception as e:
            print(f"Error setting brightness for SmartLight {self.device_id}: {e}")

    def detect_motion(self):
        try:
            print(f"SmartLight {self.device_id} detected motion.")
            if self.status == "off":
                self.turn_on()
            return True
        except Exception as e:
            print(f"Error detecting motion for SmartLight {self.device_id}: {e}")
            return False