from api.io.oto.controller import Otocalorimeter

otocalorimeter = Otocalorimeter()

def start_oto_service(port_name: str):
    otocalorimeter.open(port_name)

def close_oto_service(port_name: str):
    otocalorimeter.close(port_name)