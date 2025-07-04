from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

class Patient(BaseModel):
    id: int | None = None
    hospital_id: int | None = None
    nome: str
    data_nascimento: datetime
    cpf: str
    cidade: str
    estado: str
    telefone: str
    email:str
    fotopath:str

    @field_validator('data_nascimento')
    def check_birthday_date(cls, date: datetime) -> datetime:
        if date > datetime.now(timezone.utc):
            raise ValueError("Data de nascimento inválida.")
        return date
    
    @field_validator('email')
    def check_email(cls, email: str) -> str:
        if not '@' in email:
            raise ValueError("Endereço de e-mail inválido.")
        return email
