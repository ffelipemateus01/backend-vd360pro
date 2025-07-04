from api.io.sivecplus.models import Data, DataFormatted
from api.io.sivecplus.calibration import ElectrodeCalibration, GyroscopeCalibration
import json

electrode_calibration = ElectrodeCalibration()
gyroscope_calibration = GyroscopeCalibration()

class ConvertData:
    def convert_data(data: Data) -> DataFormatted | None:
        data_electrode_1 = (data.electrode_1 - electrode_calibration.base_line_1) * electrode_calibration.bytes_by_degrees_1
        data_electrode_2 = (data.electrode_2 - electrode_calibration.base_line_2) * electrode_calibration.bytes_by_degrees_2
        data_electrode_3 = (data.electrode_3 - electrode_calibration.base_line_3) * electrode_calibration.bytes_by_degrees_3
        data_gyroscope_x = (data.gyroscope_x - gyroscope_calibration.offset_x) / gyroscope_calibration.convert_constant
        data_gyroscope_y = (data.gyroscope_y - gyroscope_calibration.offset_y) / gyroscope_calibration.convert_constant
        data_gyroscope_z = (data.gyroscope_z - gyroscope_calibration.offset_z) / gyroscope_calibration.convert_constant
        data_formatted = DataFormatted(data_electrode_1, data_electrode_2, data_electrode_3, data_gyroscope_x, data_gyroscope_y, data_gyroscope_z)
        print(f'Data Formatted: {json.dumps(data_formatted)}')
        return data_formatted