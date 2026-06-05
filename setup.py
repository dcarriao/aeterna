import os

# Criar arquivo .streamlit/config.toml para configurar o servidor
os.makedirs(".streamlit", exist_ok=True)

with open(".streamlit/config.toml", "w") as f:
    f.write("""
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "aeterenalegado.com.br"
serverPort = 443
""")