data_storage = 'api/io/sivecplus/data/data_record.txt'

def add_data(data: str):
    with open(data_storage, 'a', encoding='utf-8') as archive:
        try:
            archive.write(f'{data}\n')
            print(f'Dado arquivado: {data}')
        except Exception as e:
            raise SystemError(f'Erro ao adicionar novos dados ao arquivo.{e}')

def read_data() -> str | None:
    with open(data_storage, 'r', encoding='utf-8') as archive:
        try:
            data = archive.read()
            print(f'Dados lidos: {data}')
            return data
        except Exception as e:
            raise SystemError(f'Erro ao ler os dados gravados.{e}')

def clear_data():
    with open(data_storage, 'w', encoding='utf-8'):
        pass