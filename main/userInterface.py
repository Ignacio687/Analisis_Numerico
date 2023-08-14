import tkinter as tk
from tkinter import ttk
from . import LeastSquaresApproximator

class UserInterface():
    def __init__(self):
        self.calculator = LeastSquaresApproximator()
        self.instance = 0
        self.labels = ["Ingrese la funcion a aproximar", "Ingrese el limite inferior del intervalo", "Ingrese el limite superior del intervalo", "Ingrese la funcion peso", 
                       "Ingrese las bases una a una, o deje el espacio en blanco para\n usar la base predeterminada, al terminar presione 'cont'", "Presione '=', luego de ver los resultados presione 'reset'"]
        self.data = []

    def on_button_click(self, button_text, entry, message_label):
        if button_text in ("=", "cont") :
            try:
                if self.instance > len(self.labels)-2:
                    finalData = self.calculator.evaluate(self.data[0], self.data[1], self.data[2], self.data[4], self.data[3])
                    entry.delete(0, tk.END)
                    entry.insert(tk.END, f"f*: {finalData[0]} Err: {finalData[1]}")
                else:
                    inputStr = entry.get()
                    if self.instance == 4 and len(self.data) < 5:
                        self.data.append([inputStr])
                    elif self.instance == 4:
                        self.data[self.instance].append(inputStr)
                    else: self.data.append(inputStr)
                    if self.instance != 4 or button_text == "cont":
                        self.instance += 1
                        message_label.config(text=self.labels[self.instance])
                    entry.delete(0, tk.END)
            except ValueError as e:
                entry.delete(0, tk.END)
                entry.insert(tk.END, e.args[0])
                self.reset(entry, message_label)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "revisar los datos ingresados")
                self.reset(entry, message_label)
        elif button_text == "C":
            entry.delete(0, tk.END)
        elif button_text == "reset":
            self.reset(entry, message_label)
        else:
            entry.insert(tk.END, button_text)

    def reset(self, entry, message_label):
        self.instance = 0
        message_label.config(text=self.labels[self.instance])
        self.data = []
        entry.delete(0, tk.END)

    def add_buttons(self, parent, buttons, entry, message_label, button_width):
        row = 5
        col = 0
        for label in buttons:
            button = ttk.Button(parent, text=label, width=button_width, command=lambda label=label: self.on_button_click(label, entry, message_label))
            button.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def run(self):
        # Create the main window
        root = tk.Tk()
        root.title("Aproximador por mínimos cuadrados")
        # Create a label for the message
        message_label = ttk.Label(root, text="Ingrese la funcion a aproximar", font=("Helvetica", 20, "bold"))
        message_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        # Create an entry widget for input
        entry = ttk.Entry(root, font=("Helvetica", 16))
        entry.grid(row=1, column=0, columnspan=4, rowspan=4, padx= 10, pady= 10, sticky="wese")
        # Define button labels
        button_labels = [
            "sin", "cos", "tan","/",
            "exp", "ln", "pi","*",
            "7", "8", "9", "-",
            "4", "5", "6", "+",
            "1", "2", "3", "C",
            "0", ".", "x", "=",
            "(", ")", "cont","reset"
        ]
        # Create and place buttons
        button_width = 20
        self.add_buttons(root, button_labels, entry, message_label, button_width)
        # Run the GUI event loop
        root.mainloop()
        
if __name__ == "__main__":
    app = UserInterface()
    app.run()