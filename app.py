from flask import Flask, render_template, request, redirect,  session, url_for  
import model

app = Flask(__name__)

app.secret_key = 'aaah'
model.init_db() 

QUESTOES_SELO = [
    {
        'pergunta': 'Dentro do contexto de ESD/OCS, como você descreveria, sucintamente, a relação entre flip-flops, registradores e os fundamentos da programação (estruturas de teste e de repetição)?',
        'alternativas': [
            ('a', 'Flip-flops armazenam bits e formam registradores, que guardam estados/valores — assim como variáveis guardam estado em estruturas de repetição e teste na programação.'),
            ('b', 'Flip-flops servem só para gerar o sinal de clock do circuito e não têm relação nenhuma com armazenamento de dados.'),
            ('c', 'Registradores servem apenas para converter sinais analógicos em digitais, sem relação com lógica sequencial.'),
        ],
        'correta': 'a',
    },
    {
        'pergunta': 'Por que é necessário o bloco ou módulo "Entrada e REM" no SAP-1? Não ficaria mais simples escrever direto na RAM 16x8?',
        'alternativas': [
            ('a', 'Porque o REM só existe pra aumentar a capacidade total de endereços da RAM; sem ele a memória teria menos posições disponíveis.'),
            ('b', 'O REM guarda temporariamente o endereço a ser acessado na RAM, permitindo controlar e sincronizar o uso do barramento W (compartilhado por vários módulos) através do clock/sequenciador.'),
            ('c', 'Ele converte os dados binários lidos da RAM para decimal antes de colocá-los no barramento.'),
        ],
        'correta': 'b',
    },
    {
        'pergunta': 'Qual a diferença entre uma RAM e uma EEPROM?',
        'alternativas': [
            ('a', 'A RAM é volátil (perde os dados sem energia) e usada como memória de trabalho rápida; a EEPROM é não-volátil, mantém os dados sem energia, mas grava mais devagar e tem ciclos de escrita limitados.'),
            ('b', 'A RAM é não-volátil e a EEPROM é volátil — essa é a única diferença entre elas.'),
            ('c', 'Não existe diferença real entre as duas; a única coisa que muda é o preço do componente.'),
        ],
        'correta': 'a',
    },
]

@app.route("/")
def home():
    busca = request.args.get('busca', '').strip()
    livros = model.listar_livros(busca if busca else None)
    return render_template('home.html', livros=livros, busca=busca)

@app.route("/cadastrar", methods=['GET', 'POST'])
def cadastro_livro():
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))

    if not session.get('selo_aprovado'):
        return redirect(url_for('verificar_selo')) #se o usuario nao tem selo, precisa ter antes de cadastrar

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        autor = request.form.get('autor', '').strip()
        genero = request.form.get('genero', '').strip()
        ano_publicacao = request.form.get('ano_publicacao', '').strip()
        preco_texto = request.form.get('preco')

        if not titulo or not genero or not preco_texto: #checagem
            erro = 'Preencha os campos obrigatórios: título, gênero e preço.'
            return render_template('cadastrar.html', erro=erro)

        try:
            preco = float(preco_texto)
        except ValueError:
            erro = 'Preço inválido. Digite um número (ex: 29.90).'
            return render_template('cadastrar.html', erro=erro)

        if preco < 0:
            erro = 'O preço não pode ser negativo.'
            return render_template('cadastrar.html', erro=erro)

        id_usuario = session['id_usuario']
        status = 'aprovado' #aprovado pq ja passou pela verificação que se vc nao fez é obrigado antes de vir para ca

        model.cadastrar_livro(titulo, autor, genero, ano_publicacao, preco, status, id_usuario)
        return redirect('/') #post
    return render_template('cadastrar.html') #get

@app.route('/editar/<int:id_livro>', methods=['GET', 'POST'])
def editar_livro(id_livro):
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))

    livro = model.buscar_livro(id_livro, session['id_usuario']) #confere para ver se pertence ao usuario
    
    if livro is None:
        return redirect(url_for('meus_livros'))  # se não achou livro, manda para a listagem

    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        autor = request.form.get('autor', '').strip()
        genero = request.form.get('genero', '').strip()
        ano_publicacao = request.form.get('ano_publicacao', '').strip()
        preco_texto = request.form.get('preco')

        if not titulo or not genero or not preco_texto:
            erro = 'Preencha os campos obrigatórios: título, gênero e preço.'
            return render_template('editar.html', livro=livro, erro=erro)

        try: # mesma validação de preço do cadastro
            preco = float(preco_texto)
        except ValueError:
            erro = 'Preço inválido. Digite um número (ex: 29.90).'
            return render_template('editar.html', livro=livro, erro=erro)

        if preco < 0:
            erro = 'O preço não pode ser negativo.'
            return render_template('editar.html', livro=livro, erro=erro)

        model.editar_livro(id_livro, titulo, autor, genero, ano_publicacao, preco, session['id_usuario'])
        return redirect(url_for('meus_livros')) #post

    return render_template('editar.html', livro=livro) #get

@app.route('/registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        senha = request.form.get('senha', '').strip()

        if not nome or not senha:
            return render_template('registrar.html', erro='Preencha nome de usuário e senha.')

        if model.usuario_existe(nome):
            return render_template('registrar.html', erro='Essa conta já existe. Escolha outro nome de usuário.')

        model.criar_usuario(nome, senha)
        return redirect(url_for('fazer_login'))
    return render_template('registrar.html')

@app.route('/login', methods=['GET', 'POST'])
def fazer_login():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        senha = request.form.get('senha', '').strip()

        if not nome or not senha:
            return render_template('login.html', erro='Preencha nome de usuário e senha.')

        usuario = model.fazer_loguin(nome, senha)

        if usuario:
            session['id_usuario'] = usuario[0]
            session['nome'] = usuario[1]
            session['selo_aprovado'] = usuario[2]
            return redirect('/')
        else:
            return render_template('login.html', erro='Nome ou senha incorretos')

    return render_template('login.html')

@app.route("/meus-livros")
def meus_livros():
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))
    livros = model.listar_livros_usuario(session['id_usuario'])
    return render_template('meus_livros.html', livros=livros)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/excluir/<int:id_livro>', methods=['POST'])
def excluir_livro(id_livro):
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))

    model.excluir_livro(id_livro, session['id_usuario'])
    return redirect(url_for('meus_livros'))

@app.route('/livro/<int:id_livro>', methods=['GET', 'POST'])
def ver_livro(id_livro):
    livro = model.buscar_livro_por_id(id_livro)
    if livro is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        # comentar exige estar logado, mas NAO exige selo diferente de cadastrar livro
        if 'id_usuario' not in session:
            return redirect(url_for('fazer_login'))

        texto = request.form.get('texto', '').strip()
        if texto:
            model.adicionar_comentario(id_livro, session['id_usuario'], texto)
        return redirect(url_for('ver_livro', id_livro=id_livro))

    comentarios = model.listar_comentarios(id_livro)
    return render_template('livro_detalhe.html', livro=livro, comentarios=comentarios)

@app.route('/livro/<int:id_livro>/comentario/<int:id_comentario>/excluir', methods=['POST'])
def excluir_comentario(id_livro, id_comentario):
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))

    model.excluir_comentario(id_comentario, session['id_usuario'])
    return redirect(url_for('ver_livro', id_livro=id_livro))

@app.route('/selo', methods=['GET', 'POST'])
def verificar_selo():
    if 'id_usuario' not in session:
        return redirect(url_for('fazer_login'))

    # se o usuário já tem o selo, não precisa fazer o teste de novo
    if session.get('selo_aprovado'):
        return redirect(url_for('cadastro_livro'))

    if request.method == 'POST':
        acertos = 0
        for i, questao in enumerate(QUESTOES_SELO):
            resposta = request.form.get(f'pergunta{i}')
            if resposta == questao['correta']:
                acertos += 1

        if acertos == len(QUESTOES_SELO):
            model.dar_selo(session['id_usuario']) # ganha o selo e salva no banco
            session['selo_aprovado'] = 1
            return render_template('selo_sucesso.html')  # mostra a telinha de sucesso
        else:
            erro = f'Você acertou {acertos} de {len(QUESTOES_SELO)} perguntas. Revise e tente de novo!'
            return render_template('selo.html', questoes=QUESTOES_SELO, erro=erro)

    return render_template('selo.html', questoes=QUESTOES_SELO)

if __name__ == '__main__':
    app.run(debug=True)
