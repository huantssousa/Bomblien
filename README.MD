Meu Jogo de Plataforma -  BOMBLIEN
Este é um jogo de plataforma e ação 2D desenvolvido em Python com a biblioteca Pygame Zero. O objetivo é guiar o herói por um percurso cheio de inimigos, utilizando bombas e pulos para sobreviver e alcançar a bandeira da vitória no final.

Requisitos
Para rodar este jogo, você precisa ter o Python 3 instalado, juntamente com a biblioteca Pygame Zero.

Python 3.12.6

Pygame Zero

Para instalar a biblioteca necessária, abra o seu terminal (CMD, PowerShell, etc.) e execute o seguinte comando:

pip install pgzero

Estrutura de Arquivos
Para que o jogo encontre as imagens e sons corretamente, a pasta do seu projeto precisa seguir esta estrutura:

seu_projeto/
├── main.py              <-- Código principal
│
├── images/              <-- Pasta para TODAS as imagens
│   ├── frente.png
│   ├── bomba.png
│   ├── joaninha.png
│   ├── rato.png
│   ├── vida.png
│   └── ... (etc.)
│
├── sounds/              <-- Pasta para EFEITOS SONOROS curtos
│   ├── bat.wav
│   ├── bomb.ogg
│   ├── jump.ogg
│   └── jump2.ogg
│
└── music/               <-- Pasta para a MÚSICA DE FUNDO
    └── music_fundo.mp3
Como Executar o Jogo:
Abra um terminal (CMD, PowerShell no Windows, ou Terminal no Mac/Linux).

Navegue com o comando cd até a pasta onde você salvou os arquivos do jogo.

Dentro da pasta basta executar: python -m pgzero main.py