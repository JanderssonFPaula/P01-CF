# 🔧 CORREÇÃO DE ERRO: "unexpected keyword argument 'proxy'"

## Problema

Você está vendo este erro:
```
Erro ao conectar: Client.__init__() got an unexpected keyword argument 'proxy'
```

## Causa

Versão incompatível da biblioteca `supabase`.

## Solução Rápida

### 1. Desinstalar versão antiga:
```bash
pip uninstall supabase -y
pip uninstall supabase-py -y
```

### 2. Instalar versão correta:
```bash
pip install supabase==2.0.0
pip install postgrest==0.13.0
```

### 3. Reiniciar o app:
```bash
python app.py
```

### 4. Testar novamente

Volte em http://localhost:5000/setup e configure de novo.

---

## Solução Completa (se a rápida não funcionar)

### 1. Limpar tudo:
```bash
pip freeze | xargs pip uninstall -y
```

### 2. Reinstalar apenas o necessário:
```bash
pip install Flask==3.0.0
pip install supabase==2.0.0
pip install python-dotenv==1.0.0
pip install postgrest==0.13.0
```

### 3. Verificar instalação:
```bash
python -c "from supabase import create_client; print('OK')"
```

Se aparecer "OK", está funcionando!

### 4. Rodar o app:
```bash
python app.py
```

---

## Alternativa: Usar requirements.txt atualizado

O arquivo `requirements.txt` já foi corrigido. Basta:

```bash
pip install -r requirements.txt --upgrade --force-reinstall
```

---

## Verificar se está tudo OK

Execute este teste:

```python
from supabase import create_client
import os

# Suas credenciais
url = "https://seu-projeto.supabase.co"
key = "sua-chave-aqui"

# Testar conexão
try:
    supabase = create_client(
        supabase_url=url,
        supabase_key=key
    )
    print("✅ Conexão OK!")
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

## Ainda com problema?

### Opção 1: Usar ambiente virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
venv\Scripts\activate

# Ativar (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar app
python app.py
```

### Opção 2: Verificar versão do Python

Certifique-se de usar Python 3.8+:

```bash
python --version
```

Se for menor que 3.8, atualize o Python.

---

## Resumo

**Problema:** Versão errada do supabase
**Solução:** Instalar `supabase==2.0.0`
**Comando:** `pip install supabase==2.0.0 postgrest==0.13.0`

Pronto! ✅
