import sounddevice as sd
import numpy as np
import queue
import tempfile
import os
import json
from datetime import datetime
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

# =============================
# CONFIGURAÇÕES
# =============================
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 3.0
JSON_PATH = "transcricao.json"
MAX_HISTORICO = 50
USAR_GPU = False 

# Variável global do modelo (começa vazia)
model = None
audio_queue = queue.Queue()

# =============================
# FUNÇÕES AUXILIARES
# =============================
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Status Audio: {status}")
    audio_queue.put(indata.copy())

def transcrever_audio(wav_path: str) -> str:
    if not model: return ""
    # beam_size=5 aumenta precisão
    segments, info = model.transcribe(wav_path, language="pt", beam_size=5)
    texto_completo = ""
    for segment in segments:
        texto_completo += segment.text
    return texto_completo.strip()

def processar_texto(texto: str) -> str:
    return " ".join(texto.split())

def atualizar_json(texto_processado: str, caminho_json: str):
    timestamp_atual = datetime.now().isoformat()
    if os.path.exists(caminho_json):
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except:
            dados = {"ultimo_texto": "", "timestamp": "", "historico": []}
    else:
        dados = {"ultimo_texto": "", "timestamp": "", "historico": []}
    
    ultimo = dados.get("ultimo_texto", "").strip().lower()
    if texto_processado.strip().lower() == ultimo:
        return 

    dados["ultimo_texto"] = texto_processado
    dados["timestamp"] = timestamp_atual
    dados["historico"].append({"texto": texto_processado, "timestamp": timestamp_atual})
    dados["historico"] = dados["historico"][-MAX_HISTORICO:]
    
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# =============================
# FUNÇÃO PRINCIPAL (Modular)
# =============================
def iniciar_ouvinte(callback_texto, callback_status=None):
    """
    Inicia o loop.
    :param callback_texto: Função que recebe o texto final.
    :param callback_status: Função que recebe string de status ("Carregando...", "Pronto").
    """
    global model

    # 1. Carregamento Tardio do Modelo
    if model is None:
        if callback_status: callback_status("Carregando Inteligência Artificial...")
        print("🧠 Carregando Whisper...")
        try:
            model = WhisperModel(
                "medium",
                device="cuda" if USAR_GPU else "cpu",
                compute_type="int8_float16" if USAR_GPU else "int8"
            )
            print("✅ Modelo carregado!")
        except Exception as e:
            print(f"❌ Erro Whisper: {e}")
            if callback_status: callback_status("Erro ao carregar IA")
            return

    # 2. Inicia Microfone
    if callback_status: callback_status("Iniciando Microfone...")
    print("\n🎤 Microfone Aberto!")
    
    # 3. Avisa que está pronto (para sumir com a tela de loading)
    if callback_status: callback_status("PRONTO")

    # 4. Loop de Áudio
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback):
        buffer = np.empty((0, CHANNELS), dtype=np.float32)

        while True:
            data = audio_queue.get()
            buffer = np.vstack((buffer, data))

            if len(buffer) >= SAMPLE_RATE * CHUNK_DURATION:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                    write(tmp.name, SAMPLE_RATE, buffer)
                    wav_path = tmp.name
                
                buffer = np.empty((0, CHANNELS), dtype=np.float32)

                try:
                    texto_bruto = transcrever_audio(wav_path)
                    
                    if texto_bruto and len(texto_bruto.strip()) > 1:
                        texto_processado = processar_texto(texto_bruto)
                        atualizar_json(texto_processado, JSON_PATH)
                        print(f"Detectado: {texto_processado}")
                        
                        # Manda para o main.py
                        callback_texto(texto_processado)

                except Exception as e:
                    print(f"Erro processamento: {e}")
                finally:
                    if os.path.exists(wav_path):
                        os.remove(wav_path)