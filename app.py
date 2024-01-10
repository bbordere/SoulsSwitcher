import psutil
import threading
import pygetwindow as pgw
import pyautogui
import time
import ctypes
import signal
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

#Represents a game process with its window name, executable name and psutil.Process instance
class Game:
	def __init__(self, windowName: str, execName: str, proc: psutil.Process):
		self.windowName = windowName
		self.execName = execName
		self.proc = proc

	def __str__(self) -> str:
		return f"Game(windowName={self.windowName}, execName={self.execName}, proc={self.proc})"
	
	def __repr__(self) -> str:
		return str(self)


class App:
	def __init__(self):
		self.thread = None
		self.games = dict()
		self.execsName = ["DarkSoulsRemastered.exe", "DarkSoulsII.exe", "DarkSoulsIII.exe", "sekiro.exe", "eldenring.exe"]
		self.windowsName = ["DARK SOULS™: REMASTERED", "DARK SOULS II", "DARK SOULS III", "Sekiro", "ELDEN RING™"]
		self.isAlive = True
		self.gamesList = []
		self.spinboxes = dict()
		self.initEvents()
		self.initWindow()
		self.initVars()
		self.initFrames()
		self.initLabels()
		self.initCheckboxes()
		self.initPauseButton()
		self.initStatus()
		self.initCurrentGameStatus()
		self.initTimeRange()
		self.initCustomLoopNumber()
		for checkbox in self.checkBoxes:
			self.checkBoxes[checkbox].pack(pady=5, padx=10, anchor="w")
		self.panedWindow.add(self.frames["left"])
		self.panedWindow.add(self.frames["right"])
		self.checkBoxes["infiniteLoop"] = ttk.Checkbutton(self.frames["right"], text="Infinite Loop", variable=self.vars["infiniteLoop"],
															command=self.toggle_spinbox_visibility)
		self.checkBoxes["infiniteLoop"].pack(pady=10)
		self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

	def initEvents(self):
		self.events = dict()
		self.events["badProc"] = threading.Event()
		self.events["badProc"].clear()
		self.events["changeTitle"] = threading.Event()
		self.events["changeTitle"].clear()
		self.events["badPermissions"] = threading.Event()
		self.events["badPermissions"].clear()
		self.events["endLoop"] = threading.Event()
		self.events["endLoop"].clear()

	def initWindow(self):
		self.window = tk.Tk()
		self.window.iconbitmap("icon.ico")
		self.window.resizable(width=False, height=False)
		self.window.title("Souls Switcher")
		self.window.geometry("500x350")
		self.window['bg'] = 'grey'
		self.panedWindow = ttk.Panedwindow(self.window, orient=tk.HORIZONTAL)
		self.panedWindow.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=2, padx=2)

	def initFrames(self):
		self.frames = dict()
		self.frames["left"] = tk.Frame(self.panedWindow, borderwidth=2,
										relief=tk.GROOVE)
		self.frames["right"] = tk.Frame(self.panedWindow, borderwidth=2,
										relief=tk.GROOVE)
		self.frames["status"] = tk.Frame(self.frames["right"], width=105,
										height=40, borderwidth=0, relief=tk.GROOVE)
		self.frames["customLoop"] = tk.Frame(self.frames["right"], borderwidth=0,
										relief=tk.GROOVE)
		ttk.Label(self.frames["left"],
					text="Game Selected",
					font=('Helvetica', 14, 'bold')).pack(padx=10, pady=10)
		ttk.Label(self.frames["right"],
					text="Options",
					font=('Helvetica', 14, 'bold')).pack(padx=10, pady=10)

	def initVars(self):
		self.vars = dict()
		self.vars["status"] = tk.StringVar()
		self.vars["minTimeVal"] = tk.IntVar()
		self.vars["maxTimeVal"] = tk.IntVar()
		self.vars["loopNumber"] = tk.IntVar()
		self.vars["currentGame"] = tk.StringVar()
		self.vars["DS1_var"] = tk.BooleanVar()
		self.vars["DS2_var"] = tk.BooleanVar()
		self.vars["DS3_var"] = tk.BooleanVar()
		self.vars["Sekiro_var"] = tk.BooleanVar()
		self.vars["ER_var"] = tk.BooleanVar()
		self.vars["infiniteLoop"] = tk.BooleanVar()
		self.vars["infiniteLoop"].set(True)

	def initLabels(self):
		self.labels = dict()
		self.labels["status"] = tk.Label(self.frames["status"],
										textvariable=self.vars["status"],
										font=('Helvetica', 10), fg='red')
	def initCheckboxes(self):
		self.checkBoxes = dict()
		self.checkBoxes["dS1Checkbox"] = ttk.Checkbutton(self.frames["left"],
										text="Dark Souls 1", variable=self.vars["DS1_var"], command=lambda: self.addGame("DarkSoulsRemastered.exe", "DS1_var"))
		self.checkBoxes["dS2Checkbox"] = ttk.Checkbutton(self.frames["left"],
										text="Dark Souls 2", variable=self.vars["DS2_var"], command=lambda: self.addGame("DarkSoulsII.exe", "DS2_var"))
		self.checkBoxes["dS3Checkbox"] = ttk.Checkbutton(self.frames["left"],
										text="Dark Souls 3", variable=self.vars["DS3_var"],command=lambda: self.addGame("DarkSoulsIII.exe", "DS3_var"))
		self.checkBoxes["sekiroCheckbox"] = ttk.Checkbutton(self.frames["left"],
										text="Sekiro", variable=self.vars["Sekiro_var"], command=lambda: self.addGame("sekiro.exe", "Sekiro_var"))
		self.checkBoxes["ERCheckbox"] = ttk.Checkbutton(self.frames["left"],
										text="Elden Ring", variable=self.vars["ER_var"], command=lambda: self.addGame("eldenring.exe", "ER_var"))
		
	def initStatus(self):
		self.vars["status"].set("Stopped")
		ttk.Label(self.frames["status"], text="Status:", font=('Helvetica', 10)).pack(pady=5, side=tk.LEFT)
		self.labels["status"].pack(pady=5, side=tk.RIGHT)
		self.frames["status"].pack(pady=10)
		self.frames["status"].pack_propagate(0)

	def initCurrentGameStatus(self):
		self.vars["currentGame"].set("Undefined")
		currentGameFrame = tk.Frame(self.frames["right"], width=200, height=40, borderwidth=0, relief=tk.GROOVE)
		tk.Label(currentGameFrame, text="Current Game:", font=('Helvetica', 10)).pack(pady=5, side=tk.LEFT)
		currentGameLabel = tk.Label(currentGameFrame, textvariable=self.vars["currentGame"], font=('Helvetica', 10), fg='blue')
		currentGameLabel.pack(pady=5, side=tk.RIGHT)
		currentGameFrame.pack(pady=10)

	def initTimeRange(self):
		timeRangeFrame = tk.Frame(self.frames["right"], borderwidth=0, relief=tk.GROOVE)
		tk.Label(timeRangeFrame, text="Time Range", font=('Helvetica', 10)).pack(side=tk.LEFT)
		timeRangeFrame.pack(pady=10)
		self.vars["minTimeVal"].set(15)
		self.vars["maxTimeVal"].set(30)
		self.spinboxes["minTime"] = ttk.Spinbox(timeRangeFrame,  from_=2, to=599, width=5, textvariable=self.vars["minTimeVal"])
		self.spinboxes["minTime"].pack(padx=10, pady=5, side=tk.LEFT)
		self.spinboxes["maxTime"] = ttk.Spinbox(timeRangeFrame, from_=3, to=600, width=5, textvariable=self.vars["maxTimeVal"])
		self.spinboxes["maxTime"].pack(padx=10, pady=5, side=tk.LEFT)

	def initCustomLoopNumber(self):
		self.vars["loopNumber"].set(10)
		ttk.Label(self.frames["customLoop"], text="Number of loop:", font=('Helvetica', 10)).pack(side=tk.LEFT)
		self.spinboxes["loopNumber"] = ttk.Spinbox(self.frames["customLoop"], from_=1, to=100, width=5, textvariable=self.vars["loopNumber"])
		self.spinboxes["loopNumber"].pack(padx=10, pady=10)

	def pauseButtonHandling(self):
		global isRunning
		self.pauseButton["text"] = "Stop" if (not isRunning) else "Start"
		self.vars["status"].set("Stopped") if (isRunning) else self.vars["status"].set("Started")
		self.labels["status"]["fg"] = 'red' if (isRunning) else 'green'
		for checkbox in self.checkBoxes:
			self.checkBoxes[checkbox].config(state=tk.DISABLED) if self.vars["status"].get() == "Started" else self.checkBoxes[checkbox].config(state=tk.NORMAL)
		for spinbox in self.spinboxes:
			self.spinboxes[spinbox].config(state=tk.DISABLED) if self.vars["status"].get() == "Started" else self.spinboxes[spinbox].config(state=tk.NORMAL)
		isRunning = True if self.vars["status"].get() == "Started" else False
		if (isRunning):
			self.startThread()

	def toggle_spinbox_visibility(self):
		if self.vars["infiniteLoop"].get():
			self.frames["customLoop"].pack_forget()
		else:
			self.frames["customLoop"].pack()

	def initPauseButton(self):
		style = ttk.Style()
		style.configure('TButton', font=('Helvetica', 16))
		self.pauseButton = ttk.Button(self.frames["right"], text="Start")
		self.pauseButton["command"] = self.pauseButtonHandling
		self.pauseButton.pack(side=tk.TOP, pady=(0, 10))

	def addGame(self, game: str, varName: str):
		if (self.vars[varName].get()):
			self.gamesList.append(game)
		else:
			self.gamesList.pop(self.gamesList.index(game))

	def getVarValue(self, varName: str):
		return (self.vars[varName].get())
# 
	def run(self):
		while (self.isAlive):
			if len(self.gamesList) < 2:
				self.pauseButton.config(state=tk.DISABLED)
			else:
				self.pauseButton.config(state=tk.NORMAL)

			if self.events["badPermissions"].is_set():
				self.pauseButtonHandling()
				self.events["badPermissions"].clear()
				messagebox.showerror(title = "Error",message = "Please run script as administrator")

			if self.events["badProc"].is_set():
				self.pauseButtonHandling()
				self.events["badProc"].clear()
				messagebox.showerror(title = "Error",message = "Please check if the selected games are launched")

			if self.events["changeTitle"].is_set():
				try:
					self.vars["currentGame"].set(pyautogui.getActiveWindow().title)
				except:
					self.vars["currentGame"] = "Undefined"
				self.events["changeTitle"].clear()
	
			if self.events["endLoop"].is_set():
				self.pauseButtonHandling()
				self.events["endLoop"].clear()

			self.window.update()
			time.sleep(0.03)

	def onClosing(self):
		global isRunning
		isRunning = False
		self.window.destroy()
		self.isAlive = False

	# Start a thread wich execute the switcher logic
	def startThread(self):
		global isRunning
		isRunning = True
		self.thread = threading.Thread(target=switcherLogic, args=[self,
														self.vars["infiniteLoop"].get(),
														self.vars["loopNumber"].get(),
														(self.vars["minTimeVal"].get(), self.vars["maxTimeVal"].get())])
		self.thread.start()

	def chooseGame(self, lastGame: str) -> str:
		choice = random.choice(self.gamesList)
		while (choice == lastGame):
			choice = random.choice(self.gamesList)
		return (choice)

	# Exec the shortcut WIN + {NUM} where num is the position of the game inside the taskbar
	def pressKeys(self, index: int) -> None:
		ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
		time.sleep(.2)
		ctypes.windll.user32.keybd_event(0x31 + index, 0, 0, 0)
		time.sleep(.2)
		ctypes.windll.user32.keybd_event(0x31 + index, 0, 2, 0)
		time.sleep(.2)
		ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)

# Wrapper for more convenient way to handle all process
def handlingProcess(mode: str, games: dict, app: App, isCritical: bool = True) -> None:
	for game in games:
		try:
			games[game].proc.resume() if mode == "resume" else games[game].proc.suspend()
		except:
			app.events["badPermissions"].set()
			if (isCritical):
				return

def switcherLogic(app: App, isInfiniteLoop: bool, loopCounter: int, timeRange: tuple) -> None:
	global isRunning
	lastGame = ""
	app.games = dict()
	# Get infos of selected process
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] in app.gamesList:
			index = app.execsName.index(proc.info['name'])
			if app.windowsName[index] not in app.games:
				if pgw.getWindowsWithTitle(app.windowsName[index]):
					app.games[app.windowsName[index]] = Game(app.windowsName[index], proc.info['name'], proc)
	
	# Securities for correct process handling
	if (app.games):
		games = [game.execName for game in app.games.values()]
	if not len(app.games) or len(app.gamesList) != len(app.games):
		app.events["badProc"].set()
		return
	if (games != app.gamesList):
		app.events["badProc"].set()
		return

	# Suspend all processes
	handlingProcess("suspend", app.games, app)

	loop = 0
	lastExec = ""
	while isRunning and (isInfiniteLoop or loop < loopCounter):
		if (not isInfiniteLoop):
			loop += 1
		try:
			# Choose a random game from the selection
			exec = app.chooseGame(lastExec)
			gamechoice =  app.windowsName[app.execsName.index(exec)]

			# Resume the chosen game process
			app.games[gamechoice].proc.resume()

			# Suspend the last game process
			if len(lastGame):
				app.games[lastGame].proc.suspend()
		
			# Execute shortcut while the current window isn't the chose game
			while (pyautogui.getActiveWindow().title != gamechoice):
				app.pressKeys(app.windowsName.index(gamechoice))
				time.sleep(.05)

			app.events["changeTitle"].set()
			lastGame = gamechoice
			lastExec = exec

			# Sleep for a random time to play
			if timeRange[0] > timeRange[1]:
				time.sleep(random.randint(timeRange[1], timeRange[0]))
			elif timeRange[0] == timeRange[1]:
				time.sleep(random.randint(timeRange[0], timeRange[1] + 1))
			else:
				time.sleep(random.randint(timeRange[0], timeRange[1]))
				
		except:
			break
			

	# At the end resume all processes
	handlingProcess("resume", app.games, app, False)
	if (loop >= loopCounter):
		app.events["endLoop"].set()
		return
	isRunning = False

# CTRL-C Handler
def handler(app: App) -> None:
	for w in app.windowsName:
		try:
			app.games[w].proc.resume()
		except:
			pass
	exit(1)

isRunning = False

if __name__ == "__main__":
	app = App()
	signal.signal(signal.SIGINT, lambda x, y: handler(app))
	app.run()
	if (app.thread):
		app.thread.join()