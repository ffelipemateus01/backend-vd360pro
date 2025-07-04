from serial import Serial
from serial import SerialException
from api.io.sivecplus.repository import add_data, clear_data
from api.io.sivecplus.converter import ConvertData
from api.io.sivecplus.models import Data, DataFormatted
from api.io.sivecplus.calibration import ElectrodeCalibration, GyroscopeCalibration
from core.config import SerialConfigs
import threading
import time

class SerialController:
    def __init__(self):
        self.connection = {}
        self.serial_lock = threading.Lock()
        self.recording = False
        self.running = False
        self.electrode_calibration = ElectrodeCalibration()
        self.gyroscope_calibration = GyroscopeCalibration()
        self.converter = ConvertData(self.electrode_calibration, self.gyroscope_calibration)

    def open(self, port_name: str) -> Serial | None:
        try:
            my_serial=Serial(
                port=port_name,
                baudrate=SerialConfigs.baudrate,
                timeout=SerialConfigs.timeout
            )
            print(f'Conectado com sucesso a porta {port_name}')
            clear_data()
            self.connection[port_name] = my_serial
            threading.Thread(target=self.run, args=(port_name,), daemon=True).start()
            return my_serial
        except Exception as e:
            print(f'Houve um problema ao tentar conectar com a serial. {e}')
            raise SerialException(f'Houve um problema ao tentar conectar com a serial. {e}')

    def data_to_data_class(self, data: str) -> Data | None:
        try:
            data_parts = data.split(',')
            values = {}
            for part in data_parts:
                key, value = part.split(':', 1)
                values[key] = value
            data_cls = Data(electrode_1=values['A1'],
                            electrode_2=values['A2'],
                            electrode_3=values['A3'],
                            gyroscope_x=values['GX'],
                            gyroscope_y=values['GY'],
                            gyroscope_z=values['GZ'])
            return data_cls
        except Exception as e:
            raise ValueError(f'Problema na conversão dos dados recebidos. {e}')

    def run(self, port_name: str):
        self.running = True
        print('Escutando...')
        my_serial = self.connection[port_name]
        while my_serial.is_open:
            try:
                with self.serial_lock:
                    if (my_serial.in_waiting > 0):
                        data=my_serial.readline().decode('utf-8').strip()
                        if self.recording:
                            add_data(data)
                        #print(f'Dado lido: {data}')
                        data_cls = self.data_to_data_class(data)
                        data_formatted = self.converter.convert_data(data_cls, self.electrode_calibration, self.gyroscope_calibration)
                        print(f'Data Convertido: {data_formatted}')
                        if not self.running:
                            break        
                    time.sleep(1)
            except Exception as e:
                print(f'Houve um problema ao tentar ler os dados da serial. {e}')
                raise SerialException(f'Houve um problema ao tentar ler os dados da serial. {e}')
        if port_name in self.connection:
            self.connection.pop(port_name)
        self.running = False
            
    def start_record(self):
        if self.connection != {} and not self.recording:
            self.recording = True
            print('Gravação iniciada.')
        else:
            print(f'Houve um problema ao tentar iniciar a gravação.')
            raise SerialException(f'Houve um problema ao tentar iniciar a gravação.')

    def pause_record(self):
        if self.connection != {} and self.recording:
            self.recording = False
            print('Gravação interrompida.')
        else:
            print(f'Houve um problema ao tentar parar a gravação.')
            raise SerialException(f'Houve um problema ao tentar parar a gravação.')
        
    def send(self, port_name:str, command: str):
        try:
            if self.connection[port_name]:
                my_serial = self.connection[port_name]
                my_serial.write(command.encode())
                print(f'Comando {command} enviado com sucesso para porta {port_name}.')
        except Exception as e:
            print(f'Houve um problema ao tentar enviar um comando para serial. {e}')
            raise SerialException(f'Houve um problema ao tentar enviar um comando para serial. {e}')

    def close(self, port_name: str):
        try:
            self.running = False
            if self.connection[port_name]:
                my_serial = self.connection[port_name]
                my_serial.close()
                self.connection.pop(port_name)
                print(f'Conexão com a porta {port_name} encerrada com sucesso.')
        except Exception as e:
            print(f'Houve um problema ao tentar fechar a conexão com a serial. {e}')
            raise SerialException(f'Houve um problema ao tentar fechar a conexão com a serial. {e}')