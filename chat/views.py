from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
import json
from .utils.conn import realiza_conn
import google.generativeai as genai

def home(request):
    return render(request,'chat/home.html', context= {
        'name':'Cleber',
    })

def orcamento(request):
    return HttpResponse("orcamento")

def chatboot (request):
    
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Realize a consulta no banco de dados com base na mensagem do usuário
        response_message = consulta_no_banco(user_message)

        # Retorne a resposta em formato JSON
        return JsonResponse({"response": response_message})
    return render(request,'chatboot.html')

def consulta_no_banco(message):
    api_key = "AIzaSyAB7vQz13VNcrEwRJ81Ek-PBL9x05jyTFM"
    genai.configure(api_key=api_key)

    # Inicializando o modelo especificado na documentação
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Inicializa uma lista para armazenar o contexto da conversa
    contexto = []

    json_orcament = realiza_conn(303258)
    json_orcament_str = json.dumps(json_orcament, indent=4)
    
    contexto.append(f"Usuário: {message.lower()}")

    prompt_completo = "\n".join(contexto) + "\n" + json_orcament_str

    response = model.generate_content(prompt_completo)

    # Formata a resposta para HTML, substituindo quebras de linha por <br> ou <pre> para manter o formato
    resposta_formatada = f"<pre>{response.text}</pre>"

    return "Aqui está sua resposta:", resposta_formatada