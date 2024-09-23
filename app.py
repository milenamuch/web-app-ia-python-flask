from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form. PT: Lê os valores do formulario
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env. PT: Carrega as configurações setadas no arquivo .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language. PT: Indica o que queremos traduzir e o idioma escolhido
    path = '/translate?api-version=3.0'
    # Add the target language parameter. pT: Adiciona um rótulo no parâmetro do idioma
    target_language_parameter = '&to=' + target_language
    # Create the full URL. PT: Cria a url
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key. PT: Configura o cabeçalho 
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated. PT: Cria o corpo da requisição com o texto a ser traduzido
    body = [{ 'text': original_text }]

    # Make the call using post. PT: Faz uma requisição via POST
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response. PT: Devolve um arquivo json
    translator_response = translator_request.json()
    # Retrieve the translation. PT: Devolve a tradução
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template PT: Chama render_template para exibir a página de resposta
    return render_template( 
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )