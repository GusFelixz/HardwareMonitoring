// Credenciais do MQTT
const username = "";
const password = "";

// Conexão com o broker MQTT via WebSocket
const brokerUrl = ""; // Broker MQTT público com WebSocket
const client = mqtt.connect(brokerUrl, {
    username: username,
    password: password
});

// Status de conexão
client.on("connect", () => {
    console.log("Conectado ao broker MQTT!");
});

client.on("error", (err) => {
    console.error("Erro de conexão:", err);
});

// Assinatura de tópicos
document.getElementById("subscribeButton").addEventListener("click", () => {
    const topic = document.getElementById("topic").value;
    if (topic) {
        client.subscribe(topic, (err) => {
            if (!err) {
                console.log(`Inscrito no tópico: ${topic}`);
            } else {
                console.error("Erro ao se inscrever:", err);
            }
        });
    } else {
        alert("Por favor, insira um tópico.");
    }
});

// Recepção de mensagens
client.on("message", (topic, message) => {
    const messageList = document.getElementById("messageList");

    // Criar uma nova mensagem
    const newMessage = document.createElement("div");
    newMessage.className = "message";
    newMessage.textContent = `[${topic}] ${message}`;

    // Adicionar ao DOM
    messageList.appendChild(newMessage);

    // Rolagem automática para a última mensagem
    messageList.scrollTop = messageList.scrollHeight;
});
