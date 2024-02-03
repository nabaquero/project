import tkinter as tk
import random

class NetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Red")

        self.devices = {
            "switch": {"x": 250, "y": 200},
            "router1": {"x": 100, "y": 150},
            "router2": {"x": 250, "y": 50},
            "router3": {"x": 400, "y": 150}
        }

        self.links = {
            ("switch", "router1"): {"state": "up", "label": None},
            ("switch", "router2"): {"state": "up", "label": None},
            ("switch", "router3"): {"state": "up", "label": None}
        }

        self.canvas = tk.Canvas(root, width=500, height=300, bg="yellow")  # Cambio de color de fondo a amarillo
        self.canvas.pack()

        self.draw_network()

        font = ("Times New Roman", 12)

        self.connect_buttons = {}

        for router in self.devices.keys():
            self.connect_buttons[router] = tk.Button(root, text=f"Conectar {router}", command=lambda router=router: self.connect_router(router))
            self.connect_buttons[router].pack(side="left", padx=5)
            self.connect_buttons[router].configure(font=font)

        self.disconnect_buttons = {}

        for router in self.devices.keys():
            self.disconnect_buttons[router] = tk.Button(root, text=f"Desconectar {router}", command=lambda router=router: self.disconnect_router(router))
            self.disconnect_buttons[router].pack(side="left", padx=5)
            self.disconnect_buttons[router].configure(font=font)

    def draw_network(self):
        font = ("Times New Roman", 12)

        for device, pos in self.devices.items():
            # Ajusta el tamaño del cuadro en 10 unidades a lo largo y ancho
            self.canvas.create_rectangle(pos["x"] - 25, pos["y"] - 25, pos["x"] + 25, pos["y"] + 25, fill="gray")
            self.canvas.create_text(pos["x"], pos["y"], text=device, font=font)

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
        font = ("Times New Roman", 12)

        for link, link_info in self.links.items():
            if link[1] == router:
                link_info["state"] = "down"
                self.canvas.itemconfig(link_info["label"], text="Disconnect", fill="red", font=font)

    def connect_router(self, router):
        font = ("Times New Roman", 12)

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
