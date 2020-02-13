import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
windowWidth = 1200
windowHeight = 800
graphFrameHeight = 800
graphFrameWidth = 800
tabFrameWidth = 400
tabFrameHeight=800

app = tk.Tk()
app.title("Warhammer dice roller")

class Tab:
    def __init__(self, parentObject):
        self.myFrame = tk.Frame(parentObject)
        self.addedObjects = []

    def addTabObject(self, objectType, rowPosition, columnPosition,objectText='', someValues=[]):
        if objectType == 'label':
            labelObject =  tk.Label(self.myFrame, text=objectText)
            labelObject.grid(row=rowPosition, column=columnPosition)
            self.addedObjects.append(labelObject)
        elif objectType == 'entry':
            entryObject = tk.Entry(self.myFrame)
            entryObject.grid(row=rowPosition, column=columnPosition)
            self.addedObjects.append(entryObject)
        elif objectType == 'combo':
            comboObject = ttk.Combobox(self.myFrame, values=someValues)
            comboObject.grid(row=rowPosition, column=columnPosition)
            self.addedObjects.append(comboObject)
        else:
            raise Exception("Invalid tab object added")

    def pack(self):
        self.myFrame.pack()

    def getWidget(self, row, column):
        return self.myFrame.grid_slaves(row, column)


profileWindowTabControl = ttk.Notebook(app)
attackerTab = Tab(profileWindowTabControl)
possibleDiceModifiers = [-3,-2,-1,0,1,2,3]
row = 0
attackerTab.addTabObject('label', row, 0, 'Number of Shots:')
attackerTab.addTabObject('entry', row, 1)
row += 1
attackerTab.addTabObject('label', row, 0, 'Balistic Skill:')
attackerTab.addTabObject('combo', row, 1, '', [2, 3, 4, 5, 6])
row += 1
attackerTab.addTabObject('label', row, 0, 'Hit Re Roll:')
attackerTab.addTabObject('combo', row, 1, '', ['ones', 'hits', 'failed hits'])
row += 1
attackerTab.addTabObject('label', row, 0, 'Hit Modifiers:')
attackerTab.addTabObject('combo', row, 1, '', possibleDiceModifiers)
row += 1
attackerTab.addTabObject('label', row,0,'Weapon Strength:')
attackerTab.addTabObject('entry', row, 1)
row += 1
attackerTab.addTabObject('label', row, 0, 'Wound modifiers:')
attackerTab.addTabObject('combo', row, 1, '', possibleDiceModifiers)
row += 1
attackerTab.addTabObject('label', row, 0, 'Wound Re Roll:')
attackerTab.addTabObject('combo', row, 1, '', ['ones', 'hits', 'failed hits'])

defenderTab = Tab(profileWindowTabControl)
row = 0
defenderTab.addTabObject('label', row, 0, 'Toughness:')
defenderTab.addTabObject('entry', row, 1)
row += 1
defenderTab.addTabObject('label', row, 0, 'Wounds Characteristic:')
defenderTab.addTabObject('entry', row, 1)
row += 1
defenderTab.addTabObject('label', row, 0, 'Armour Save:')
defenderTab.addTabObject('combo', row, 1, '', [2,3,4,5,6,7])
row += 1
defenderTab.addTabObject('label', row, 0, 'Invunerable Save:')
defenderTab.addTabObject('combo', row, 1, '', [2,3,4,5,6,7])
row += 1
defenderTab.addTabObject('label', row, 0, 'Feel No Pain save:')
defenderTab.addTabObject('combo', row, 1, '', [2,3,4,5,6,7])
row += 1

profileWindowTabControl.add(attackerTab.myFrame, text="Attacker")
profileWindowTabControl.add(defenderTab.myFrame, text="Defender")

resultWindowTabControl = ttk.Notebook(app)
deadModelsGraphTab = tk.Frame(resultWindowTabControl)
damageReceivedGraphTab = tk.Frame(resultWindowTabControl)
statisticsTab = tk.Frame(resultWindowTabControl)
resultWindowTabControl.add(deadModelsGraphTab, text="Lost models")
resultWindowTabControl.add(damageReceivedGraphTab, text="Damage done")
resultWindowTabControl.add(statisticsTab, text="Statistics")

fig = Figure(figsize=(5,4), dpi=100)
data = [0,1,2,3,2,1,0]
fig.add_subplot(111).plot(data)

canvas = FigureCanvasTkAgg(fig, master=damageReceivedGraphTab)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, damageReceivedGraphTab)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

profileWindowTabControl.pack()
resultWindowTabControl.pack()

app.mainloop()