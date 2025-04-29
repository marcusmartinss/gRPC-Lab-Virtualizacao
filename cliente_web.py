from flask import Flask, render_template, request, jsonify
import grpc
import calculadora_pb2
import calculadora_pb2_grpc

app = Flask(__name__)

def criar_stub():
	canal = grpc.insecure_channel('localhost:50051')
	return calculadora_pb2_grpc.CalculadoraStub(canal)

@app.route('/')

def index():
	return render_template('calculadora.html')

@app.route('/calcular', methods=['POST'])
def calcular():
	data = request.json
	operacao = data['operacao']
	num1 = float(data['num1'])
	num2 = float(data['num2'])
	stub = criar_stub()
	try:
		if operacao == 'soma':
			resposta = stub.Soma(calculadora_pb2.OperacaoRequest(numero1=num1, numero2=num2))
		elif operacao == 'subtracao':
			resposta = stub.Subtracao(calculadora_pb2.OperacaoRequest(numero1=num1, numero2=num2))
		else:
			return jsonify({'erro':'Operação inválida'}), 400

		return jsonify({'resultado':resposta.resultado})

	except grpc.RpcError as e:
		return jsonify({'erro':e.details()}), 400

if __name__ == '__main__':
	app.run(debug=True, port=5000)
