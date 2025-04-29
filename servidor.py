from concurrent import futures
import grpc
import calculadora_pb2
import calculadora_pb2_grpc

class CalculadoraServicer(calculadora_pb2_grpc.CalculadoraServicer):
	def Soma(self, request, context):
		resultado = request.numero1 + request.numero2
		return calculadora_pb2.ResultadoResponse(resultado=resultado)

	def Subtracao(self,request,context):
		resultado = request.numero1 - request.numero2
		return calculadora_pb2.ResultadoResponse(resultado=resultado)

def servir():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	calculadora_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicer(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	print("Servidor gRPC rodando na porta 50051...")
	server.wait_for_termination()

if __name__ == '__main__':
	servir()
