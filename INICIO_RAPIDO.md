# 🚀 GUIA RÁPIDO - 10 MINUTOS

## 1️⃣ CRIAR CONTA NO SUPABASE (3 min)

```
1. Acesse: https://supabase.com
2. Crie conta (pode usar Google/GitHub)
3. Clique em "New Project"
4. Preencha:
   - Name: controle-financeiro
   - Database Password: [crie uma senha]
   - Region: South America (ou mais próxima)
5. Clique em "Create new project"
6. Aguarde 2 minutos...
```

## 2️⃣ PEGAR CREDENCIAIS (1 min)

```
1. No menu lateral: Settings → API
2. Copiar:
   ✓ Project URL
   ✓ anon public key (começa com eyJhbGc...)
```

## 3️⃣ INSTALAR E RODAR (2 min)

```bash
# Instalar
pip install flask supabase python-dotenv

# Rodar
python app.py
```

Abrir: http://localhost:5000

## 4️⃣ CONFIGURAR (2 min)

```
1. Cole o Project URL
2. Cole o anon key
3. Clique em "Salvar e Continuar"
4. COPIAR TODO O SQL mostrado
```

## 5️⃣ CRIAR TABELAS (2 min)

```
1. Voltar ao Supabase
2. Menu lateral: SQL Editor
3. Colar o SQL
4. Clicar em "Run" (ou F5)
5. Aguardar "Success No rows returned"
```

## 6️⃣ PRONTO! 🎉

```
Voltar ao navegador
Clicar em "Ir para o Sistema"

Agora você tem:
✓ Sistema configurado
✓ Banco de dados criado
✓ Pronto para usar!
```

---

## 💰 CRIAR PRIMEIRA CONTA

```
1. Clicar em "Nova Conta"
2. Preencher:
   - Nome: Conta Corrente
   - Banco: Nubank
   - Categoria: Contas a Pagar
   - Saldo: 1000.00
   - Cor: Azul
3. Criar!
```

## 🛒 USAR LISTA DE COMPRAS

```
1. Menu: Listas de Compras
2. Nova Lista: "Mercado da Semana"
3. Adicionar Item:
   - Arroz 5kg
   - Quantidade: 2
   - Valor: 15.90
4. Adicionar mais itens...
5. Clicar em "Pagar Lista"
6. Escolher conta
7. Confirmar!

✓ Total calculado automaticamente
✓ Débito registrado na conta
✓ Lista marcada como concluída
```

---

## 🔥 COMANDOS ÚTEIS

```bash
# Rodar o sistema
python app.py

# Reinstalar dependências
pip install -r requirements.txt

# Ver logs
# Olhar terminal onde rodou python app.py
```

---

## ⚠️ PROBLEMAS?

**Erro de conexão:**
```
→ Verificar URL e key no setup
→ Verificar se projeto Supabase está ativo
```

**Tabelas não existem:**
```
→ Executar SQL no Supabase SQL Editor
→ Verificar "Success" após executar
```

**Página não carrega:**
```
→ Verificar se python app.py está rodando
→ Verificar http://localhost:5000
```

---

## 📚 QUER MAIS?

Leia o **README.md** completo para:
- Deploy em produção
- Configurar autenticação
- Múltiplos usuários
- Backup de dados
- E muito mais!

---

**🎉 Agora é só usar e organizar suas finanças!**
