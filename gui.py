import tkinter as tk
from tkinter import ttk
import seaborn as sns

windowWidth = 1200
windowHeight = 800
graphFrameHeight = 800
graphFrameWidth = 800
tabFrameWidth = 400
tabFrameHeight=800

app = tk.Tk()
app.title("Warhammer dice roller")

class Frame:
    def __init__(self):
        self.myFrame = tk.Frame()


profileWindowTabControl = ttk.Notebook(app)
attackerTab = tk.Frame(profileWindowTabControl)
balisticSkillLabel = tk.Label(attackerTab, text="Balistic skill:")
balisticSkillLabel.grid(row=0, column=0)
balisticSkillEntry = tk.Entry(attackerTab)
balisticSkillEntry.grid(row=0,column=1)
reRollLabel = tk.Label(attackerTab, text="Re roll:")
reRollLabel.grid(row=1,column=0)
reRollCombo = ttk.Combobox(attackerTab, values=['ones', 'hits', 'failed hits'])
reRollCombo.grid(row=1,column=1)
hitModifierLabel = tk.Label(attackerTab, text="Hit modifier:")
hitModifierLabel.grid(row=2,column=0)
hitModifierEntry = tk.Entry(attackerTab)
hitModifierEntry.grid(row=2,column=1)
attackerTab.pack()
defenderTab = tk.Frame(profileWindowTabControl)
profileWindowTabControl.add(attackerTab, text="Attacker")
profileWindowTabControl.add(defenderTab, text="Defender")

resultWindowTabControl = ttk.Notebook(app)
deadModelsGraphTab = tk.Frame(resultWindowTabControl)
damageReceivedGraphTab = tk.Frame(resultWindowTabControl)
statisticsTab = tk.Frame(resultWindowTabControl)
resultWindowTabControl.add(deadModelsGraphTab, text="Lost models")
resultWindowTabControl.add(damageReceivedGraphTab, text="Damage done")
resultWindowTabControl.add(statisticsTab, text="Statistics")

profileWindowTabControl.pack()
resultWindowTabControl.pack()

app.mainloop()