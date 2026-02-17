from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import datetime
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

# Variável global para o cliente Supabase
supabase: Client = None

# Prefixo das tabelas - Projeto 01 Controle Financeiro
TABLE_PREFIX = "p01cf_"
TABLE_CONTAS = f"{TABLE_PREFIX}contas"
TABLE_TRANSACOES = f"{TABLE_PREFIX}transacoes"
TABLE_LISTAS = f"{TABLE_PREFIX}listas_compras"
TABLE_ITENS = f"{TABLE_PREFIX}itens_lista"

def is_configured():
    config_file = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(config_file):
        return False
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    return url and key

def init_supabase():
    global supabase
    if is_configured():
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        try:
            supabase = create_client(supabase_url=url, supabase_key=key)
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    return False

def verificar_tabelas():
    try:
        supabase.table(TABLE_CONTAS).select('count').limit(1).execute()
        return True
    except:
        return False

def gerar_sql_tabelas():
    return f"""-- TABELAS COM PREFIXO {TABLE_PREFIX.upper()}
-- Projeto 01 - Controle Financeiro

CREATE TABLE IF NOT EXISTS {TABLE_CONTAS} (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    banco TEXT NOT NULL,
    categoria TEXT NOT NULL,
    saldo DECIMAL(10,2) DEFAULT 0,
    cor TEXT DEFAULT '#007bff',
    data_criacao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS {TABLE_TRANSACOES} (
    id BIGSERIAL PRIMARY KEY,
    conta_id BIGINT REFERENCES {TABLE_CONTAS}(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    data TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS {TABLE_LISTAS} (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT NOW(),
    concluida BOOLEAN DEFAULT FALSE,
    conta_id BIGINT REFERENCES {TABLE_CONTAS}(id),
    data_conclusao TIMESTAMP
);

CREATE TABLE IF NOT EXISTS {TABLE_ITENS} (
    id BIGSERIAL PRIMARY KEY,
    lista_id BIGINT REFERENCES {TABLE_LISTAS}(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    quantidade INTEGER DEFAULT 1
);

ALTER TABLE {TABLE_CONTAS} ENABLE ROW LEVEL SECURITY;
ALTER TABLE {TABLE_TRANSACOES} ENABLE ROW LEVEL SECURITY;
ALTER TABLE {TABLE_LISTAS} ENABLE ROW LEVEL SECURITY;
ALTER TABLE {TABLE_ITENS} ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Permitir tudo" ON {TABLE_CONTAS};
CREATE POLICY "Permitir tudo" ON {TABLE_CONTAS} FOR ALL USING (true);

DROP POLICY IF EXISTS "Permitir tudo" ON {TABLE_TRANSACOES};
CREATE POLICY "Permitir tudo" ON {TABLE_TRANSACOES} FOR ALL USING (true);

DROP POLICY IF EXISTS "Permitir tudo" ON {TABLE_LISTAS};
CREATE POLICY "Permitir tudo" ON {TABLE_LISTAS} FOR ALL USING (true);

DROP POLICY IF EXISTS "Permitir tudo" ON {TABLE_ITENS};
CREATE POLICY "Permitir tudo" ON {TABLE_ITENS} FOR ALL USING (true);
"""

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        supabase_url = request.form['supabase_url']
        supabase_key = request.form['supabase_key']
        
        try:
            test_client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
            
            env_path = os.path.join(os.path.dirname(__file__), '.env')
            with open(env_path, 'w') as f:
                f.write(f'SUPABASE_URL={supabase_url}\n')
                f.write(f'SUPABASE_KEY={supabase_key}\n')
            
            load_dotenv()
            init_supabase()
            
            if verificar_tabelas():
                flash('Conexão OK! Tabelas já existem.', 'success')
                return redirect(url_for('index'))
            else:
                flash('Conexão OK! Agora vamos criar as tabelas.', 'success')
                return redirect(url_for('setup_tables'))
            
        except Exception as e:
            flash(f'Erro ao conectar: {str(e)}', 'error')
            return render_template('setup.html', error=str(e))
    
    return render_template('setup.html')

@app.route('/setup/tables')
def setup_tables():
    sql_script = gerar_sql_tabelas()
    return render_template('setup_tables.html', sql_script=sql_script)

@app.route('/setup/test')
def test_connection():
    try:
        supabase.table(TABLE_CONTAS).select('*').limit(1).execute()
        return jsonify({'success': True, 'message': 'Conexão OK! Tabelas criadas!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.before_request
def check_setup():
    if request.endpoint and request.endpoint not in ['setup', 'setup_tables', 'test_connection', 'static']:
        if not is_configured():
            return redirect(url_for('setup'))

@app.route('/')
def index():
    try:
        contas = supabase.table(TABLE_CONTAS).select('*').order('categoria').order('nome').execute()
        categorias = {}
        total_geral = 0
        for conta in contas.data:
            if conta['categoria'] not in categorias:
                categorias[conta['categoria']] = {'contas': [], 'total': 0}
            categorias[conta['categoria']]['contas'].append(conta)
            categorias[conta['categoria']]['total'] += float(conta['saldo'])
            total_geral += float(conta['saldo'])
        return render_template('index.html', categorias=categorias, total_geral=total_geral)
    except Exception as e:
        flash(f'Erro: {str(e)}. Verifique se as tabelas foram criadas.', 'error')
        return redirect(url_for('setup_tables'))

@app.route('/conta/adicionar', methods=['POST'])
def adicionar_conta():
    supabase.table(TABLE_CONTAS).insert({
        'nome': request.form['nome'],
        'banco': request.form['banco'],
        'categoria': request.form['categoria'],
        'saldo': float(request.form.get('saldo', 0)),
        'cor': request.form.get('cor', '#007bff')
    }).execute()
    flash('Conta criada!', 'success')
    return redirect(url_for('index'))

@app.route('/conta/<int:id>')
def ver_conta(id):
    conta = supabase.table(TABLE_CONTAS).select('*').eq('id', id).single().execute()
    transacoes = supabase.table(TABLE_TRANSACOES).select('*').eq('conta_id', id).order('data', desc=True).limit(50).execute()
    return render_template('conta.html', conta=conta.data, transacoes=transacoes.data)

@app.route('/conta/<int:id>/transacao', methods=['POST'])
def adicionar_transacao(id):
    tipo = request.form['tipo']
    valor = float(request.form['valor'])
    supabase.table(TABLE_TRANSACOES).insert({
        'conta_id': id,
        'tipo': tipo,
        'valor': valor,
        'descricao': request.form['descricao']
    }).execute()
    conta = supabase.table(TABLE_CONTAS).select('*').eq('id', id).single().execute()
    novo_saldo = float(conta.data['saldo']) + (valor if tipo == 'entrada' else -valor)
    supabase.table(TABLE_CONTAS).update({'saldo': novo_saldo}).eq('id', id).execute()
    flash('Transação registrada!', 'success')
    return redirect(url_for('ver_conta', id=id))

@app.route('/conta/<int:id>/editar', methods=['POST'])
def editar_conta(id):
    supabase.table(TABLE_CONTAS).update({
        'nome': request.form['nome'],
        'banco': request.form['banco'],
        'categoria': request.form['categoria'],
        'cor': request.form['cor']
    }).eq('id', id).execute()
    flash('Conta atualizada!', 'success')
    return redirect(url_for('ver_conta', id=id))

@app.route('/conta/<int:id>/deletar', methods=['POST'])
def deletar_conta(id):
    supabase.table(TABLE_CONTAS).delete().eq('id', id).execute()
    flash('Conta deletada!', 'success')
    return redirect(url_for('index'))

@app.route('/listas')
def listas_compras():
    try:
        listas_ativas = supabase.table(TABLE_LISTAS).select('*').eq('concluida', False).order('data_criacao', desc=True).execute()
        for lista in listas_ativas.data:
            itens = supabase.table(TABLE_ITENS).select('*').eq('lista_id', lista['id']).execute()
            lista['itens_lista'] = itens.data
            lista['total'] = sum(float(i['valor']) * i['quantidade'] for i in itens.data)
        
        listas_concluidas = supabase.table(TABLE_LISTAS).select('*').eq('concluida', True).order('data_conclusao', desc=True).limit(10).execute()
        for lista in listas_concluidas.data:
            itens = supabase.table(TABLE_ITENS).select('*').eq('lista_id', lista['id']).execute()
            lista['itens_lista'] = itens.data
            lista['total'] = sum(float(i['valor']) * i['quantidade'] for i in itens.data)
            if lista.get('conta_id'):
                conta = supabase.table(TABLE_CONTAS).select('nome').eq('id', lista['conta_id']).single().execute()
                lista['contas'] = conta.data if conta.data else {}
            else:
                lista['contas'] = {}
        
        return render_template('listas_compras.html', listas_ativas=listas_ativas.data, listas_concluidas=listas_concluidas.data)
    except Exception as e:
        flash(f'Erro: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/lista/nova', methods=['POST'])
def nova_lista():
    lista = supabase.table(TABLE_LISTAS).insert({'nome': request.form['nome']}).execute()
    flash('Lista criada!', 'success')
    return redirect(url_for('ver_lista', id=lista.data[0]['id']))

@app.route('/lista/<int:id>')
def ver_lista(id):
    lista = supabase.table(TABLE_LISTAS).select('*').eq('id', id).single().execute()
    itens = supabase.table(TABLE_ITENS).select('*').eq('lista_id', id).execute()
    total = sum(float(i['valor']) * i['quantidade'] for i in itens.data)
    contas = supabase.table(TABLE_CONTAS).select('*').execute()
    return render_template('lista_detalhe.html', lista=lista.data, itens=itens.data, total=total, contas=contas.data)

@app.route('/lista/<int:id>/item', methods=['POST'])
def adicionar_item_lista(id):
    supabase.table(TABLE_ITENS).insert({
        'lista_id': id,
        'descricao': request.form['descricao'],
        'valor': float(request.form['valor']),
        'quantidade': int(request.form.get('quantidade', 1))
    }).execute()
    flash('Item adicionado!', 'success')
    return redirect(url_for('ver_lista', id=id))

@app.route('/lista/<int:id>/item/<int:item_id>/deletar', methods=['POST'])
def deletar_item_lista(id, item_id):
    supabase.table(TABLE_ITENS).delete().eq('id', item_id).execute()
    flash('Item removido!', 'success')
    return redirect(url_for('ver_lista', id=id))

@app.route('/lista/<int:id>/pagar', methods=['POST'])
def pagar_lista(id):
    conta_id = int(request.form['conta_id'])
    lista = supabase.table(TABLE_LISTAS).select('*').eq('id', id).single().execute()
    itens = supabase.table(TABLE_ITENS).select('*').eq('lista_id', id).execute()
    total = sum(float(i['valor']) * i['quantidade'] for i in itens.data)
    conta = supabase.table(TABLE_CONTAS).select('*').eq('id', conta_id).single().execute()
    
    if float(conta.data['saldo']) < total:
        flash('Saldo insuficiente!', 'error')
        return redirect(url_for('ver_lista', id=id))
    
    itens_desc = ', '.join([f"{i['quantidade']}x {i['descricao']}" for i in itens.data[:3]])
    if len(itens.data) > 3:
        itens_desc += f" e mais {len(itens.data) - 3} itens"
    
    supabase.table(TABLE_TRANSACOES).insert({
        'conta_id': conta_id,
        'tipo': 'saida',
        'valor': total,
        'descricao': f"Lista: {lista.data['nome']} ({itens_desc})"
    }).execute()
    
    novo_saldo = float(conta.data['saldo']) - total
    supabase.table(TABLE_CONTAS).update({'saldo': novo_saldo}).eq('id', conta_id).execute()
    supabase.table(TABLE_LISTAS).update({
        'concluida': True,
        'conta_id': conta_id,
        'data_conclusao': datetime.now().isoformat()
    }).eq('id', id).execute()
    
    flash(f'Lista paga! R$ {total:.2f} debitado de {conta.data["nome"]}', 'success')
    return redirect(url_for('listas_compras'))

@app.route('/lista/<int:id>/deletar', methods=['POST'])
def deletar_lista(id):
    supabase.table(TABLE_LISTAS).delete().eq('id', id).execute()
    flash('Lista deletada!', 'success')
    return redirect(url_for('listas_compras'))

@app.route('/api/resumo')
def api_resumo():
    contas = supabase.table(TABLE_CONTAS).select('*').execute()
    resumo = {'total_geral': sum(float(c['saldo']) for c in contas.data), 'por_categoria': {}}
    for c in contas.data:
        cat = c['categoria']
        if cat not in resumo['por_categoria']:
            resumo['por_categoria'][cat] = 0
        resumo['por_categoria'][cat] += float(c['saldo'])
    return jsonify(resumo)

if __name__ == '__main__':
    init_supabase()
    app.run(debug=True, host='0.0.0.0', port=5000)
