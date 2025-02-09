function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const chatWindow = document.getElementById("chat-window");

    // Aggiungi il messaggio dell'utente alla chat
    const userMessage = document.createElement("div");
    userMessage.className = "message";
    userMessage.textContent = "Tu: " + userInput;
    chatWindow.appendChild(userMessage);

    // Pulisci il campo di input
    document.getElementById("user-input").value = "";

    // Invia il messaggio al server
    fetch("/get_response", {
        method: "POST",
        body: new URLSearchParams({ user_input: userInput }),
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    })
    .then(response => response.json())
    .then(data => {
        // Mostra la risposta dell'IA
        const aiMessage = document.createElement("div");
        aiMessage.className = "message";
        aiMessage.textContent = "AI: " + data.response;
        chatWindow.appendChild(aiMessage);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    })
    .catch(error => {
        console.error("Errore:", error);
    });
}
