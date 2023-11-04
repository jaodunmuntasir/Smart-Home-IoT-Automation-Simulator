class Thermostat:
    def __init__(self, device_id, automation_system=None):
        self.device_id = device_id
        self.status = "off"
        self.temperature = 20  # Default temperature
        self.automation_system = automation_system

    def turn_on(self):
        # self.status = "on"
        # print(f"Thermostat {self.device_id} is turned on. Temperature: {self.temperature}°C")
        self.status = "on"
        print(f"Thermostat {self.device_id} is turned on. Temperature: {self.temperature}°C")
        if hasattr(self, 'status_var'):
            self.status_var.set(f"Status: {self.status}, Temperature: {self.temperature}°C")

    def turn_off(self):
        self.status = "off"
        self.temperature = 20  # Reset to default temperature
        print(f"Thermostat {self.device_id} is turned off.")
        if hasattr(self, 'status_var'):
            self.status_var.set(f"Status: {self.status}, Temperature: {self.temperature}°C")

        self.automation_system.check_and_start_recording()

    def set_temperature(self, temperature):
        if self.status == "on":
            self.temperature = temperature
            print(f"Thermostat {self.device_id} temperature set to {self.temperature}°C")
        else:
            print(f"Thermostat {self.device_id} is off. Cannot set temperature.")
