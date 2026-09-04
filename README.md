# Sistema de Livraria (CRUD)

Sistema web simples para gerenciamento de acervo de livros, desenvolvido como **Trabalho 2** da disciplina de **Banco de Dados**. O projeto aplica conceitos de modelagem relacional e desenvolvimento web, oferecendo um CRUD completo com foco em usabilidade e acessibilidade.

---

## Tecnologias Utilizadas

| Back-end | Front-end | Banco de Dados |
|----------|-----------|----------------|
| ![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white) |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) | |
| | ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white) | |

---

## Funcionalidades (CRUD)

- 🔐 **Autenticação de usuários** (cadastro e login).
- 📖 **Criar (Create):** Formulário para cadastro de novos livros.
- 🔍 **Ler (Read):** Listagem de livros com campo de busca por título, autor ou gênero.
- ✏️ **Atualizar (Update):** Edição de dados de livros já cadastrados.
- 🗑️ **Excluir (Delete):** Remoção de registros com validação de propriedade.
- 💬 **Comentários:** Sistema de interação nos detalhes de cada livro.
- ♿ **Acessibilidade:** Projeto desenvolvido seguindo diretrizes WCAG (contraste de cores, navegação por teclado, labels em formulários e HTML semântico).

---

## Estrutura do Projeto

```text
projeto-livraria/
├── app.py                # Rotas Flask e lógica da aplicação
├── model.py              # Funções de acesso e manipulação do banco de dados
├── livraria.db           # Banco SQLite 
├── templates/            # Páginas HTML (Jinja2)
│   ├── base.html
│   ├── home.html
│   ├── cadastrar.html
│   ├── editar.html
│   ├── meus_livros.html
│   ├── livro_detalhe.html
│   ├── login.html
│   └── registrar.html
└── static/
    └── css/
        └── style.css     # Estilos globais do projeto
```
Paleta de cores
Desenvolvida com atenção ao contraste e acessibilidade (verificada no WebAIM Contrast Checker):
🟣 Primária: #534AB7
⚪ Fundo: #F5F5F7
🟢 Sucesso (Selo): #14532D
🔴 Erro: #991B1B
🟡 Foco (acessibilidade): #FF9900

