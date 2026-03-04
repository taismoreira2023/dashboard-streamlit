
# Dashboard Streamlit

Dashboard desenvolvido com **Streamlit** para análise de dados.

---

# ⚙️ Configuração do Ambiente Virtual

O projeto já possui scripts prontos para criação e ativação do ambiente virtual, de acordo com o sistema operacional.

Antes de tudo, verifique se você tem o Python instalado:

```bash
python --version
```
ou
```bash
python3 --version
```

---

## 🐧 Linux 

O projeto possui o script:

```
venv.sh
```

### ▶️ Para criar e ativar o ambiente virtual:

```bash
bash venv.sh
```

O script irá:

* Criar o ambiente `.venv`
* Ativar o ambiente
* Instalar as dependências do `requirements.txt`

---

## 🪟 Windows (PowerShell)

O projeto possui o script:

```
venv.ps1
```

### ▶️ Para criar e ativar o ambiente virtual:

```powershell
.\venv.ps1
```

> Caso o PowerShell bloqueie a execução, rode primeiro:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

O script irá:

* Criar o ambiente `.venv`
* Ativar o ambiente
* Instalar as dependências do `requirements.txt`

---

# 🚀 Executando o Dashboard

Após rodar o script do seu sistema operacional, execute:

```bash
streamlit run app.py
```

O terminal exibirá algo como:

```
Local URL: http://localhost:8501
```

Abra esse endereço no navegador para visualizar o dashboard.

---

# 🛑 Para desativar o ambiente

```bash
deactivate
```
