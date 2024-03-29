## kenzie_doc_flask

- [Sobre](#sobre)
- [Instalação](#instalação)
- [Documentação](#documentação)
- [Desenvolvedores da API](#desenvolvedores-da-api)
- [Termos de uso](#termos-de-uso)

<br>

# Sobre

<p>A API <b>kenzie_doc_flask</b> se propõe a cadastrar médicos e pacientes na plataforma possibilitando o agendamento de consultas de maneira simples e intuitiva, além de fazer a gestão de consultas agendadas e a da lista de espera.
 
O objetivo da aplicação é ser uma ferramenta que possibilite o profissional de saúde cadastrar sua especialidade e seus locais de atendimento e possibilitar ao paciente  fazer uma busca pelo profissional mais adequado para sua necessidade e  agendar a consulta de forma confortável, prática e rápida.

Esta API utiliza o framework python <b>Flask</b>, o ORM <b>SQLAlchemy</b>, o adaptador de banco de dados <b>Psycopg2</b> e a lib para comunicação via whatsapp <strong>PyWhatKit</strong>.
</p>
<br>

# Instalação

Após feito o clone do repositório Kenziedoc , instalar :

1. O arquivo oculto <b>.env<b> com o comando:

```
touch .env
```

dentro do arquivo .env configurar os seguintes comandos:

```
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI="postgresql://SEU_NOME_DE_USUARIO:SUA_SENHA_DE_USUÁRIO@localhost:5432/SEU_BANCO_DE_DADOS"
SQLALCHEMY_TRACK_MODIFICATIONS=""

```

2. O ambiente virtual e atualizar suas dependências com o seguinte comando:

```
python -m venv venv --upgrade-deps
```

ative o seu ambiente virtual com o comando:

```
source/venv/bin/activate
```

3. recursivamente as dependências do projeto com o comando :

```
pip install -r requirements.txt
```

# Documentação

Para ter acesso ao descrições detalhes das rotas e seus retornos, conferir documentação completa no link a seguir:

https://manual-api-kenziedoc.vercel.app/

# Desenvolvedores da API

 <div align = "center"> 
     <img  align = "center"  alt ="catCoding" src = "https://camo.githubusercontent.com/8a0f84184f42bfa158b242b4561e4f7ce17183cc4684258fa3eb33993ca0dc63/68747470733a2f2f6d656469612e67697068792e636f6d2f6d656469612f756c6534766863593178454b512f67697068792e676966" height: "30" width="150" >
  </div>

<div> 
<span>André Kuratomi  </span><div> 
<a href="https://www.linkedin.com/in/andre-kuratomi/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/AndreKuratomi"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a> 
 
<p>David Avanci </p>
<a href="https://www.linkedin.com/in/davidavanci/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/DavidAvanci"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>

<p>Keila Passos</p> 
<a href="https://www.linkedin.com/in/keila-aparecida-rodrigues-passos" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/keilapassos"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a> 
 
<p>Leonardo Pereira</p>
<a href="https://www.linkedin.com/in/leonardo-m-pereira/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/leokito"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>

<p>Nicole Pimenta </p>
<a href="https://www.linkedin.com/in/keila-aparecida-rodrigues-passos" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/nicole-pimenta"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>

<p>Pierre Kalil  </p>
<a href="https://www.linkedin.com/in/pierre-kalil/" target="_blank" ><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
  <a href = "https://github.com/Pierre-Kalil"><img src="https://www.kindpng.com/picc/m/128-1280187_github-logo-png-github-transparent-png.png" width= 106px height=27px target="_blank"> </a>

# Termos de uso

Esse projeto atende a fins exclusivamente didáticos e sem nenhum intuito comercial.
