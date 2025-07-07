from api.io.oto.controller import Otocalorimeter

otocalorimeter = Otocalorimeter()

def start_oto_service(port_name: str):
    otocalorimeter.open(port_name)

def close_oto_service(port_name: str):
    otocalorimeter.close(port_name)

def increase_temp_service(port_name: str):
    otocalorimeter.send(port_name, 'increase')

def decrease_temp_service(port_name: str):
    otocalorimeter.send(port_name, 'decrease')