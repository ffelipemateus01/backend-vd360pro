from api.io.sivecplus.controller import SerialController

serial_controller = SerialController()

def start_serial_service(port_name: str):
    serial_controller.open(port_name)

def start_record_service():
    serial_controller.start_record()

def pause_record_service():
    serial_controller.pause_record()

def send_command_service(port_name: str, command: str):
    serial_controller.send(port_name, command)
    
def close_serial_service(port_name: str):
    serial_controller.close(port_name)