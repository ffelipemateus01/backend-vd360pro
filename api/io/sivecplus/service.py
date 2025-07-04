from api.io.sivecplus.controller import SivecController

sivec_controller = SivecController()

def start_sivec_service(port_name: str):
    sivec_controller.open(port_name)

def start_record_service():
    sivec_controller.start_record()

def pause_record_service():
    sivec_controller.pause_record()

def send_command_service(port_name: str, command: str):
    sivec_controller.send(port_name, command)
    
def close_sivec_service(port_name: str):
    sivec_controller.close(port_name)