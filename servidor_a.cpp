#include <iostream>
#include <memory>
#include <string>
#include <grpcpp/grpcpp.h>
#include "calculadora.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;

using calculadora::Calculadora;
using calculadora::OperacaoRequest;
using calculadora::ResultadoResponse;

class CalculadoraServiceImpl final : public Calculadora::Service {
  Status Soma(ServerContext* context, const OperacaoRequest* request, ResultadoResponse* response) override {
    double resultado = request->numero1() + request->numero2();
    response->set_resultado(resultado);
    return Status::OK;
  }

  Status Subtracao(ServerContext* context, const OperacaoRequest* request, ResultadoResponse* response) override {
    return Status(grpc::StatusCode::UNIMPLEMENTED, "Subtracao não implementada no Servidor A.");
  }
};

void RunServer() {
  std::string server_address("0.0.0.0:50052");
  CalculadoraServiceImpl service;

  ServerBuilder builder;
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  builder.RegisterService(&service);

  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Servidor A (Adição) ouvindo em " << server_address << std::endl;
  server->Wait();
}

int main() {
  RunServer();
  return 0;
}
