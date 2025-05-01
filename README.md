# gRPC-Lab-Virtualizacao

Este repositório contém o desenvolvimento em grupo de um sistema distribuído utilizando gRPC para comunicação entre serviços. O projeto consiste em um servidor web que se comunica com um stub central, o qual gerencia a interação com dois stubs secundários.

## Arquitetura

             [Cliente Web] 
                   |
                   v
          [Servidor Central] 
             /         \
            v           v
     [Servidor A]    [Servidor B] 
    (Adição:50052) (Subtração:50053)

## Tecnologias utilizadas

- gRPC e gRPC tools
- Protobuf
- Flask
- HTML
- Python
- C++

Dependendo do ambiente de desenvolvimento será necessário criar um ambiente virtual para poder baixar as ferramentas necessárias

## Ambiente

### Pré-requisitos

```bash
sudo apt update
sudo apt install -y build-essential autoconf libtool pkg-config cmake git python3-pip
pip install grpcio grpcio-tools flask
```

### Instalação gRPC

```bash
export MY_INSTALL_DIR=/usr/local
git clone --recurse-submodules -b v1.71.0 --depth 1 https://github.com/grpc/grpc
cd grpc
mkdir -p cmake/build && cd cmake/build
cmake -DgRPC_INSTALL=ON -DCMAKE_INSTALL_PREFIX=$MY_INSTALL_DIR ..
make -j$(nproc)
sudo make install
sudo ldconfig
```

### Instalação Protobuf

```bash
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.15.8/protoc-3.15.8-linux-x86_64.zip
unzip protoc-3.15.8-linux-x86_64.zip -d protoc3
sudo mv protoc3/bin/* /usr/local/bin/
sudo mv protoc3/include/* /usr/local/include/
```

## Configuração dos Servidores Secundários

**1. Para gerar os arquivos C++ padrão do Protobuf**

```bash
protoc -I=. --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) calculadora.proto
```

**2. Para compilar os servidores secundários**

```bash
# Compilar Servidor A (Adição)
g++ -std=c++17 -o servidor_a servidor_a.cpp calculadora.pb.cc calculadora.grpc.pb.cc \
    $(pkg-config --cflags --libs grpc++ protobuf) \
    -lssl -lcrypto -lre2 -lcares -lupb -lz -lpthread -laddress_sorting

# Compilar Servidor B (Subtração)
g++ -std=c++17 -o servidor_b servidor_b.cpp calculadora.pb.cc calculadora.grpc.pb.cc \
    $(pkg-config --cflags --libs grpc++ protobuf) \
    -lssl -lcrypto -lre2 -lcares -lupb -lz -lpthread -laddress_sorting

# Dando permissão para os binários
chmod +x servidor_a servidor_b
```

**3. Execução dos servidores secundários**

```bash
# Terminal 1 - Servidor A (Adição na porta 50052)
./servidor_a
```

```bash
# Terminal 2 - Servidor B (Subtração na porta 50053)
./servidor_b
```

## Configuração do Servidor Web

**1. Para gerar `calculadora_pb2.py` e `calculadora_pb_grpc.py`:**

``` bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculadora.proto
```

**2. Para subir o Servidor Web**

``` bash
# Terminal 3 - Servidor Web na porta 50051
python3 servidor.py
```

**3. Para subir o Web**

``` bash
# Terminal 4 - Cliente Web na porta 5000
python3 cliente_web.py
```

Agora é possível acessar na porta **http://localhost:5000/** a aplicação web conectada ao web server + stub gRPC que irá calcular e retornar os resultados de soma ou subtração

> É necessário que servidor e cliente estejam em terminais diferentes e funcionando ao mesmo tempo
