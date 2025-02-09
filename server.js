const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const port = 3000;

// Abilita CORS e JSON parsing
app.use(cors());
app.use(express.json());

// Servire file statici (ad esempio file HTML, CSS, JS)
app.use(express.static(path.join(__dirname)));

// Rotta principale per verificare se il server funziona
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'home.html')); // Assicurati che esista il file "home.html"
});

// Rotta per AI.html
app.get('/AI.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'AI.html')); // Assicurati che esista il file "AI.html"
});

// Rotta per il chatbot (gestisce le richieste POST per l'AI)
app.post('/get_response', (req, res) => {
    const userInput = req.body.user_input.toLowerCase(); // Converti l'input a minuscolo per evitare problemi di maiuscole/minuscole

    // Risposte predefinite
    const risposteAI = {
        "ciao": "Ciao! Come posso aiutarti oggi?",
        "come stai?": "Sto bene, grazie! E tu come stai?",
        "sto bene": "Sono felice di sentirlo! 😊",
        "sto male": "Mi dispiace sentirlo. C'è qualcosa che posso fare per aiutarti? 💖",
        "chi sei?": "Sono un'AI creata per aiutarti con le tue domande e necessità!",
        "come ti chiami?": "Mi chiamo SmartLife AI, piacere di conoscerti! 😊",
        "grazie": "Prego! Sono qui per aiutarti. 🌟",
        "addio": "Arrivederci! Spero di rivederti presto. 👋",
        "default": "Non ho capito bene, puoi ripetere?"
    };

    // Cerca la risposta corrispondente o usa quella di default
    const aiResponse = risposteAI[userInput] || risposteAI["default"];
    res.json({ response: aiResponse });
});

// Avvia il server
app.listen(port, () => {
    console.log(`Server in ascolto su http://localhost:${port}`);
});
