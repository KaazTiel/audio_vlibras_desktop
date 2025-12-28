<h1 align="center">Audio VLibras Desktop 🗣️👐</h1>

<p align="center">
  Uma aplicação Desktop que ouve sua voz, transcreve em tempo real e traduz para Libras utilizando o Avatar 3D oficial do governo.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/AI-Faster_Whisper-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Avatar-VLibras-yellow?style=for-the-badge" />
</p>

## :dart: Sobre o Projeto

Este projeto é uma evolução do visualizador web do VLibras. Ele encapsula o avatar em uma janela flutuante (**widget**) que fica sempre sobreposta a outras janelas, ideal para apresentações, aulas e acessibilidade em tempo real.

O sistema utiliza:
1.  **Faster Whisper:** Para reconhecimento de fala offline de alta precisão.
2.  **API VLibras V2:** Para tradução gramatical correta (Português -> Glosa Libras).
3.  **PyWebView:** Para renderizar o avatar Unity em uma janela desktop leve.

## :sparkles: Funcionalidades

* 🎤 **Reconhecimento de Voz:** Captação de áudio e transcrição automática a cada 3 segundos.
* 🧠 **Tradução Inteligente:** Converte frases do português para a estrutura gramatical de Libras (ex: "O gato comeu" -> "GATO COMER").
* 🖥️ **Interface Responsiva:** Janela "Sempre no Topo" (Always on Top) com tela de carregamento.
* ⚙️ **Controles:** Ajuste de velocidade da animação em tempo real.
* 🚀 **Performance:** Lógica de fila e *debounce* para evitar atropelamento de sinais.

## :hammer_and_wrench: Instalação e Execução

### Pré-requisitos
* Python 3.8 ou superior instalado.
* Git instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/KaazTiel/audio_vlibras_desktop.git](https://github.com/KaazTiel/audio_vlibras_desktop.git)
    cd audio_vlibras_desktop
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o projeto:**
    ```bash
    python main.py
    ```

> **Nota:** Na primeira execução, o sistema irá baixar automaticamente o modelo de IA do Whisper (aprox. 500MB a 1.5GB dependendo da versão). Isso pode levar alguns minutos.

## :gear: Configuração Técnica

O projeto é dividido em dois módulos principais para facilitar a manutenção:

* `main.py`: Gerencia a interface gráfica, o servidor local do avatar e a ponte entre o Python e o Javascript.
* `reconhecimento.py`: Módulo isolado responsável por capturar o áudio do microfone e processar com o Faster Whisper.

## :memo: Licença e Créditos

Este projeto utiliza o motor gráfico do **VLibras** (Governo Federal do Brasil) e é baseado no wrapper web original de [Luan de Gregori](https://github.com/luangregori).

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.md) para mais detalhes.

---
Desenvolvido com 💙 para acessibilidade.