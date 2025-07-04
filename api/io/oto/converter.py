from api.io.oto.models import OtoData

class ConvertOtoData():
    def convert_to_data_cls(data: str) -> OtoData | None:
        values = {}
        data_parts = data.split(',')
        for parts in data_parts:
            key, value = parts.split(':') #Conferir entrada de dados
            values[key] = value
        data_cls = OtoData(
            set_point = values['set_point']
            sensor_irr = values['sensor_irr']
            sensor_amb = values['amb']
        )
        return data_cls

