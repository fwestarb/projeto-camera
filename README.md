# Projeto Câmera / Camera Project

Dois experimentos de visão computacional com **Python, OpenCV e MediaPipe**: desenho por gestos e lembrete de postura. / Two computer vision experiments: gesture drawing and a posture reminder.

## Português

### O que faz

- `desenho.py`: desenha sobre a imagem da webcam ao aproximar polegar e indicador. Inclui lápis, borracha e limpeza do quadro.
- `app.py`: acompanha orelhas e ombros e mostra um alerta quando a distância vertical fica abaixo de um limite configurável.
- Processamento local. Não grava nem envia imagens da câmera. No primeiro uso, baixa os modelos de fontes oficiais do MediaPipe.

O lembrete usa uma regra geométrica simples sobre pontos detectados por um modelo pré-treinado. **Não é um diagnóstico médico nem um modelo treinado por mim.** O resultado varia com enquadramento, iluminação, posição da câmera e corpo da pessoa. O limite `0.23` veio da configuração pessoal do protótipo e precisa ser ajustado para cada uso.

### Instalação e execução

Ambiente verificado: Windows e Python 3.12. Internet necessária para instalar dependências e baixar os modelos na primeira execução.

```powershell
git clone https://github.com/fwestarb/projeto-camera.git
cd projeto-camera
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe desenho.py
# Ou:
.\.venv\Scripts\python.exe app.py --limit 0.23
```

Se a câmera errada for selecionada, acrescente `--camera 1` (ou outro índice). Também é possível configurar `CAMERA_INDEX`. Para desligar o alerta sonoro no Windows, use `app.py --mute`.

**Desenho:** pinça para desenhar; indicador estendido para mover o cursor no quadro; feche a mão com o cursor sobre o botão para trocar ferramenta. Teclas: **E** troca lápis/borracha, **C** limpa e **Q** sai. No monitor de postura, **Q** sai.

O controle do mouse do computador é opcional. Para usá-lo, instale `requirements-mouse.txt` e execute `desenho.py --mouse`. Esse modo também move e clica fora da janela; o mecanismo de parada do PyAutoGUI permanece ligado. Ele não foi validado nesta etapa.

**Calibração:** observe a distância mostrada em uma posição confortável e depois compare com a posição que quer evitar. Escolha um limite entre esses valores. Se o corpo não estiver visível com confiança, o programa não calcula a distância.

### Verificação — 02/10/2026

- Quatro testes automatizados: distância de postura, baixa confiança/dados inválidos, distância entre dedos e liberação da câmera após falha.
- Os dois modelos carregaram e processaram um quadro vazio.
- Uma webcam local forneceu quadros de 640 × 480; nenhuma imagem foi salva.
- Reconhecimento de gestos, calibração de postura, áudio e controle do mouse ainda precisam de teste manual. Nenhum vídeo de demonstração foi gravado nesta etapa.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Modelos, ambiente virtual, caches e mídias antigas não são publicados no repositório. Fontes dos modelos e instruções: [Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker/python) e [Pose Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker/python). Os modelos seguem os termos dos respectivos fornecedores.

## English

### Features

- `desenho.py`: draw over the webcam image using a thumb/index pinch. Pencil, eraser and canvas clearing are included.
- `app.py`: track ears and shoulders and display a reminder when their vertical distance drops below a configurable threshold.
- Camera images are processed locally and are not recorded or uploaded. On first use, the apps download pretrained MediaPipe models from official sources.

The posture reminder applies a simple geometric rule to pretrained-model landmarks. It is **not a medical diagnosis or a model I trained**. Camera placement, lighting and body position affect the result. The default `0.23` threshold comes from a personal prototype calibration and should be adjusted.

### Setup and use

Tested environment: Windows, Python 3.12. Use the installation commands above. Run `desenho.py` for drawing or `app.py --limit 0.23` for the posture reminder. Use `--camera 1` to select a different camera, or set `CAMERA_INDEX`. `app.py --mute` disables the Windows sound alert.

Pinch to draw; point your index finger to move the canvas cursor; close your hand over the tool button to switch pencil/eraser. **E** switches tools, **C** clears the canvas and **Q** exits. Optional system mouse control requires `requirements-mouse.txt` and `desenho.py --mouse`; PyAutoGUI's fail-safe remains enabled.

To calibrate, compare the displayed distance in a comfortable position with the position you want to avoid, then choose a threshold between those readings. Low-confidence landmarks are ignored.

### Validation — October 2, 2026

Four automated tests passed. Both models loaded and processed an empty image; a local webcam returned 640 × 480 frames without recording. Gesture interaction, posture calibration, sound and optional mouse control still require manual validation. No real demo video has been recorded yet.

Run the test command above to check the core logic. Model binaries, virtual environments, caches and old media are excluded from the repository; see the official model documentation linked above.


## Site do projeto / Project website

[Apresentação, prints, instalação e download / Overview, screenshots, setup and download](https://fwestarb.github.io/projeto-camera/).

Código do site: [website](website). Publicação e testes: [docs/SITE.md](docs/SITE.md).

Outros projetos / Other projects: [ESP32 Tera](https://fwestarb.github.io/esp32-tera/) · [GhostReply](https://fwestarb.github.io/ghostreply/) · [Projeto Câmera](https://fwestarb.github.io/projeto-camera/).
