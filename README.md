# Calculadora gRPC

## Tecnologias utilizadas

- gRPC e gRPC toots
- Flask
- HTML
- Python

Dependendo do ambiente de desenvolvimento será necessário criar um ambiente virtual para poder baixar as ferramentas necessárias

## Ambiente

Para gerar calculadora_pb2.py e calculadora_pb_grpc.py:

``` bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto
```

Para subir o servidor

``` bash
python3 servidor.py
```

Servidor rodando na porta 50051

Para subir o cliente

``` bash
python3 cliente_web.py
```

Agora é possível acessar na porta **http://localhost:5000/** a aplicação web conectada ao web server + stub gRPC que irá calcular e retornar os resultados de soma ou subtração

> É necessário que servidor e cliente estejam em terminais diferentes e funcionando ao mesmo tempo