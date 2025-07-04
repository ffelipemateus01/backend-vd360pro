from api.io.sivecplus.models import Data, DataFormatted
from api.io.sivecplus.calibration import ElectrodeCalibration, GyroscopeCalibration

class ConvertSivecData:
    def __init__(self, electrode_calibration: ElectrodeCalibration, gyroscope_calibration: GyroscopeCalibration):
        self.electrode_calibration = electrode_calibration
        self.gyroscope_calibration = gyroscope_calibration

    def convert_to_data_cls(self, data: str) -> Data | None:
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
            print(f'Sivec: Problema na conversão dos dados recebidos. {e}')
            raise ValueError(f'Sivec: Problema na conversão dos dados recebidos. {e}')
        
    def convert_to_data_formatted(self, data: Data, electrode_calibration: ElectrodeCalibration, gyroscope_calibration: GyroscopeCalibration) -> DataFormatted | None:
        data_electrode_1 = (data.electrode_1 - electrode_calibration.base_line_1) * electrode_calibration.bytes_by_degrees_1
        data_electrode_2 = (data.electrode_2 - electrode_calibration.base_line_2) * electrode_calibration.bytes_by_degrees_2
        data_electrode_3 = (data.electrode_3 - electrode_calibration.base_line_3) * electrode_calibration.bytes_by_degrees_3
        data_gyroscope_x = (data.gyroscope_x - gyroscope_calibration.offset_x) / gyroscope_calibration.convert_constant
        data_gyroscope_y = (data.gyroscope_y - gyroscope_calibration.offset_y) / gyroscope_calibration.convert_constant
        data_gyroscope_z = (data.gyroscope_z - gyroscope_calibration.offset_z) / gyroscope_calibration.convert_constant
        data_formatted = DataFormatted(g_electrode_1=data_electrode_1,
                                       g_electrode_2=data_electrode_2,
                                       g_electrode_3=data_electrode_3,
                                       g_gyroscope_x=data_gyroscope_x,
                                       g_gyroscope_y=data_gyroscope_y,
                                       g_gyroscope_z=data_gyroscope_z)
        return data_formatted