import json
from flask import Flask, render_template, request, jsonify
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
from datetime import datetime
import os

# Carica il modello GPT-2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Carica i file JSON (tasks.json ed emotions.json)
try:
    with open('tasks.json', 'r') as f:
        tasks_data = json.load(f)

    with open('emotions.json', 'r') as f:
        emotions_data = json.load(f)
except Exception as e:
    print(f"Errore nel caricamento dei file JSON: {e}")
    tasks_data = []
    emotions_data = []

# Funzione per analizzare il tono dell'utente (semplice esempio)
def analyze_emotion(user_input):
    if "felice" in user_input or "contento" in user_input:
        return "positivo"
    elif "triste" in user_input or "giù" in user_input:
        return "triste"
    elif "stressato" in user_input or "ansioso" in user_input:
        return "stressato"
    elif "stanco" in user_input:
        return "stanco"
    else:
        return "neutro"

# Funzione per rispondere a emozioni conosciute
def get_emotion_response(user_input):
    for emotion in emotions_data:
        if emotion['user_message'].lower() in user_input.lower():
            return emotion['ai_response']
    return None  # Se non c'è una risposta predefinita per quell'emozione

# Funzione per il reminder dei task
def task_reminder():
    today = datetime.today().strftime('%Y-%m-%d')
    reminder_message = []
    
    for task in tasks_data:
        if task['date'] == today:
            reminder_message.append(f"Oggi devi {task['task']}.")
    
    if reminder_message:
        return " ".join(reminder_message)
    return "Non hai compiti urgenti oggi, ma ricordati di fare un piano per domani!"

# Funzione per risposte motivanti e divertenti da palestra
def gym_motivation():
    insults = [
        "Dai, smettila di lamentarti! Non ti stai allenando abbastanza duramente!",
        "Cosa stai facendo? Alzare solo il bicchiere per bere? Su, muoviti!",
        "Forza! Non hai ancora sudato abbastanza per chiamarlo allenamento!"
    ]
    motivations = [
        "Non mollare, che il tuo futuro te ne sarà grato!",
        "Ogni ripetizione conta! Continua così, fra poco sarai un campione!",
        "Se non senti la fatica, allora non stai facendo abbastanza! Datti dentro!"
    ]
    advice = [
        "Ricorda, una buona alimentazione è fondamentale per ottenere risultati. Mangia sano!",
        "Non dimenticare di fare stretching prima e dopo gli allenamenti. Prevenire gli infortuni è la chiave!",
        "I muscoli crescono mentre riposi, non solo mentre ti alleni. Riposo e nutrizione sono fondamentali!"
    ]
    
    return random.choice(insults) + " " + random.choice(motivations) + " " + random.choice(advice)

# Funzione per generare una risposta personalizzata
def generate_response(user_input, conversation_context, user_preferences):
    # Risposta specifica per "ciao"
    if user_input.lower() == "ciao":
        return "Ciao! Come posso aiutarti oggi?"

    # Risposta motivazionale per la palestra
    if "mi serve motivazione" in user_input.lower() or "ho bisogno di motivazione" in user_input.lower():
        return gym_motivation()

    # Controlla emozioni
    emotion_response = get_emotion_response(user_input)
    if emotion_response:
        return emotion_response

    # Risposta ai task reminder
    if "compiti" in user_input.lower() or "scadenza" in user_input.lower():
        reminder = task_reminder()
        return reminder

    emotion = analyze_emotion(user_input)
    
    if emotion == "positivo":
        response = "Sono felice che tu sia felice! 😊"
    elif emotion == "triste":
        response = "Mi dispiace sentirlo, spero che vada meglio presto. ❤️"
    elif emotion == "stressato":
        response = "Capisco, lo stress può essere difficile. Prova a fare una pausa e respirare profondamente."
    elif emotion == "stanco":
        response = "Capisco, magari una pausa ti farà bene! ☕"
    elif "palestra" in user_input.lower() or "allenamento" in user_input.lower():
        response = gym_motivation()
    else:
        input_text = conversation_context + " " + user_input + tokenizer.eos_token
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        
        response_ids = model.generate(input_ids, max_length=50, num_return_sequences=1,
                                      no_repeat_ngram_size=2, top_k=50, top_p=0.95,
                                      temperature=0.8)
        response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    
    return response

# Imposta Flask
app = Flask(__name__)

# Rotta per la pagina principale
@app.route('/')
def index():
    return render_template('AI.html')

# Rotta per ricevere il messaggio dell'utente e rispondere con l'IA
@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_input = request.json['user_input']  # Usa .json invece di .form
        conversation_context = ""
        user_preferences = {}

        if "musica" in user_input.lower():
            user_preferences['musica'] = "rock"
        elif "sport" in user_input.lower():
            user_preferences['sport'] = "calcio"

        response = generate_response(user_input, conversation_context, user_preferences)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Errore nel server: {str(e)}")
        return jsonify({'response': 'Si è verificato un errore sul server. Riprova più tardi.'}), 500

if __name__ == "__main__":
    app.run(debug=True)
