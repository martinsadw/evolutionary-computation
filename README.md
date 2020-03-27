Adaptive Curricular Sequence with Evolutionary Computation
==========================================================

Requisitos
----------

- Python 3
    - Numpy
    - Matplotlib

Você pode instalar as dependências com os seguintes comandos:

```
apt install python3-pip python3-tk
pip3 install -r requirements.txt
```

Executando
----------

### Geração da base de materiais

### Escolha dos parâmetros

A escolha dos parâmetros para cada algoritmo é feita utilizando o pacote irace.

### Geração do arquivo de resultados

Para gerar os dados de comparação entre os métodos basta executar o arquivo `generate_data.py`. Por exemplo, para gerar os dados para a base `real` com 100000 avaliações da função objetivo, 5 repetições e excluindo os testes com o PSO execute o seguinte comando:

```
python3 -m generate_data instances/real/instance.txt -n results/real.pickle -b 100000 -r 5 --no-pso
```

#### Parâmetros

O comportamento da geração de dados pode ser controlado pelos seguintes parâmetros:

- `-r, --repetitions`: Número de vezes que os algoritmos serão executados. Múltiplas repetições são utilizadas para reduzir os efeitos da aleatoriedade das meta-heurísticas;
- `-b, --cost-budget`: Quantidade de avaliações da função objetivo permitidas para cada algoritmo. É utilizado como um critério de parada para os algoritmos;
- `-s, --max-stagnation`: Quantidade máxima de iterações sem melhorias no valor da função objetivo. É utilizado como um critério de parada para os algoritmos;
- `-i, --num-iterations`: Quantidade de iterações permitidas para cada algoritmo. É utilizado como um critério de parada para os algoritmos;
- `-f, --results-format`: Formato dos dados que serão gerados. Pode ser `simple` ou `full`;
- `-n, --results-name`: Nome do arquivo que será gerado;
- `--no-ppad`: Não executa os testes para o PPAD
- `--no-pso`: Não executa os testes para o PSO
- `--no-ga`: Não executa os testes para o GA
- `--no-de`: Não executa os testes para o DE

É necessário especificar pelo menos um dos critérios de parada (`-b`, `-s` ou `-i`). Caso multiplos critérios de parada sejam definidos os algoritmos serão interrompidos quando o primeiro critério de parada ocorrer.

#### Resultados

Existem dois formatos de dados disponíveis para a geração dos dados:

- `simple`: Retorna uma tupla `(selected_materials, cost_value, partial_fitness_array)`. Gera arquivos menores, mas inclui apenas os materiais selecionados e os dados parciais de custo e valor de cada função objetivo ao longo das iterações.
- `full`: Retorna uma tupla `(selected_materials, cost_value, best_fitness_array, partial_fitness_array, perf_counter_array, process_time_array)`. Gera arquivos maiores mas, além dos dados gerados pelo formato `simple`, inclui dados de tempo de execução dos algoritmos. Além disso retorna o valor da função objetivo final (esse valor pode ser calculado a partir de `partial_fitness_array`).

Exemplo das informações contidas no arquivo gerado:

```json
{
    "info": {
        "algorithms": ["ppa_d", "ga", "de"],
        "command": "generate_data.py instances/real/instance.txt -n results/real.pickle -b 10 --no-pso",
        "datetime": "2020-03-27 15:06:24.658132",
        "instance": <acs.instance.Instance object>,
        "cost_budget": 100000,
        "max_stagnation": None,
        "num_iterations": None,
        "repetitions": 5,
        "results_format": "simple",
        "results_name": "results/real.pickle"
    },
    "ppa_d": [...],
    "ga": [...],
    "de": [...]
}
```

- `algorithms`: Lista de algoritmos incluidos no arquivo de resultados;
- `command`: Comando utilizado para gerar os dados;
- `datetime`: Data da geração dos dados;
- `instance`: Dados da instância utilizada no arquivo de resultados;
- `cost_budget`: Valor do parametro `-b`;
- `max_stagnation`: Valor do parametro `-s`;
- `num_iterations`: Valor do parametro `-i`;
- `repetitions`: Valor do parametro `-r`;
- `results_format`: Valor do parametro `-f`;
- `results_name`: Valor do parametro `-n`;
- `ppa_d`, `pso`, `ga` e `de`: Dados gerados por cada um dos algotimos.


### Geração dos gráficos

Os códigos utilizados para a geração dos gráficos estão na pasta `graphics`. Todos eles dependem de gerar o arquivo de resultados previamente.


Datasets
--------

Todos os datasets se encontram na pasta `instances`
