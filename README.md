# Robox Forever

Trata-se de um jogo do estilo Sokoban, onde o usuário controla um jogador com o objetivo de empurrar caixas para uma posição destacada.
Para rodar o jogo: 

-git clone https://github.com/jhorn26/robox_forever.git
-pip install pygame 
python ./final.py

## final.py

Nosse arquivo temos a classe Game, que inicia o jogo, a Level, para criar o level selecionado pelo usuário,  a Screen, responsável pelas diferentes janelas que temos no decorrer do jogo (tela inicial, tela de seleção do jogo, tela do jogo rodando e tela de vitória), e a Button, que define o level a partir do botão que o usuário clicar.

## sprites.py

Aqui definimos as nossas sprites, Robo (o nosso jogador), Box (as caixas que o jogador vai empurrar), Goal (a posição em que as caixas devem estar para completar o level), Well (as paredes que delimitam o espaço que o jogador e as caixas podem circular) e Floor (o chão onde o jogador e as caixas circulam).

## levels.txt

Arquivo com as posições das sprites em cada level.

## images

Todas as imagens utilizadas no nosso jogo.

## sounds

Todos os sons utilizados no nosso jogo.

## fonts

A fonte utilizada em todas as palavras do jogo.

## docs 

Arquivos contendo a documentação. Para abrir o HTML do site da documentação, abra ./docs/_build/html/index.html

## diagrams

Arquivos contendo os PDFs dos diagramas e um PDF explicativo sobre o jogo.


## auxiliar

### create_level.py

Funções auxiliares para o _poligon.py_.

### poligon.py

Usado para escrever o _levels.txt_.
