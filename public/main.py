import webview
import threading
import http.server
import socketserver
import os
import requests
import urllib3
import time
from unicodedata import normalize

# Importa o módulo da outra equipe
import reconhecimento 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURAÇÕES ---
PORTA_SERVIDOR = 8085
API_URL = "https://traducao2.vlibras.gov.br/translate"

def iniciar_servidor():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.log_message = lambda *args: None
    porta = PORTA_SERVIDOR
    while True:
        try:
            with socketserver.TCPServer(("", porta), Handler) as httpd:
                print(f"✅ Servidor WebGL: http://localhost:{porta}")
                httpd.serve_forever()
                break
        except OSError:
            porta += 1

# --- TRADUÇÃO ---
def traduzir_via_api(texto_original):
    try:
        payload = {'text': texto_original}
        response = requests.post(API_URL, json=payload, timeout=3, verify=False)
        if response.status_code == 200:
            return response.text.replace('"', '').strip()
        return limpar_texto_local(texto_original)
    except:
        return limpar_texto_local(texto_original)

def limpar_texto_local(texto):
    if not texto: return ""
    IGNORAR = ["O", "A", "OS", "AS", "UM", "UMA", "DE", "DA", "DO", "EM", "QUE", "E"]
    try:
        t = normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').upper().strip()
        palavras = [p for p in t.split() if p not in IGNORAR]
        return " ".join(palavras) if palavras else t
    except:
        return str(texto).upper().strip()

# --- PONTE DE COMUNICAÇÃO ---
def receber_texto_do_whisper(texto):
    if not texto or len(texto.strip()) < 2: return
    
    glosa = traduzir_via_api(texto)
    
    if 'janela' in globals() and janela:
        print(f"🗣️ Enviando: {glosa}")
        try:
            janela.evaluate_js(f'py_receber("{glosa}")')
        except: pass

def atualizar_status_loading(mensagem):
    """Atualiza o texto na tela de carregamento (Blindado)"""
    if 'janela' in globals() and janela:
        try:
            if mensagem == "PRONTO":
                janela.evaluate_js('if(window.py_esconder_loading) py_esconder_loading()')
            else:
                janela.evaluate_js(f'if(window.py_atualizar_texto_loading) py_atualizar_texto_loading("{mensagem}")')
        except Exception as e:
            print(f"⏳ Carregando... ({mensagem})")

# --- FUNÇÃO DE ENCERRAMENTO (A CORREÇÃO) ---
def encerrar_tudo():
    print("❌ Encerrando aplicação e liberando terminal...")
    # Força o encerramento imediato do processo e de todas as threads
    os._exit(0)

# --- MAIN ---
def main():
    global janela
    
    # 1. Inicia Servidor HTTP
    t_server = threading.Thread(target=iniciar_servidor, daemon=True)
    t_server.start()
    
    # 2. Configura a Janela
    janela = webview.create_window(
        'Avatar VLibras', 
        f'http://localhost:{PORTA_SERVIDOR}/index.html',
        width=400, 
        height=600, 
        background_color='#333333',
        on_top=True
    )

    # --- VINCULA O EVENTO DE FECHAR ---
    # Quando o usuário clicar no X, chama a função que mata o terminal
    janela.events.closed += encerrar_tudo

    # 3. Função que roda DEPOIS que a janela abre
    def iniciar_thread_geral():
        time.sleep(2) 
        reconhecimento.iniciar_ouvinte(receber_texto_do_whisper, atualizar_status_loading)

    # Inicia a thread lógica
    webview.start(func=iniciar_thread_geral)

if __name__ == '__main__':
    main()