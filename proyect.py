import tkinter as tk
import tkinter.messagebox


class NetworkSimulator:
    def __init__(self, root):
        # Inicialización de la ventana principal de la aplicación
        self.root = root
        self.root.title("Simulador de Red")

        # Definición de dispositivos y sus posiciones
        canvas_width = 800
        canvas_height = 400
        self.devices = {
            "switch": {"x": canvas_width // 2, "y": canvas_height // 2},
            "router1": {"x": canvas_width // 4, "y": canvas_height // 2},
            "router2": {"x": canvas_width // 2, "y": canvas_height // 4},
            "router3": {"x": 3 * canvas_width // 4, "y": canvas_height // 2},
            "router4": {"x": canvas_width // 4, "y": 3 * canvas_height // 4},
            "pc1": {"x": 50, "y": 150, "ip": "192.168.1.1"},
            "pc2": {"x": 250, "y": 50, "ip": "192.168.1.2"},
            "pc3": {"x": 750, "y": 250, "ip": "192.168.1.3"},
            "pc4": {"x": 50, "y": 250, "ip": "192.168.1.4"}
        }

        # Definición de enlaces entre dispositivos
        self.links = {
            ("switch", "router1"): {"state": "up", "label": None},
            ("switch", "router2"): {"state": "up", "label": None},
            ("switch", "router3"): {"state": "up", "label": None},
            ("switch", "router4"): {"state": "up", "label": None},
            ("router1", "pc1"): {"state": "up", "label": None},
            ("router2", "pc2"): {"state": "up", "label": None},
            ("router3", "pc3"): {"state": "up", "label": None},
            ("router4", "pc4"): {"state": "up", "label": None}
        }

        # Creación del lienzo de la red con un tamaño mayor
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="yellow")
        self.canvas.pack()

        # Dibujo de la red en el lienzo
        self.draw_network()

        font = ("Times New Roman", 12)

        # Creación de botones para conectar y desconectar routers
        self.connect_buttons = {}
        self.disconnect_buttons = {}

        for router in self.devices.keys():
            self.connect_buttons[router] = tk.Button(root, text=f"C. {router.replace('router', 'RT.')}",
                                                     command=lambda router=router: self.connect_router(router))
            self.connect_buttons[router].pack(side="left", padx=5)
            self.connect_buttons[router].configure(font=font)

            self.disconnect_buttons[router] = tk.Button(root, text=f"D. {router.replace('router', 'RT.')}",
                                                        command=lambda router=router: self.disconnect_router(router))
            self.disconnect_buttons[router].pack(side="left", padx=5)
            self.disconnect_buttons[router].configure(font=font)

        self.connect_buttons["switch"].configure(command=self.connect_all_routers)
        self.disconnect_buttons["switch"].configure(command=self.disconnect_all_routers)

    def draw_network(self):
        # Dibuja los dispositivos y enlaces en el lienzo
        font = ("Times New Roman", 12)

        for device, pos in self.devices.items():
            width_adjustment = 30 if device.startswith("router") else 50
            self.canvas.create_rectangle(pos["x"] - width_adjustment, pos["y"] - 20, pos["x"] + width_adjustment,
                                         pos["y"] + 20, fill="gray")
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
        # Desconecta el router especificado y su PC correspondiente si está conectada, actualizando el lienzo
        font = ("Times New Roman", 12)

        for link, link_info in self.links.items():
            if link[1] == router:
                link_info["state"] = "down"
                self.canvas.itemconfig(link_info["label"], text="Disconnect", fill="red", font=font)

                # Desconectar la PC asociada al router
                pc_device = "pc" + router[-1]  # Obtener el nombre de la PC correspondiente al router
                pc_link = (router, pc_device)
                if pc_link in self.links:
                    self.links[pc_link]["state"] = "down"
                    self.canvas.itemconfig(self.links[pc_link]["label"], text="Disconnect", fill="red", font=font)

    def connect_router(self, router):
        # Conecta el router especificado y su PC correspondiente si está desconectada, actualizando el lienzo
        font = ("Times New Roman", 12)

        for link, link_info in self.links.items():
            if link[1] == router:
                link_info["state"] = "up"
                self.canvas.itemconfig(link_info["label"], text="Connect", fill="green", font=font)

                # Conectar la PC asociada al router si está desconectada
                pc_device = "pc" + router[-1]  # Obtener el nombre de la PC correspondiente al router
                pc_link = (router, pc_device)
                if pc_link in self.links and self.links[pc_link]["state"] == "down":
                    self.links[pc_link]["state"] = "up"
                    self.canvas.itemconfig(self.links[pc_link]["label"], text="Connect", fill="green", font=font)

    def disconnect_all_routers(self):
        # Desconecta todos los routers y muestra un mensaje de aviso
        tkinter.messagebox.showinfo("AVISO", "No hay conexión con la red principal")

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

    def connect_pc1_to_router1(self):
        # Conecta PC1 a Router1 y actualiza el lienzo
        font = ("Times New Roman", 12)

        self.links[("router1", "pc1")]["state"] = "up"
        self.canvas.itemconfig(self.links[("router1", "pc1")]["label"], text="Connect", fill="green", font=font)

    def disconnect_pc1_from_router1(self):
        # Desconecta PC1 de Router1 y actualiza el lienzo
        font = ("Times New Roman", 12)

        self.links[("router1", "pc1")]["state"] = "down"
        self.canvas.itemconfig(self.links[("router1", "pc1")]["label"], text="Disconnect", fill="red", font=font)


def main():
    root = tk.Tk()
    app = NetworkSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()