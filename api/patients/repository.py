from api.patients.models import Patient
from core.exceptions import PatientDbError, PatientNotFound
from core.database import connection
import json

def create_patient(paciente: Patient) -> Patient | None:
    query = 'Insert into pacientes(hospitalid, nome, datanascimento, cpf, cidade, estado, telefone, email, fotopath) values(%s, %s, %s, %s, %s, %s, %s, %s, %s) returning idpaciente'
    params = (paciente.hospital_id, paciente.nome, paciente.data_nascimento, paciente.cpf, paciente.cidade, paciente.estado, paciente.telefone, paciente.email, paciente.fotopath)
    with connection.cursor() as cursor:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            new_id = cursor.fetchone()[0]
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f'Banco de dados: Houve um problema ao tentar inserir um paciente. {e}')
            raise PatientDbError(f'Banco de dados: Houve um problema ao tentar inserir um paciente. {e}')
    paciente_inserido = Patient(**paciente.model_dump())
    paciente_inserido.id = new_id
    print('Banco de dados: Paciente {} inserido com ID={}'.format(paciente_inserido.nome, paciente_inserido.id))
    return paciente_inserido

page_size = 50 #número de pacientes por linha
def get_all_patients(offset: int):
    query= 'SELECT idPaciente, nome, dataNascimento, cpf, telefone FROM pacientes ORDER BY idPaciente OFFSET %s ROWS FETCH NEXT %s ROWS ONLY'
    params= (offset, page_size)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params)
            list_pacientes = cursor.fetchall()     
        except Exception as e:
            connection.rollback()
            print(f'Banco de dados: Houve um problema ao tentar listar os pacientes. {e}')
            raise PatientDbError(f'Banco de dados: Houve um problema ao tentar listar os pacientes. {e}')
        jdata = json.dumps(list_pacientes, default=str)
        print(f'Banco de dados: Lista de pacientes adquirida com sucesso.\n{jdata}')
        return list_pacientes
        
def get_patient_by_id(id: int):
    query= 'SELECT hospitalid, nome, datanascimento, cpf, cidade, estado, telefone, email, fotopath FROM pacientes where idpaciente = %s'
    params= (id,)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query, params)
            paciente_data = cursor.fetchone()        
        except Exception as e:
            connection.rollback()
            print(f'Banco de dados: Houve um problema ao tentar buscar o paciente. {e}')
            raise PatientDbError(f'Banco de dados: Houve um problema ao tentar buscar o paciente. {e}')
    if paciente_data is None:
        print('Banco de dados: Paciente inexistente.')
        raise PatientNotFound('Banco de dados: Paciente inexistente.')
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
        fotopath=paciente_data[8])
    print(f'Banco de dados: O paciente {paciente_encontrado.nome} foi encontrado.')
    return paciente_encontrado
        
def count_patients():
    query='SELECT COUNT(*) FROM pacientes'
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            (n_pacientes,) = cursor.fetchone()
        except Exception as e:
            connection.rollback()
            print(f'Banco de dados: Houve um problema ao tentar contar os paciente. {e}')
            raise PatientDbError(f'Banco de dados: Houve um problema ao tentar contar os paciente. {e}')
        if n_pacientes is None:
            print('Banco de dados: Não há pacientes.')
            raise PatientNotFound('Banco de dados: Não há pacientes.')
        print(f'Banco de dados: Existem {n_pacientes} pacientes.')
        return n_pacientes