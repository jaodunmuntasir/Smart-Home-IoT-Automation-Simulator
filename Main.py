from SmartLight import SmartLight
from Thermostat import Thermostat
from SecurityCamera import SecurityCamera
from AutomationSystem import AutomationSystem
import time

class SimulationError(Exception):
    """ Custom exception class for simulation errors. """

def simulation_loop(automation_system):
    try:
        while True:
            automation_system.run_simulation()
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulation loop interrupted by user.")
    except Exception as e:
        print(f"An error occurred during simulation: {e}")

def main():
    try:
        home_automation = AutomationSystem()
        # Create instances of IoT devices
        light1 = SmartLight("Light1", home_automation)
        thermostat1 = Thermostat("Thermostat1", home_automation)
        camera1 = SecurityCamera("Camera1", home_automation)

        # Add devices to the automation system
        home_automation.add_device(light1)
        home_automation.add_device(thermostat1)
        home_automation.add_device(camera1)

        # Discover devices
        home_automation.discover_devices()

        # Simulate device behaviors
        light1.turn_on()
        light1.set_brightness(40)
        thermostat1.turn_off()
        camera1.turn_on()  # Ensure the camera is turned on

        # Run simulation loop
        simulation_loop(home_automation)

    except SimulationError as e:
        print(f"Simulation error: {e}")
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")

# Ensure that the main function is only run when this script is executed directly
if __name__ == "__main__":
    main()
