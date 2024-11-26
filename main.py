import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt_client
import psutil

# Função de publicação no MQTT
def publish_mqtt_data():   
    machine_status = get_machine_status()
    try:       
        client.publish("maquina/monitoramento", machine_status)  # Usando o cliente MQTT
        status_label.config(text="Enviado: " + machine_status)
    except Exception as e:
        messagebox.showerror("Erro MQTT", str(e))

# Função de conexão com o broker MQTT
def connect_to_mqtt():
    try:
        client.connect(broker_address, broker_port, 60)  # Usando a variável correta
        client.loop_start()
        messagebox.showinfo("Conexão", "Conectado ao servidor MQTT!")
    except Exception as e:
        messagebox.showerror("Erro de Conexão", str(e))

# Configuração do MQTT
broker_address = "localhost"  # Endereço do broker MQTT
broker_port = 1883

client = mqtt_client.Client()  # Cliente MQTT

# Método para pegar as informações da máquina
def get_machine_status():
    uso_cpu = psutil.cpu_percent(interval=1)  # Uso da CPU em %
    memoria = psutil.virtual_memory()  # Memória virtual
    disco = psutil.disk_usage('/')  # Uso de disco
    temp = psutil.sensors_temperatures() if hasattr(psutil, 'sensors_temperatures') else None  # Verifica a temperatura

    # Obtendo as informações de status em formato de string
    status = f"CPU: {uso_cpu}% | Memória: {memoria.percent}% | Disco: {disco.percent}%"

    # Adicionando a temperatura se disponível
    if temp and 'coretemp' in temp:
        cpu_temp = temp['coretemp'][0].current  # Acessa a temperatura do CPU
        status += f" | Temperatura: {cpu_temp}°C"
    else:
        status += " | Temperatura: Indisponível"

    return status

# GUI Tkinter
def update_status():
    machine_status = get_machine_status()
    status_label.config(text=f"Status: {machine_status}")

def auto_update_status():
    update_status()
    root.after(5000, auto_update_status)  # Atualiza a cada 5 segundos

def setup_gui():
    global root, status_label, client  # Tornando a variável global para usá-la em várias funções

    root = tk.Tk()
    root.title("Monitoramento de Máquina")

    # Título
    title_label = tk.Label(root, text="Monitoramento de Máquina", font=("Arial", 16))
    title_label.pack(pady=10)

    # Status da máquina
    status_label = tk.Label(root, text="Status: Desconhecido", font=("Arial", 12))
    status_label.pack(pady=10)

    # Botão para publicar dados
    send_button = tk.Button(root, text="Enviar Dados", command=publish_mqtt_data)  # Adicionando o comando
    send_button.pack(pady=10)

    # Botão para conectar ao servidor MQTT
    connect_button = tk.Button(root, text="Conectar ao Servidor MQTT", command=connect_to_mqtt)  # Adicionando o comando
    connect_button.pack(pady=10)

    # Atualização automática do status
    auto_update_status()

    # Loop da interface gráfica
    root.mainloop()

# Executa GUI
setup_gui()
