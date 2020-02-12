import tkinter as tk
import seaborn as sns

root = tk.Tk()
frameWidth = 300
frameHeight = 500
label = tk.Label(root, text="label")
label.pack()

hitterFrame = tk.Frame(root,width=frameWidth, height=frameHeight)
bsEntry = tk.Entry(hitterFrame).pack()
hitModifierEntry = tk.Entry(hitterFrame).pack()
reRollEntry = tk.Entry(hitterFrame).pack()
numHitsEntry = tk.Entry(hitterFrame).pack()
hitterFrame.pack()
wounderFrame = tk.Frame(root, width=frameWidth, height=frameHeight)

root.mainloop()