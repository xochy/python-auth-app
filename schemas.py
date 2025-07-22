from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Esquema base para usuario (atributos comunes)
class UserBase(BaseModel):
    username: str
    email: EmailStr # Valida que sea un formato de correo electrónico

# Esquema para crear un nuevo usuario (incluye la contraseña)
class UserCreate(UserBase):
    password: str

# Esquema para la respuesta de usuario (NO incluye la contraseña hasheada)
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True # Permite que Pydantic lea datos directamente de un modelo ORM

# Esquema para el inicio de sesión
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para el token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str

# Esquema para los datos del token
class TokenData(BaseModel):
    username: str | None = None

# Belvo Schemas
# Esquema para Institution (Instituciones)
class Institution(BaseModel):
    id: int
    name: str
    type: str
    website: Optional[str] = None
    display_name: str
    country_codes: List[str]
    primary_color: Optional[str] = None
    logo: Optional[str] = None
    icon_logo: Optional[str] = None
    text_logo: Optional[str] = None
    status: str

# Sub-esquemas para Account y Transaction
class AccountInstitution(BaseModel):
    name: str
    type: str

class AccountBalance(BaseModel):
    current: float
    available: float

# Esquema para Account (Cuentas)
class Account(BaseModel):
    id: str
    link: str
    institution: AccountInstitution
    category: str
    type: str
    name: str
    number: str
    currency: str
    balance: AccountBalance

# Esquema para Balance (Balances)
class Balance(BaseModel):
    id: str
    link: str
    account_id: str
    currency: str
    available: float
    blocked: float
    automatically_invested: float

# Sub-esquemas para Transaction
class TransactionAccount(BaseModel):
    id: str
    link: str
    institution: AccountInstitution # Reutiliza el esquema de institución de cuenta
    name: str
    number: str
    currency: str
    balance: AccountBalance # Reutiliza el esquema de balance de cuenta

# Esquema para Transaction (Transacciones)
class Transaction(BaseModel):
    id: str
    account: TransactionAccount
    amount: float
    currency: str
    description: str
    value_date: str
    type: str
    status: str
    category: str
    subcategory: Optional[str] = None