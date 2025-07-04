from serial import Serial
from serial import SerialException
from api.io.sivecplus.repository import add_data, clear_data
from api.io.sivecplus.converter import ConvertSivecData
from api.io.sivecplus.models import Data, DataFormatted
from api.io.sivecplus.calibration import ElectrodeCalibration, GyroscopeCalibration
from core.config import SerialSivecConfigs
import threading
import time

class SivecController:
    def __init__(self):
        self.connection = {}
        self.serial_lock = threading.Lock()
        self.recording = False
        self.electrode_calibration = ElectrodeCalibration()
        self.gyroscope_calibration = GyroscopeCalibration()
        self.converter = ConvertSivecData(self.electrode_calibration, self.gyroscope_calibration)

    def open(self, port_name: str):
        try:
            sivec=Serial(
                port=port_name,
                baudrate=SerialSivecConfigs.baudrate,
                timeout=SerialSivecConfigs.timeout
            )
            print(f'Sivec: Conectado com sucesso a porta {port_name}')
            clear_data()
            self.connection[port_name] = sivec
            threading.Thread(target=self.run, args=(port_name,), daemon=True).start()
        except Exception as e:
            print(f'Sivec: Houve um problema ao tentar conectar com a serial. {e}')
            raise SerialException(f'Sivec: Houve um problema ao tentar conectar com a serial. {e}')

    def run(self, port_name: str):
        if port_name not in self.connection:
            print(f'Sivec: Tentativa de leitura em porta inexistente.')
            raise SerialException(f'Sivec: Tentativa de leitura em porta inexistente.')
        print('Sivec: Escutando...')
        sivec = self.connection[port_name]
        while sivec.is_open:
            try:
                with self.serial_lock:
                    if (sivec.in_waiting > 0):
                        data=sivec.readline().decode('utf-8').strip()
                        if self.recording:
                            add_data(data)
                        #print(f'Dado lido: {data}')
                        data_cls = self.converter.convert_to_data_cls(data)
                        data_formatted = self.converter.convert_to_data_formatted(data_cls, self.electrode_calibration, self.gyroscope_calibration)
                        print(f'Sivec: Data Convertido: {data_formatted}')
                    time.sleep(1)
            except Exception as e:
                print(f'Sivec: Houve um problema ao tentar ler os dados da serial. {e}')
                raise SerialException(f'Sivec: Houve um problema ao tentar ler os dados da serial. {e}')
        if port_name in self.connection:
            self.connection.pop(port_name)

    def start_record(self):
        if self.connection != {} and not self.recording:
            self.recording = True
            print('Sivec: Gravação iniciada.')
            return
        print(f'Sivec: Houve um problema ao tentar iniciar a gravação.')
        raise SerialException(f'Sivec: Houve um problema ao tentar iniciar a gravação.')

    def pause_record(self):
        if self.connection != {} and self.recording:
            self.recording = False
            print('Sivec: Gravação interrompida.')
            return
        print(f'Sivec: Houve um problema ao tentar parar a gravação.')
        raise SerialException(f'Sivec: Houve um problema ao tentar parar a gravação.')
        
    def send(self, port_name:str, command: str):
        if port_name not in self.connection:
            print(f'Sivec: Tentativa de envio de comandos para porta inexistente.')
            raise SerialException(f'Sivec: Tentativa de envio de comandos para porta inexistente.')
        try:
            sivec = self.connection[port_name]
            sivec.write(command.encode())
            print(f'Sivec: Comando {command} enviado com sucesso para porta {port_name}.')
        except Exception as e:
            print(f'Sivec: Houve um problema ao tentar enviar um comando para serial. {e}')
            raise SerialException(f'Sivec: Houve um problema ao tentar enviar um comando para serial. {e}')

    def close(self, port_name: str):
        if port_name not in self.connection:
            print(f'Sivec: Tentativa de encerramento de porta inexistente.')
            raise SerialException(f'Sivec: Tentativa de encerramento de porta inexistente.')
        try:
            sivec = self.connection[port_name]
            sivec.close()
            self.connection.pop(port_name)
            print(f'Sivec: Conexão com a porta {port_name} encerrada com sucesso.')
        except Exception as e:
            print(f'Sivec: Houve um problema ao tentar fechar a conexão com a serial. {e}')
            raise SerialException(f'Sivec: Houve um problema ao tentar fechar a conexão com a serial. {e}')