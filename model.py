import sqlite3

DB_NAME = 'livraria_HH.db'

def init_db():
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute('PRAGMA foreign_keys = ON')  # ativa a checagem de foreign key
    cursor = conexao.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS usuario(
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR NOT NULL,
        senha VARCHAR NOT NULL,
        selo_aprovado INTEGER NOT NULL DEFAULT 0
        )  
        '''
    )#o selo de aprovado quando é criado esta nao aprovado

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS livro(
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo VARCHAR NOT NULL,
        autor VARCHAR,
        genero VARCHAR NOT NULL,
        ano_publicacao VARCHAR,
        preco REAL NOT NULL,
        status VARCHAR NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
        '''
    )#no caso eu pensei caso nao coloquem nome do autor dar "nao definido" e data da "indefinido", fui pesquisar tmb e REAL é o DOUBLE do sqlite

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS comentario(
        id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
        texto VARCHAR NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id_livro INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_livro) REFERENCES livro(id_livro),
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
        )
        '''
    )#comentario liga livro e usuario: quem ainda nao tem selo pode comentar mesmo sem poder postar livro

    conexao.commit()
    conexao.close()

def cadastrar_livro(titulo, autor, genero, ano_publicacao, preco, status, id_usuario):
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute('PRAGMA foreign_keys = ON')
    cursor = conexao.cursor()

    cursor.execute(
        '''
        INSERT INTO livro (Titulo, Autor, Genero, Ano_Publicacao, Preco, Status, Id_Usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, autor, genero, ano_publicacao, preco, status, id_usuario)
    )
    conexao.commit()
    conexao.close()

def usuario_existe(nome):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        'SELECT id_usuario FROM usuario WHERE nome = ?',
        (nome,)
    )
    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None  # True se já existe

def criar_usuario(nome, senha):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO usuario (nome, senha) VALUES (?, ?)',
        (nome, senha)
    )
    conexao.commit()
    conexao.close()

def fazer_loguin(nome, senha):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        'SELECT id_usuario, nome, selo_aprovado FROM usuario WHERE nome = ? AND senha = ?',
        (nome, senha)
    )
    usuario = cursor.fetchone() #resultado select
    conexao.close()
    return usuario  # None se não encontrar

def listar_livros(busca=None):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()

    if busca: #se tiver busca, mostra o que a pessoa esta pesquisando
        termo = f'%{busca}%'
        cursor.execute(
            '''
            SELECT livro.id_livro, livro.titulo, livro.autor, livro.genero,
            livro.ano_publicacao, livro.preco, livro.status,
            usuario.nome, usuario.selo_aprovado
            FROM livro
            JOIN usuario ON livro.id_usuario = usuario.id_usuario
            WHERE livro.titulo LIKE ? OR livro.autor LIKE ? OR livro.genero LIKE ?
            ORDER BY livro.id_livro DESC
            ''', (termo, termo, termo)
        )
    else: #se nao mostra tudo, nao busca por titulo autor ou genero
        cursor.execute(
            '''
            SELECT livro.id_livro, livro.titulo, livro.autor, livro.genero,
            livro.ano_publicacao, livro.preco, livro.status,
            usuario.nome, usuario.selo_aprovado
            FROM livro
            JOIN usuario ON livro.id_usuario = usuario.id_usuario
            ORDER BY livro.id_livro DESC
            '''
        )

    livros = cursor.fetchall()
    conexao.close()
    return livros


def listar_livros_usuario(id_usuario):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        '''
        SELECT id_livro, titulo, autor, genero, ano_publicacao, preco, status
        FROM livro
        WHERE id_usuario = ?
        ORDER BY id_livro DESC
        ''', (id_usuario,)
    )
    livros = cursor.fetchall()
    conexao.close()
    return livros

def excluir_livro(id_livro, id_usuario):
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute('PRAGMA foreign_keys = ON')
    cursor = conexao.cursor()
    cursor.execute(
        'DELETE FROM livro WHERE id_livro = ? AND id_usuario = ?',
        (id_livro, id_usuario)
    )
    conexao.commit()
    conexao.close()

def buscar_livro(id_livro, id_usuario):
    # busca um livro só, pra pre preencher o formulario de edição
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        '''
        SELECT id_livro, titulo, autor, genero, ano_publicacao, preco, status
        FROM livro
        WHERE id_livro = ? AND id_usuario = ?
        ''', (id_livro, id_usuario)
    )
    livro = cursor.fetchone()
    conexao.close()
    return livro  # None se não encontrar 

def editar_livro(id_livro, titulo, autor, genero, ano_publicacao, preco, id_usuario):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        '''
        UPDATE livro
        SET titulo = ?, autor = ?, genero = ?, ano_publicacao = ?, preco = ?
        WHERE id_livro = ? AND id_usuario = ?
        ''', (titulo, autor, genero, ano_publicacao, preco, id_livro, id_usuario)
    ) # so o dono do livro pode editar ele
    conexao.commit()
    conexao.close()

def buscar_livro_por_id(id_livro):
    # busca um livro pra pagina de detalhe publica, sem checar dono
    # (diferente de buscar_livro, que so retorna se for do id_usuario da sessao)
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        '''
        SELECT livro.id_livro, livro.titulo, livro.autor, livro.genero,
        livro.ano_publicacao, livro.preco, livro.status,
        usuario.nome, usuario.selo_aprovado, livro.id_usuario
        FROM livro
        JOIN usuario ON livro.id_usuario = usuario.id_usuario
        WHERE livro.id_livro = ?
        ''', (id_livro,)
    )
    livro = cursor.fetchone()
    conexao.close()
    return livro  # None se não encontrar

def adicionar_comentario(id_livro, id_usuario, texto):
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute('PRAGMA foreign_keys = ON')
    cursor = conexao.cursor()
    cursor.execute(
        'INSERT INTO comentario (texto, id_livro, id_usuario) VALUES (?, ?, ?)',
        (texto, id_livro, id_usuario)
    )
    conexao.commit()
    conexao.close()

def listar_comentarios(id_livro):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        '''
        SELECT comentario.id_comentario, comentario.texto, comentario.data_criacao,
        comentario.id_usuario, usuario.nome, usuario.selo_aprovado
        FROM comentario
        JOIN usuario ON comentario.id_usuario = usuario.id_usuario
        WHERE comentario.id_livro = ?
        ORDER BY comentario.id_comentario DESC
        ''', (id_livro,)
    )
    comentarios = cursor.fetchall()
    conexao.close()
    return comentarios

def excluir_comentario(id_comentario, id_usuario):
    # so o autor do comentario pode excluir o proprio comentario
    conexao = sqlite3.connect(DB_NAME)
    conexao.execute('PRAGMA foreign_keys = ON')
    cursor = conexao.cursor()
    cursor.execute(
        'DELETE FROM comentario WHERE id_comentario = ? AND id_usuario = ?',
        (id_comentario, id_usuario)
    )
    conexao.commit()
    conexao.close()

def dar_selo(id_usuario):
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    cursor.execute(
        'UPDATE usuario SET selo_aprovado = 1 WHERE id_usuario = ?',
        (id_usuario,)
    ) #marca aprovado
    conexao.commit()
    conexao.close()
