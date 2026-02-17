# 📊 ESTRUTURA DAS TABELAS - P01CF_

## 🎯 Por que usar prefixo?

O sistema usa o prefixo **P01CF_** em todas as tabelas:
- **P01** = Projeto 01
- **CF** = Controle Financeiro

### Vantagens:

✅ **Organização**: Você pode ter vários projetos no mesmo banco Supabase
✅ **Identificação**: Fácil identificar quais tabelas são deste sistema
✅ **Compartilhamento**: Use o mesmo Supabase para múltiplos sistemas

## 📋 Tabelas Criadas

O sistema cria automaticamente 4 tabelas:

### 1. **p01cf_contas**
Armazena as contas bancárias cadastradas.

```sql
CREATE TABLE p01cf_contas (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    banco TEXT NOT NULL,
    categoria TEXT NOT NULL,
    saldo DECIMAL(10,2) DEFAULT 0,
    cor TEXT DEFAULT '#007bff',
    data_criacao TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único
- `nome`: Nome da conta (ex: "Conta Corrente")
- `banco`: Banco (ex: "Nubank")
- `categoria`: Categoria (ex: "Contas a Pagar")
- `saldo`: Saldo atual
- `cor`: Cor para identificação visual
- `data_criacao`: Quando foi criada

---

### 2. **p01cf_transacoes**
Registra todas as movimentações financeiras.

```sql
CREATE TABLE p01cf_transacoes (
    id BIGSERIAL PRIMARY KEY,
    conta_id BIGINT REFERENCES p01cf_contas(id) ON DELETE CASCADE,
    tipo TEXT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    descricao TEXT,
    data TIMESTAMP DEFAULT NOW()
);
```

**Campos:**
- `id`: Identificador único
- `conta_id`: ID da conta (relacionamento)
- `tipo`: "entrada" ou "saida"
- `valor`: Valor da transação
- `descricao`: Descrição (ex: "Salário do mês")
- `data`: Quando foi registrada

---

### 3. **p01cf_listas_compras**
Armazena as listas de compras.

```sql
CREATE TABLE p01cf_listas_compras (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    data_criacao TIMESTAMP DEFAULT NOW(),
    concluida BOOLEAN DEFAULT FALSE,
    conta_id BIGINT REFERENCES p01cf_contas(id),
    data_conclusao TIMESTAMP
);
```

**Campos:**
- `id`: Identificador único
- `nome`: Nome da lista (ex: "Mercado da Semana")
- `data_criacao`: Quando foi criada
- `concluida`: Se já foi paga
- `conta_id`: De qual conta foi paga (se paga)
- `data_conclusao`: Quando foi paga

---

### 4. **p01cf_itens_lista**
Armazena os itens de cada lista de compras.

```sql
CREATE TABLE p01cf_itens_lista (
    id BIGSERIAL PRIMARY KEY,
    lista_id BIGINT REFERENCES p01cf_listas_compras(id) ON DELETE CASCADE,
    descricao TEXT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    quantidade INTEGER DEFAULT 1
);
```

**Campos:**
- `id`: Identificador único
- `lista_id`: ID da lista (relacionamento)
- `descricao`: O que é (ex: "Arroz 5kg")
- `valor`: Valor unitário
- `quantidade`: Quantos itens

---

## 🔐 Segurança (RLS)

Todas as tabelas têm **Row Level Security (RLS)** ativado com política pública:

```sql
-- Política de acesso público (desenvolvimento)
CREATE POLICY "Permitir tudo" ON p01cf_contas FOR ALL USING (true);
```

### Para Produção:

Se quiser restringir acesso por usuário, modifique as políticas:

```sql
-- Exemplo: apenas ver suas próprias contas
DROP POLICY "Permitir tudo" ON p01cf_contas;

CREATE POLICY "Ver apenas suas contas" 
ON p01cf_contas 
FOR SELECT 
USING (auth.uid() = user_id);
```

(Você precisaria adicionar coluna `user_id` em cada tabela)

---

## 🗄️ Relacionamentos

```
p01cf_contas
    ↓
    ├─→ p01cf_transacoes (conta_id)
    └─→ p01cf_listas_compras (conta_id - quando paga)
            ↓
            └─→ p01cf_itens_lista (lista_id)
```

**Efeitos CASCADE:**
- Deletar conta → deleta transações automaticamente
- Deletar lista → deleta itens automaticamente

---

## 🔄 Mudar o Prefixo

Se quiser usar outro prefixo (ex: `meuapp_`), edite o `app.py`:

```python
# Linha ~14
TABLE_PREFIX = "meuapp_"  # Mude aqui
```

Depois execute o SQL com o novo prefixo no Supabase.

---

## 📊 Consultas Úteis

### Ver todas as tabelas do projeto:
```sql
SELECT tablename 
FROM pg_tables 
WHERE tablename LIKE 'p01cf_%';
```

### Contar registros:
```sql
SELECT 
    (SELECT COUNT(*) FROM p01cf_contas) as total_contas,
    (SELECT COUNT(*) FROM p01cf_transacoes) as total_transacoes,
    (SELECT COUNT(*) FROM p01cf_listas_compras) as total_listas,
    (SELECT COUNT(*) FROM p01cf_itens_lista) as total_itens;
```

### Backup de uma tabela:
```sql
CREATE TABLE p01cf_contas_backup AS 
SELECT * FROM p01cf_contas;
```

---

## 🗑️ Limpar Tudo

Se quiser deletar tudo e recomeçar:

```sql
DROP TABLE IF EXISTS p01cf_itens_lista CASCADE;
DROP TABLE IF EXISTS p01cf_listas_compras CASCADE;
DROP TABLE IF EXISTS p01cf_transacoes CASCADE;
DROP TABLE IF EXISTS p01cf_contas CASCADE;
```

Depois rode o sistema novamente que ele recriará as tabelas.

---

## ✅ Verificar se Tabelas Existem

Via SQL:
```sql
SELECT EXISTS (
    SELECT FROM pg_tables 
    WHERE tablename = 'p01cf_contas'
);
```

Via Python:
```python
from supabase import create_client

supabase = create_client(url, key)
try:
    result = supabase.table('p01cf_contas').select('count').limit(1).execute()
    print("✅ Tabelas existem!")
except:
    print("❌ Tabelas não existem!")
```

---

**💡 Dica Final**: O prefixo `p01cf_` é apenas uma convenção. O importante é ser consistente e usar o mesmo prefixo em todas as tabelas do projeto!
