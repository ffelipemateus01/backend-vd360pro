from serial import Serial, SerialException
from api.io.oto.models import OtoData
from core.config import SerialOtoConfigs
import threading
import time

class Otocalorimeter:
    def __init__(self):
        self.sensors_data = OtoData(sensor_amb=0.0, sensor_irr=0.0, set_point=24)
        self.connection = {}
        self.serial_lock = threading.Lock()

    def open(self, port_name: str):
        try:
            oto = Serial(port=port_name,
                               baudrate=SerialOtoConfigs.baudrate,
                               timeout=SerialOtoConfigs.timeout)
            self.connection[port_name] = oto
            print(f'Otocalorímetro: Conectado com sucesso a porta {port_name}')
            threading.Thread(target=self.run, args=(port_name,), daemon=True).start() 
        except Exception as e:
            print(f'Otocalorímetro: Houve uma falha ao tentar conectar a porta {port_name}')
            raise SerialException(f'Otocalorímetro: Houve uma falha ao tentar conectar a porta {port_name}. {e}')
        
    def run(self, port_name: str):
        if port_name not in self.connection:
            print(f'Otocalorímetro: Tentiva de leitura em porta inexistente. {e}')
            raise SerialException(f'Otocalorímetro: Tentiva de leitura em porta inexistente. {e}')
        try:
            print('Otocalorímetro: Escutando...')
            oto = self.connection[port_name] 
            while oto.is_open:
                with self.serial_lock:
                    if oto.in_waiting > 0:
                        data = oto.readline().decode('utf8').strip()
                        print(data)
                    time.sleep(1)
        except Exception as e:
            print(f'Otocalorímetro: Houve um problema ao tentar ler os dados da serial. {e}')
            raise SerialException(f'Otocalorímetro: Houve um problema ao tentar ler os dados da serial. {e}')
        
    def close(self, port_name: str):
        if port_name not in self.connection:
            print(f'Otocalorímetro: Tentiva de encerramento de porta inexistente.')
            raise SerialException(f'Otocalorímetro: Tentiva de encerramento de porta inexistente.')
        try:
            oto = self.connection[port_name]
            oto.close()
            self.connection.pop(port_name)
            print(f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.')
        except Exception as e:
            print(f'Otocalorímetro: Houve um problema ao tentar fechar a conexão com a serial. {e}')
            raise SerialException(f'Otocalorímetro: Houve um problema ao tentar fechar a conexão com a serial. {e}')
        