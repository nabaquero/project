import tkinter as tk
import tkinter.messagebox

class NetworkSimulator:
    def __init__(self, root):
        # Inicialización de la ventana principal de la aplicación
        self.root = root
        self.root.title("Simulador de Red")

        # Definición de dispositivos y sus posiciones
        self.devices = {
            "switch": {"x": 250, "y": 200},
            "router1": {"x": 100, "y": 150, "ip": "192.168.1.1"},
            "router2": {"x": 250, "y": 50, "ip": "192.168.1.2"},
            "router3": {"x": 400, "y": 150, "ip": "192.168.1.3"},
            "router4": {"x": 100, "y": 250, "ip": "192.168.1.4"}
        }

        # Definición de enlaces entre dispositivos
        self.links = {
            ("switch", "router1"): {"state": "up", "label": None},
            ("switch", "router2"): {"state": "up", "label": None},
            ("switch", "router3"): {"state": "up", "label": None},
            ("switch", "router4"): {"state": "up", "label": None}
        }

        # Creación del lienzo de la red
        self.canvas = tk.Canvas(root, width=500, height=300, bg="yellow")
        self.canvas.pack()

        # Dibujo de la red en el lienzo
        self.draw_network()

        font = ("Times New Roman", 12)

        # Creación de botones para conectar y desconectar routers
        self.connect_buttons = {}
        self.disconnect_buttons = {}

        for router in self.devices.keys():
            self.connect_buttons[router] = tk.Button(root, text=f"Conectar {router}", command=lambda router=router: self.connect_router(router))
            self.connect_buttons[router].pack(side="left", padx=5)
            self.connect_buttons[router].configure(font=font)

            self.disconnect_buttons[router] = tk.Button(root, text=f"Desconectar {router}", command=lambda router=router: self.disconnect_router(router))
            self.disconnect_buttons[router].pack(side="left", padx=5)
            self.disconnect_buttons[router].configure(font=font)

        self.connect_buttons["switch"].configure(command=self.connect_all_routers)

        self.disconnect_buttons["switch"].configure(command=self.disconnect_all_routers)

    def draw_network(self):
        # Dibuja los dispositivos y enlaces en el lienzo
        font = ("Times New Roman", 12)

        for device, pos in self.devices.items():
            self.canvas.create_rectangle(pos["x"] - 50, pos["y"] - 20, pos["x"] + 50, pos["y"] + 20, fill="gray")
            self.canvas.create_text(pos["x"], pos["y"], text=device, font=font)
            if "ip" in pos:
                self.canvas.create_text(pos["x"], pos["y"] + 15, text="IP: " + pos["ip"], font=font)

        for link, link_info in self.links.items():
            if link_info["state"] == "up":
                text = "Connect"
                color = "green"
            else:
                text = "Disconnect"
                color = "red"
            link_info["label"] = self.canvas.create_text((self.devices[link[0]]["x"] + self.devices[link[1]]["x"]) / 2,
                                                         (self.devices[link[0]]["y"] + self.devices[link[1]]["y"]) / 2,
                                                         text=text, fill=color, font=font)

    def disconnect_router(self, router):
        # Desconecta el router especificado y actualiza el lienzo
        font = ("Times New Roman", 12)

        for link, link_info in self.links.items():
            if link[1] == router:
                link_info["state"] = "down"
                self.canvas.itemconfig(link_info["label"], text="Disconnect", fill="red", font=font)

    def connect_router(self, router):
        # Conecta el router especificado y actualiza el lienzo
        font = ("Times New Roman", 12)

        for link, link_info in self.links.items():
            if link[1] == router:
                link_info["state"] = "up"
                self.canvas.itemconfig(link_info["label"], text="Connect", fill="green", font=font)

    def disconnect_all_routers(self):
        # Desconecta todos los routers y muestra un mensaje de aviso
        tkinter.messagebox.showinfo("AVISO","No hay conexión con la red principal")

        font = ("Times New Roman", 12)

        for router in self.devices.keys():
            if router != "switch":
                for link, link_info in self.links.items():
                    if link[1] == router:
                        link_info["state"] = "down"
                        self.canvas.itemconfig(link_info["label"], text="Disconnect", fill="red", font=font)

    def connect_all_routers(self):
        # Conecta todos los routers y muestra un mensaje de aviso
        tkinter.messagebox.showinfo("AVISO", "Se restableció la conexión con la red principal")

        font = ("Times New Roman", 12)

        for router in self.devices.keys():
            if router != "switch":
                for link, link_info in self.links.items():
                    if link[1] == router:
                        link_info["state"] = "up"
                        self.canvas.itemconfig(link_info["label"], text="Connect", fill="green", font=font)

def main():
    root = tk.Tk()
    app = NetworkSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

