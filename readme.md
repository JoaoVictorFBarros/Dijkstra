# Roteamento com Algoritmo de Dijkstra

O **roteamento de rede** é o processo pelo qual pacotes de dados são direcionados de um ponto a outro em uma rede de computadores. Utiliza-se um conjunto de algoritmos para determinar o melhor caminho entre o ponto de origem e o destino. O algoritmo de Dijkstra, que é utilizado neste projeto, é um dos algoritmos clássicos para encontrar o caminho mais curto entre dois pontos em um grafo. Ele trabalha determinando o menor custo total para alcançar o destino a partir de um nó de início, considerando as arestas e seus pesos.

### Clone o repositório
```bash
git clone https://github.com/JoaoVictorFBarros/Dijkstra.git
```


### Instalação das Dependências

Se ainda não tiver as bibliotecas instaladas, use:

```
pip install tkinter networkx matplotlib
```

### Executando o Projeto

Para iniciar o simulador, execute:

```
python3 main.py
```
<div align="center">
<img src=print.png width=80%>
</div>

## Funcionalidades

- Adicionar e remover nós e arestas no grafo.
- Calcular e visualizar o caminho mais curto entre dois nós.
- Atualizar a visualização do grafo em tempo real.
