from serial import Serial
from core.exceptions import OtoError, OtoIndexError
from api.io.oto.models import OtoData
from api.io.oto.converter import ConvertOtoData
from core.config import SerialOtoConfigs
import threading
import time

class Otocalorimeter:
    def __init__(self):
        self.sensors_data = OtoData(sensor_amb=0.0, sensor_irr=0.0, set_point=24)
        self.connection = {}
        self.converter = ConvertOtoData()
        self.serial_lock = threading.Lock()
        self.commands = {'increase':'ssr3d','decrease':'ssr3d'}

    def open(self, port_name: str):
        try:
            oto = Serial(port=port_name,
                               baudrate=SerialOtoConfigs.baudrate,
                               timeout=SerialOtoConfigs.timeout)
        except Exception as e:
            print(f'Otocalorímetro: Houve uma falha ao tentar conectar a porta {port_name}')
            raise OtoError(f'Otocalorímetro: Houve uma falha ao tentar conectar a porta {port_name}. {e}')
        self.connection[port_name] = oto
        print(f'Otocalorímetro: Conectado com sucesso a porta {port_name}')
        threading.Thread(target=self.run, args=(port_name,), daemon=True).start() 
        
    def run(self, port_name: str):
        if port_name not in self.connection:
            print(f'Otocalorímetro: Tentiva de leitura em porta inexistente. {e}')
            raise OtoIndexError(f'Otocalorímetro: Tentiva de leitura em porta inexistente. {e}')
        oto = self.connection[port_name] 
        print('Otocalorímetro: Escutando...')
        while oto.is_open:
            try:
                with self.serial_lock:
                    if oto.in_waiting > 0:
                        data = oto.readline().decode('utf8').strip()
            except Exception as e:
                print(f'Otocalorímetro: Houve um problema ao tentar ler os dados da serial. {e}')
                raise OtoError(f'Otocalorímetro: Houve um problema ao tentar ler os dados da serial. {e}')
            time.sleep(1)
            data = 'set_point:24,sensor_irr:23,sensor_amb:20'
            data_cls = self.converter.convert_to_data_cls(data)
            print(data_cls)
        if port_name in self.connection:
            self.connection.pop(port_name)
        
    def send(self, port_name: str, action: str):
        if port_name not in self.connection:
            print(f'Otocalorímetro: Tentiva de envio de comando para porta inexistente.')
            raise OtoIndexError(f'Otocalorímetro: Tentiva de envio de comando para porta inexistente.')
        command = self.commands[action]
        oto = self.connection[port_name]
        try:
            oto.write(command.encode())
            print(f'Otocalorímetro: Comando {command} enviado com sucesso para a porta {port_name}')
        except Exception as e:
            print(f'Otocalorímetro: Houve um problema ao tentar enviar um comando para serial. {e}')
            raise OtoError(f'Otocalorímetro: Houve um problema ao tentar enviar um comando para serial. {e}')
        
    def close(self, port_name: str):
        if port_name not in self.connection:
            print(f'Otocalorímetro: Tentiva de encerramento de porta inexistente.')
            raise OtoIndexError(f'Otocalorímetro: Tentiva de encerramento de porta inexistente.')
        oto = self.connection[port_name]
        try:
            oto.close()
        except Exception as e:
            print(f'Otocalorímetro: Houve um problema ao tentar fechar a conexão com a serial. {e}')
            raise OtoError(f'Otocalorímetro: Houve um problema ao tentar fechar a conexão com a serial. {e}')
        self.connection.pop(port_name)
        print(f'Otocalorímetro: Conexão com a porta {port_name} encerrada com sucesso.')
        