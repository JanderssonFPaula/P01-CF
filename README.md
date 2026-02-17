# 💰 Controle Financeiro Web + Supabase + Lista de Compras

Sistema completo de controle financeiro web usando Supabase como banco de dados e incluindo funcionalidade de lista de compras.

## 🌟 Novidades nesta Versão

### ✅ Supabase (PostgreSQL Cloud)
- Substituiu SQLite por Supabase (banco de dados na nuvem)
- Cada usuário tem sua própria instância
- Configuração automática via interface web
- Dados sincronizados e acessíveis de qualquer lugar

### ✅ Sistema de Lista de Compras
- Criar listas de compras com múltiplos itens
- Adicionar items com quantidade e valor
- Ver total automaticamente
- Pagar lista direto de uma conta bancária
- Histórico de listas concluídas

## 📋 Funcionalidades

### Dashboard Financeiro
- Visualização de todas as contas organizadas por categoria
- Saldo total e por categoria
- Cores personalizadas para identificação
- Interface responsiva

### Gestão de Contas
- Cadastro de múltiplas contas em diferentes bancos
- Categorização (Contas a Pagar, Emergência, Casa, etc.)
- Histórico completo de transações
- Edição e exclusão de contas

### Lista de Compras 🆕
- **Criar listas** com nome personalizado
- **Adicionar itens** com descrição, quantidade e valor
- **Cálculo automático** do total da lista
- **Pagar lista** escolhendo de qual conta sai o dinheiro
- **Registro automático** da transação na conta
- **Histórico** de listas concluídas

## 🚀 Como Começar

### 1. Criar Projeto no Supabase (5 minutos)

1. Acesse https://supabase.com
2. Crie uma conta gratuita
3. Crie um novo projeto
   - Nome do projeto: `controle-financeiro`
   - Região: escolha a mais próxima
   - Senha do banco: crie uma senha forte
4. Aguarde o projeto ser criado (~2 minutos)

### 2. Pegar as Credenciais

1. No dashboard do Supabase, vá em **Settings** → **API**
2. Copie:
   - **Project URL** (exemplo: `https://xyzcompany.supabase.co`)
   - **anon/public key** (chave longa começando com `eyJhbGc...`)

### 3. Instalar o Sistema

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o sistema
python app.py
```

### 4. Configurar pelo Navegador

1. Abra http://localhost:5000
2. Você será redirecionado para a tela de configuração
3. Cole o **Project URL** e a **anon key**
4. Clique em **Salvar e Continuar**
5. Copie o SQL mostrado
6. Abra o Supabase → **SQL Editor**
7. Cole o SQL e clique em **Run**
8. Volte para o sistema e clique em **Ir para o Sistema**

**Pronto!** Sistema configurado! 🎉

## 📊 Como Usar

### Criar uma Conta Bancária

1. No dashboard, clique em **Nova Conta**
2. Preencha:
   - Nome: `Conta Corrente Principal`
   - Banco: `Nubank`
   - Categoria: `Contas a Pagar`
   - Saldo inicial: `1000.00`
   - Cor: escolha uma cor
3. Clique em **Criar Conta**

### Registrar Transações

1. Clique em uma conta
2. Use **Entrada** para adicionar dinheiro
3. Use **Saída** para registrar gastos
4. O saldo atualiza automaticamente!

### Usar Lista de Compras 🛒

#### Criar uma Lista:
1. Clique em **Listas de Compras** no menu
2. Clique em **Nova Lista**
3. Nome: `Mercado da Semana`

#### Adicionar Itens:
1. Na lista, clique em **Adicionar Item**
2. Descrição: `Arroz 5kg`
3. Quantidade: `2`
4. Valor: `15.90`
5. Clique em **Adicionar**

Repita para todos os itens. O total é calculado automaticamente!

#### Pagar a Lista:
1. Clique em **Pagar Lista**
2. Escolha de qual conta sai o dinheiro
3. Clique em **Confirmar Pagamento**

**O que acontece:**
- ✅ Lista marcada como concluída
- ✅ Transação registrada na conta
- ✅ Saldo da conta atualizado
- ✅ Histórico mantido

## 🗂️ Estrutura do Banco de Dados

### Tabela: contas
- id, nome, banco, categoria, saldo, cor, data_criacao

### Tabela: transacoes
- id, conta_id, tipo, valor, descricao, data

### Tabela: listas_compras
- id, nome, data_criacao, concluida, conta_id, data_conclusao

### Tabela: itens_lista
- id, lista_id, descricao, valor, quantidade

## 🔒 Segurança

### Por Padrão (Desenvolvimento):
- Políticas RLS criadas com acesso público
- Qualquer um com a URL pode acessar

### Para Produção (Recomendado):
Configure autenticação no Supabase:

1. Ative Authentication no Supabase
2. Configure providers (Email, Google, etc.)
3. Modifique as políticas RLS:

```sql
-- Exemplo de política segura
DROP POLICY "Permitir tudo em contas" ON contas;

CREATE POLICY "Usuários vêem apenas suas contas" 
ON contas FOR ALL 
USING (auth.uid() = user_id);
```

4. Adicione coluna `user_id` em todas as tabelas
5. Integre auth do Supabase no Flask

## 💡 Exemplos de Uso

### Cenário 1: Mercado do Mês
```
1. Criar lista: "Mercado Novembro"
2. Adicionar itens:
   - Arroz 5kg (2x) - R$ 15,90
   - Feijão 1kg (3x) - R$ 8,50
   - Leite 1L (12x) - R$ 4,20
   - ...
3. Total calculado: R$ 234,50
4. Pagar com: Conta Corrente Nubank
5. Lista concluída ✓
```

### Cenário 2: Organização de Finanças
```
Contas criadas:
- 🔵 Nubank → Contas do Mês
- 🟢 Inter → Reserva Emergência
- 🟡 BB → Casa e Reformas
- 🟣 XP → Investimentos

Listas:
- Mercado Semanal → pago do Nubank
- Material Construção → pago do BB
- Compras Online → pago do Nubank
```

## 🔧 Configurações Avançadas

### Mudar de Supabase

Para trocar de projeto:
1. Delete o arquivo `.env`
2. Reinicie o app
3. Configure com novas credenciais

### Backup dos Dados

No Supabase:
1. **Database** → **Backups**
2. Backups automáticos diários (gratuito)
3. Pode restaurar a qualquer momento

### Exportar Dados

```sql
-- No SQL Editor do Supabase
COPY contas TO '/tmp/contas.csv' CSV HEADER;
COPY transacoes TO '/tmp/transacoes.csv' CSV HEADER;
```

## 📱 Acesso Multi-dispositivo

Como está no Supabase, você pode:
- ✅ Acessar de qualquer computador
- ✅ Deploy em servidor (Heroku, Railway, etc.)
- ✅ Múltiplos usuários (com auth configurada)
- ✅ App mobile pode usar a mesma API

## 🐛 Problemas Comuns

### Erro: "relation does not exist"
**Solução:** Execute o SQL das tabelas no Supabase

### Erro: "Invalid API key"
**Solução:** Verifique se copiou a chave correta (anon public key)

### Lista não aparece após pagar
**Solução:** Recarregue a página. Verifique se a conta tem saldo suficiente.

### Não consigo deletar lista
**Solução:** Listas concluídas não podem ser deletadas (só pendentes)

## 🎯 Próximas Melhorias Sugeridas

- [ ] Autenticação de usuários
- [ ] Gráficos de gastos
- [ ] Categorias personalizadas
- [ ] Exportar relatórios PDF
- [ ] App mobile com Supabase
- [ ] Notificações por email
- [ ] Metas de economia
- [ ] Compartilhamento de listas
- [ ] Sugestões de produtos
- [ ] Integração com Open Banking

## 📄 Arquivos do Projeto

```
controle_financeiro_supabase/
├── app.py                  # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── .env                    # Credenciais (gerado automaticamente)
├── templates/
│   ├── base.html          # Template base
│   ├── setup.html         # Configuração inicial
│   ├── setup_tables.html  # SQL das tabelas
│   ├── index.html         # Dashboard
│   ├── conta.html         # Detalhes da conta
│   ├── listas_compras.html      # Lista de compras
│   └── lista_detalhe.html       # Detalhes da lista
└── static/
    ├── css/style.css      # Estilos
    └── js/script.js       # JavaScript
```

## 🌐 Deploy para Produção

### Opção 1: Railway

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway init
railway up
```

### Opção 2: Heroku

```bash
# Criar Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create meu-controle-financeiro
git push heroku main
```

### Opção 3: PythonAnywhere

1. Upload dos arquivos
2. Configure o WSGI
3. Adicione variáveis de ambiente

## 💬 Suporte

- Documentação Supabase: https://supabase.com/docs
- Documentação Flask: https://flask.palletsprojects.com/

## 📝 Licença

Livre para uso pessoal e modificações!

---

**Desenvolvido com ❤️ usando Flask + Supabase**

🎉 **Aproveite seu novo sistema de controle financeiro!**
