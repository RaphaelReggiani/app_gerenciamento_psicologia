from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from collections import Counter


def name_validator(value):
    if not value or value.strip() == "":
        raise ValidationError("O campo deve ser preenchido.")

    words = value.strip().split()

    if len(words) < 2:
        raise ValidationError("O campo 'nome' deve conter o nome completo.")

    for word in words:
        if len(word) < 3:
            raise ValidationError("O nome deve conter no mínimo 3 caracteres.")
        if not word.isalpha():
            raise ValidationError("Não pode conter números ou caracteres especiais.")

def email_validator(value):
    if not value or value.strip() == "":
        raise ValidationError("O campo de e-mail deve ser preenchdio.")

    if "@" not in value:
        raise ValidationError("O e-mail deve conter @exemplo.com.")

    local_part = value.split("@")[0]

    if not local_part:
        raise ValidationError("O e-mail deve conter os dados antes do '@'.")

    if " " in value:
        raise ValidationError("Não pode conter espaços.")

    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        raise ValidationError("Insira uma e-mail válido.")

def validate_password_rules(value):
    if not (6 <= len(value) <= 12):
        raise ValidationError("A senha deve conter entra 6 e 12 caracteres.")

    if not re.search(r'\d', value):
        raise ValidationError("A senha deve ter pelo menos 1 número.")

    if not re.search(r'[!@#$%^&*()_\-+=\[\]{};:,.<>?/\\|`~]', value):
        raise ValidationError("A senha deve ter pelo menos 1 caracter especial (#@!...)")

    counter = Counter(value)
    for char, count in counter.items():
        if count > 2:
            raise ValidationError(f"O caracter '{char}' foi repetido mais de 2 vezes.")
        
nickname_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]{5,15}$',
    message="O nome de usuário deve ter de 5-15 caracteres (apenas letras e/ou números)."
)

phone_validator = RegexValidator(regex=r'^\(\d{3}\)\s?\d{9}$',message="O número deve estar no formato: (011) 000000000")