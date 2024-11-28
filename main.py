import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt_client
import psutil

broker_address = ""
broker_port = 

client = mqtt_client.Client()

def get_machine_status():
    uso_cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    status = f"CPU: {uso_cpu}% | Memória: {memoria.percent}% | Disco: {disco.percent}%"
    return status

def publish_mqtt_data():   
    machine_status = get_machine_status()
    try:       
        client.publish("maquina/monitoramento", machine_status)
        status_label.config(text="Enviado: " + machine_status)
    except Exception as e:
        messagebox.showerror("Erro MQTT", str(e))

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        root.after(0, lambda: messagebox.showinfo("Conexão", "Conectado ao servidor MQTT!"))
    else:
        root.after(0, lambda: messagebox.showerror("Erro de Conexão", f"Código de retorno: {rc}"))

def connect_to_mqtt():
    try:
        client.username_pw_set(username="Gusta1", password="123456Ig")
        client.tls_set()
        client.connect(broker_address, broker_port, 60)
        client.loop_start()
    except Exception as e:
        messagebox.showerror("Erro de Conexão", str(e))

client.on_connect = on_connect

def auto_update_status():
    update_status()
    root.after(5000, auto_update_status)

def update_status():
    machine_status = get_machine_status()
    status_label.config(text=f"Status: {machine_status}")

def setup_gui():
    global root, status_label
    root = tk.Tk()
    root.title("Monitoramento de Máquina")

    title_label = tk.Label(root, text="Monitoramento de Máquina", font=("Arial", 16))
    title_label.pack(pady=10)

    global status_label
    status_label = tk.Label(root, text="Status: Desconhecido", font=("Arial", 12))
    status_label.pack(pady=10)

    send_button = tk.Button(root, text="Enviar Dados", command=publish_mqtt_data)
    send_button.pack(pady=10)

    connect_button = tk.Button(root, text="Conectar ao Servidor MQTT", command=connect_to_mqtt)
    connect_button.pack(pady=10)

    auto_update_status()
    root.mainloop()

setup_gui()
