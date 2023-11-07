class InvalidTemperatureError(Exception):
    """Exception raised when an invalid temperature is set for the thermostat."""
    pass

class Thermostat:
    def __init__(self, device_id, automation_system=None):
        self.device_id = device_id
        self.status = "off"
        self.temperature = 20  # Default temperature
        self.automation_system = automation_system
        # Initialize status_var
        self.status_var = None

    def turn_on(self):
        self.status = "on"
        print(f"Thermostat {self.device_id} is turned on. Temperature: {self.temperature}°C")
        self._update_status_var()

    def turn_off(self):
        self.status = "off"
        self.temperature = 20  # Reset to default temperature
        print(f"Thermostat {self.device_id} is turned off.")
        self._update_status_var()
        if self.automation_system:
            try:
                self.automation_system.check_and_start_recording()
            except Exception as e:
                print(f"Error while trying to start recording: {e}")

    def set_temperature(self, temperature):
        try:
            temperature = int(temperature)
            if not 10 <= temperature <= 30:
                raise InvalidTemperatureError("Temperature must be between 10°C and 30°C.")
        except ValueError:
            print(f"Invalid temperature input: {temperature}")
            return
        except InvalidTemperatureError as e:
            print(e)
            return

        if self.status == "on":
            self.temperature = temperature
            print(f"Thermostat {self.device_id} temperature set to {self.temperature}°C")
            self._update_status_var()
        else:
            print(f"Thermostat {self.device_id} is off. Cannot set temperature.")

    def _update_status_var(self):
        if hasattr(self, 'status_var') and self.status_var:
            self.status_var.set(f"Status: {self.status}, Temperature: {self.temperature}°C")