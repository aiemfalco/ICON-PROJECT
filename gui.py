from dataset import create_dataset
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def update_graph():

    updated_data = create_dataset()

    plt.clf()

    plt.plot(updated_data)

    canvas.draw()

def generate_pie_chart(team_name, win_percentage, draw_percentage, lose_percentage, root):
    labels = ['Vittoria', 'Pareggio', 'Sconfitta']
    sizes = [win_percentage, draw_percentage, lose_percentage]
    colors = ['#ff9999','#66b3ff','#99ff99']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')  
    ax.set_title(f"Percentuali di risultati per {team_name}")

    # Creare un oggetto FigureCanvasTkAgg per Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Creazione della finestra principale
root = tk.Tk()
root.title("Previsione del Match")

# Creazione di un canvas per il grafico
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

'''
Etichetta per il valore
value_label = tk.Label(root, text="Valore da visualizzare:")
value_label.pack() 
'''

'''
Simuliamo i dati delle due squadre
team1_name = "Squadra A"
team1_win_percentage = 30
team1_draw_percentage = 40
team1_lose_percentage = 30

team2_name = "Squadra B"
team2_win_percentage = 40
team2_draw_percentage = 30
team2_lose_percentage = 30
'''

'''
Genera i grafici a torta per le due squadre
generate_pie_chart(team1_name, team1_win_percentage, team1_draw_percentage, team1_lose_percentage, root)
generate_pie_chart(team2_name, team2_win_percentage, team2_draw_percentage, team2_lose_percentage, root)
'''

# Avvio del loop principale dell'interfaccia grafica
root.mainloop()
