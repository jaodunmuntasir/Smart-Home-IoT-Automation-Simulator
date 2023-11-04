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
        self.status = "on"
        self.brightness = 85
        # self.brightness = random.randint(50, 100)
        print(f"SmartLight {self.device_id} is turned on. Brightness: {self.brightness}%")
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")

    def turn_off(self):
        self.status = "off"
        self.brightness = 0
        print(f"SmartLight {self.device_id} is turned off.")
        # Update status_var if defined
        if self.status_var:
            self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")

        self.automation_system.check_and_start_recording()

    def set_brightness(self, brightness):
        if self.status == "on":
            self.brightness = brightness
            print(f"SmartLight {self.device_id} brightness set to {self.brightness}%")
            # Update status_var if defined
            if self.status_var:
                self.status_var.set(f"Status: {self.status}, Brightness: {self.brightness}%")
        else:
            print(f"SmartLight {self.device_id} is off. Cannot set brightness.")

    def detect_motion(self):
        print(f"SmartLight {self.device_id} detected motion.")
        if self.status == "off":
            self.turn_on()
        return True
