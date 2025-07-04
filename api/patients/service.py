from api.patients.models import Patient
from core.database import connection
import json

def insert_paciente(paciente: Patient) -> Patient | None:
    with connection.cursor() as cursor:
        try:
            cursor = connection.cursor()
            query = 'Insert into pacientes(hospitalid, nome, datanascimento, cpf, cidade, estado, telefone, email, fotopath) values(%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpaciente'
            params = (paciente.hospital_id, paciente.nome, paciente.data_nascimento, paciente.cpf, paciente.cidade, paciente.estado, paciente.telefone, paciente.email, paciente.fotopath)
            cursor.execute(query, params)
            new_id = cursor.fetchone()[0]
            connection.commit()
            paciente_inserido = Patient(**paciente.model_dump())
            paciente_inserido.id = new_id
            print('Python service: Paciente {} inserido com ID={}'.format(paciente_inserido.nome, paciente_inserido.id))
            return paciente_inserido
        except Exception as e:
            connection.rollback()
            print(f'Python service: Houve um problema ao tentar inserir um paciente. {e}')
            return None


page_size = 50 #número de pacientes por linha
def get_all_pacientes(offset: int):
    with connection.cursor() as cursor:
        try:
            query= 'SELECT idPaciente, nome, dataNascimento, cpf, telefone FROM pacientes ORDER BY idPaciente OFFSET %s ROWS FETCH NEXT %s ROWS ONLY'
            params= (offset, page_size)
            cursor.execute(query, params)
            list_pacientes = cursor.fetchall()     
            if list_pacientes is None:
                print('Python service: Banco de dados não retornou nenhum item na lista.')
                return None
            jdata = json.dumps(list_pacientes, default=str)
            print(f'Python service: Lista de pacientes adquirida com sucesso.\n{jdata}')
            return list_pacientes
        except Exception as e:
            connection.rollback()
            print(f'Python service: Houve um problema ao tentar listar os pacientes. {e}')
            return None
        
def get_paciente_by_id(id: int):
    with connection.cursor() as cursor:
        try:
            query= 'SELECT hospitalid, nome, datanascimento, cpf, cidade, estado, telefone, email, fotopath FROM pacientes where idpaciente = %s'
            params= (id,)
            cursor.execute(query, params)
            paciente_data = cursor.fetchone()        
            if paciente_data is None:
                print('Python service: Banco de dados retornou um paciente vazio')
                return None        
            paciente_encontrado = Patient(
                id=id,
                hospital_id=paciente_data[0],
                nome=paciente_data[1],
                data_nascimento=paciente_data[2],
                cpf=paciente_data[3],
                cidade=paciente_data[4],
                estado=paciente_data[5],
                telefone=paciente_data[6],
                email=paciente_data[7],
                fotopath=paciente_data[8]
            )
            print(f'Python service: O paciente {paciente_encontrado.nome} foi encontrado.')
            return paciente_encontrado
        except Exception as e:
            connection.rollback()
            print(f'Python service: Houve um problema ao tentar buscar o paciente. {e}')
            return None
        
def count_pacientes():
    with connection.cursor() as cursor:
        try:
            query='SELECT COUNT(*) FROM pacientes'
            cursor.execute(query)
            (n_pacientes,) = cursor.fetchone()
            if n_pacientes is None:
                print('Python service: Banco de dados retornou um paciente vazio')
                return None
            print(f'Python service: Existem {n_pacientes} pacientes.')
            return n_pacientes
        except Exception as e:
            connection.rollback()
            print(f'Python service: Houve um problema ao tentar contar os paciente. {e}')
            return None
