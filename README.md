# *Web Crawler* para extração da agenda da ALESC

Minha entrega para o teste técnico da **DataPolicy** para a vaga de desenvolvedor Python: implementação de um *web crawler* que extrai dados de eventos da agenda da [ALESC](https://www.alesc.sc.gov.br/agenda/) (Assembléia Legislativa do Estado de Santa Catarina). O programa aceita como entrada uma data em formato ISO 8601 (*e.g.*, 2025-01-12) para filtrar por eventos a partir dessa data.


## Instruções para execução
Para evitar problemas de incompatibilidade, é recomendado a execução do programa em um container Docker. Instruções de instalação podem ser consultadas [aqui](https://docs.docker.com/engine/install/).

Em ambientes Linux, o *script* `start.sh` pode ser utilizado com o comando `sh` para construir a imagem definida no `Dockerfile` e executar o programa, com todas as dependências definidas no arquivo `requirements.txt` já instaladas. \
A imagem é construída somente se não estiver disponível no *host*.

```sh
# ./start.sh
#! /usr/bin/sh

image="gscolombo/alesc-crawler:latest"


if [ -z "$(docker images -q $image 2> /dev/null)" ]; then
    echo "Image \"$image\" not found.\nStarting build...\n"
    docker build -t $image .
fi
echo "\n"
clear
docker run -itv $PWD/data:/home/datapolicy/data $image python src/main.py
```

No Windows, o [Git Bash](https://git-scm.com/) pode ser utilizado para execução do *script*. Além disso, pode ser necessário prefixar o comando `sh` com `winpty`, como abaixo.

```sh
winpty sh start.sh
```
Para obtenção e uso dos dados extraídos no *host*, a execução do container é configurada com uma montagem de ligação (*bind mount*) na pasta `data`, criada automaticamente caso não exista. \
Ao final da execução do programa, os dados em formato JSON deverão estar contidos nessa pasta.

Também é possível rodar o *script* Python diretamente, após instalar as dependências em `requirements.txt`.

```sh
pip install -r requirements

python src/main.py # No Windows
python3 src/main.py # Em ambientes Linux
```
A pasta `data` também será criada automaticamente nesse caso.



## Observações
O arquivo `compose.yaml` foi utilizado somente para facilitar o desenvolvimento no ambiente do container. Não é necessário utilizá-lo para executar o programa.

    
    
