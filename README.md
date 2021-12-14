# KENZIEDOC - Descrição:

A aplicação KenzieDoc se propõe a cadastrar médicos, pacientes de agendar consultas de maneira simples e intuitiva.
O objetivo da aplicação é ser uma ferramente em que o médico cadastra sua especialidade e seus locais de atendimento e o paciente pode buscar por especialidade, pelo nome do médico e por seu endereço e agendar a consulta de forma confortável , prática e rápida.

# Primeiros passos:

##

Como instalar

##

Após feito o clone da Kenziedoc instalar no terminal:

1. O arquivo oculto .env:

```
touch .env
```

E nele configurar os seguintes comandos:

```
FLASK_ENV=development

SQLALCHEMY_DATABASE_URI="postgresql://SEU_NOME_DE_USUARIO:SUA_SENHA_DE_USUÁRIO@localhost:5432/SEU_BANCO_DE_DADOS"
SQLALCHEMY_TRACK_MODIFICATIONS=""
SECRET_KEY=SUA_SENHA(qualquer uma)
```

2. O ambiente virtual e atualizar suas dependências com o seguinte comando:

```
python -m venv venv --upgrade-deps
```

Abra seu ambiente virtual:

```
source/venv/bin/activate
```

3. Feitas as instalações acima instalar recursivamente as demais dependências deste modo:

```
pip install -r requirements.txt
```

# Documentação:

Para ter acesso às descrições dos requests mais detalhes conferir documentação completa no link a seguir:

https://manual-api-kenziedoc.vercel.app/

# Observações:

Esta aplicação tem fins didáticos e não se destina a fins comerciais.
