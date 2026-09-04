#Livraria do HH

> *"Aloha! Confira os livros incríveis cadastrados pelos usuários (dahoras) do site de seu professor vietnamita."*  
> — H. (Love & Peace!) ✌️

Uma livraria virtual desenvolvida como trabalho da disciplina de **Banco de Dados**, com sistema de CRUD completo, autenticação de usuários e um quiz divertido para liberar o famoso **Selo HH** 🏅.

---

##Tecnologias

| Back-end | Front-end | Banco de Dados |
|----------|-----------|----------------|
| ![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | |
| | ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white) | |

---

##Funcionalidades

- 🔐 **Autenticação de usuários** (cadastro, login e logout)
- 📖 **CRUD completo de livros** (cadastrar, listar, editar e excluir)
- 💬 **Sistema de comentários** nos livros
- 🔍 **Busca** por título, autor ou gênero
- 🏅 **Selo HH** — um quiz de perguntas sobre ESD/OCS que o usuário precisa acertar para poder cadastrar livros
- ♿ **Acessibilidade** seguindo as diretrizes WCAG (contraste, navegação por teclado, labels, etc.)

---

##Estrutura do Projeto

├── app.py # Rotas Flask e lógica da aplicação
├── model.py # Funções de acesso ao banco de dados
├── livraria_HH.db # Banco SQLite (criado automaticamente)
├── templates/ # Páginas HTML (Jinja2)
│ ├── base.html
│ ├── home.html
│ ├── cadastrar.html
│ ├── editar.html
│ ├── meus_livros.html
│ ├── livro_detalhe.html
│ ├── login.html
│ └── registrar.html
└── static/
└── css/
└── style.css # Estilos do projeto

Paleta de cores
Desenvolvida com atenção ao contraste e acessibilidade (verificada no WebAIM Contrast Checker):
🟣 Primária: #534AB7
⚪ Fundo: #F5F5F7
🟢 Sucesso (Selo): #14532D
🔴 Erro: #991B1B
🟡 Foco (acessibilidade): #FF9900

