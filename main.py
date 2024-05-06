from flask import Flask, jsonify, request
from sqldb import add_user, add_payment
import json
import os

app = Flask(__name__)

def liberar_acesso(email):
  print(f"Liberar acesso do e-mail: {email}")


def enviar_mensagem_boas_vindas(email):
  print(f"Enviar mensagem de boas vindas para o e-mail: {email}")


def revogar_acesso(email):
  print(f"Revogar acesso do e-mail: {email}")


@app.route("/", methods=["POST"])
def webhook():
    

    data_byte = request.get_data()

    # Converte os dados bytes para string
    data_str = data_byte.decode('utf-8')

    # Converte a string JSON para um dicionário Python
    data = json.loads(data_str)

    nome = data.get("nome","")
    email = data.get("email","")
    status = data.get("status","")
    payment_method = data.get("forma_pagamento","")
    value = data.get("valor","")
    plots = data.get("parcelas","")

    
    user = add_user(nome, email, status)
    payment = add_payment(user[0], status, payment_method, plots, value)

    if user[2] == status:
        if status == "aprovado":
            liberar_acesso()
            enviar_mensagem_boas_vindas()
        elif status == "recusado":
            print("O pagamento foi recusado")
        elif status == "reembolsado":
            revogar_acesso(email)
        else:
            print("Status", status)

    return jsonify({"message": "Webhook recebido com sucesso"})
 

@app.route("/", methods=["GET"])
def get_webhook():
  data = request.get_data()

  print(data)
  print("Web Hook")
  return {"cod": 200}


if __name__ == '__main__':
  app.run(debug=True, port=os.getenv("PORT", default=5000))
