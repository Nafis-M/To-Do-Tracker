import customtkinter as tk
import platform
import datetime
import roughDraft
from PIL import Image

'''Check date and return if date is valid'''
def dateChecker(date):
    try:
        datetime.datetime.strptime(date, '%m/%d/%y')
        return True
    except ValueError:
        return False

'''When clicked on the Task, popup more information about task'''
class viewTask(tk.CTkToplevel):
    def __init__(self, itemID="", dataObj=tk, mainObj = tk,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry("400x300")
        # self.resizable(False,False)
        self.allData = roughDraft.getValue(itemID)
        self.title("Data")
        self.itemID = itemID
        self.dataObj = dataObj
        self.mainObj = mainObj

        #form Frame
        self.formFrameTop = tk.CTkFrame(self)
        self.formFrameTop.pack(padx=10, pady=10)
        self.formFrameBottom = tk.CTkFrame(self)
        self.formFrameBottom.pack(padx=10,pady=10)
        self.buttonFrame = tk.CTkFrame(self)
        self.buttonFrame.pack(padx=10, pady=10)

        # Title
        self.userTitleLabel = tk.CTkLabel(self.formFrameTop, text="Title")
        self.userTitleLabel.grid(row=0, column=0)
        self.userTitleTextBox = tk.CTkTextbox(self.formFrameTop, height=80)
        self.userTitleTextBox.configure(wrap="word")
        self.userTitleTextBox.grid(row=0, column=1, padx=10, pady=10)
        self.userTitleTextBox.insert("0.0", self.allData[0])
        self.userTitleTextBox.configure(state="disabled")

        # Description
        self.descriptionLabel = tk.CTkLabel(self.formFrameTop, text="Description")
        self.descriptionLabel.grid(row=1, column=0, padx=10)
        self.descriptionTextBox = tk.CTkTextbox(self.formFrameTop, height=150)
        self.descriptionTextBox.configure(wrap="word")
        self.descriptionTextBox.grid(row=1, column=1, padx=10, pady=10)
        self.descriptionTextBox.insert("0.0", self.allData[1])
        self.descriptionTextBox.configure(state="disabled")

        # Priority
        self.priorityLabel = tk.CTkLabel(self.formFrameBottom, text="Select Priority")
        self.priorityLabel.grid(row=0,column=0,padx=2)
        self.priorityEntry = tk.CTkEntry(self.formFrameBottom)
        self.priorityEntry.insert(0, self.allData[3])
        self.priorityEntry.configure(state="disabled")
        self.priorityEntry.grid(row=0, column=1,padx=10,pady=10)

        # Date
        self.dateLabel = tk.CTkLabel(self.formFrameBottom, text="Date")
        self.dateLabel.grid(row=1,column=0)
        self.dateEntry = tk.CTkEntry(self.formFrameBottom, placeholder_text=datetime.date.today().strftime("%m/%d/%y"))
        self.dateEntry.insert(0, self.allData[2])
        self.dateEntry.configure(state="disabled")
        self.dateEntry.grid(row=1,column=1,padx=10, pady=10)

        # Button
        self.leftButton = tk.CTkButton(self.buttonFrame, text="Previous Phase", command=self.moveLeft)
        self.rightButton = tk.CTkButton(self.buttonFrame, text="Next Phase", command=self.moveRight)
        self.deleteButton = tk.CTkButton(self.buttonFrame, text="Delete", command=self.deleteData)
        self.editButton = tk.CTkButton(self.buttonFrame, text="Edit", command=self.editData)
        self.saveButton = tk.CTkButton(self.buttonFrame, text="Save", command=self.saveData)
        self.leftButton.grid(row = 0, column = 0,padx=10, pady=10)
        self.rightButton.grid(row = 0, column = 1, padx=10, pady=10)
        self.deleteButton.grid(row = 1, column = 0, padx=10, pady=10)
        self.editButton.grid(row = 1, column = 1, padx=10, pady=10)
    '''Get all user input and check it, if passed, save data and change it in the gui'''
    def saveData(self):
        #get data
        self.dataTitle = self.userTitleTextBox.get("1.0", "end-1c")
        self.dataDescription = self.descriptionTextBox.get("1.0","end-1c")
        self.dataPriority = self.priorityComboBox.get()
        self.dataDate = self.dateEntry.get()

        # Error Checking
        self.color = self.priorityLabel.cget("text_color")
        self.userTitleLabel.configure(text_color=self.color)
        self.descriptionLabel.configure(text_color=self.color)
        self.dateLabel.configure(text_color=self.color)
        self.failed = False
        if(len(self.dataTitle) == 0):
            self.userTitleLabel.configure(text_color="red")
            self.failed = True
        if(len(self.dataDescription) == 0):
            self.descriptionLabel.configure(text_color="red")
            self.failed = True
        if(not(len(self.dataDate) == 0) and not dateChecker(self.dataDate)):
            self.dateLabel.configure(text_color="red")
            self.failed = True
        if self.failed:
            return

        if(len(self.dataDate) == 0):
            self.dataDate = self.dateEntry.cget("placeholder_text")
        else:
            self.dataDate = datetime.datetime.strptime(self.dataDate, '%m/%d/%y').strftime("%m/%d/%y")
        # create Task Frame
        roughDraft.editValues(self.itemID, [self.dataTitle, self.dataDescription, self.dataDate, self.dataPriority, self.allData[4]])
        self.dataObj.textBox.configure(state="normal")
        self.dataObj.textBox.delete("0.0", "end")
        self.dataObj.textBox.insert("0.0", self.dataTitle)
        self.dataObj.textBox.configure(state="disabled")
        self.dataObj.leftLabel.configure(text=self.dataDate)
        self.dataObj.rightLabel.configure(text=self.dataPriority)
        if(self.dataPriority == "Low"):
            self.dataObj.rightLabel.configure(text_color=("green","light green"))
        if(self.dataPriority == "Medium"):
            self.dataObj.rightLabel.configure(text_color=("orange","orange"))
        if(self.dataPriority == "High"):
            self.dataObj.rightLabel.configure(text_color=("red","red"))
        # close popup
        # close popup
        self.destroy()

    '''Edit data in popup'''
    def editData(self):
        # make everything editable
        self.userTitleTextBox.configure(state="normal")
        self.descriptionTextBox.configure(state="normal")
        self.dateEntry.configure(state="normal")

        # replace priority with priority combobox
        self.priorityEntry.grid_remove()
        self.priorityComboBox = tk.CTkComboBox(self.formFrameBottom, values=["Low", "Medium", "High"], state="readonly")
        self.priorityComboBox.set(self.priorityEntry.get())
        self.priorityComboBox.grid(row=0, column=1,padx=10,pady=10)

        # remove button
        self.leftButton.grid_remove()
        self.rightButton.grid_remove()
        self.editButton.grid_remove()

        #add save button
        self.saveButton.grid(row = 1, column = 1, padx=10, pady=10)
    '''Move task frame to right'''
    def moveRight(self):
        if(self.allData[4] == 3):
            return
        if(self.allData[4] == 0):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=1, frameToPassTo=self.mainObj.progressFrame)
        elif(self.allData[4] == 1):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=2, frameToPassTo=self.mainObj.reviewFrame)
        elif(self.allData[4] == 2):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=3, frameToPassTo=self.mainObj.completedFrame)
        self.destroy()
    '''Move task frame to left'''
    def moveLeft(self):
        if(self.allData[4] == 0):
            return
        if(self.allData[4] == 1):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=0, frameToPassTo=self.mainObj.openFrame)
        elif(self.allData[4] == 2):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=1, frameToPassTo=self.mainObj.progressFrame)
        elif(self.allData[4] == 3):
            self.createTaskFrame(title=self.allData[0], description=self.allData[1], priority=self.allData[3], date=self.allData[2], position=2, frameToPassTo=self.mainObj.reviewFrame)
        self.destroy()

    '''Delete task frame and delete data in database'''
    def deleteData(self):
        roughDraft.deleter(self.itemID)
        self.dataObj.destroy()
        self.destroy()
    '''Create task frame'''
    def createTaskFrame(self, title="", description="", priority="", date="", frameToPassTo=tk, position = -1):
        self.temp = taskClass(frameToPassTo, title=title, description=description, priority=priority, date=date, position=position, mainObj=self.mainObj, addToDatabase=True)
        self.temp.grid(sticky="ew",padx=10,pady=5)
        frameToPassTo.columnconfigure(0,weight=1)
        roughDraft.deleter(self.itemID)
        self.dataObj.destroy()
        
'''Display/Create task on gui'''
class taskClass(tk.CTkFrame):
    def __init__(self, master, title = "", description="", priority="", date="", position = -1, mainObj = tk, addToDatabase = False, itemID = "", **kwargs):
        super().__init__(master, **kwargs)

        self.mainObj = mainObj
        self.addToDatabase = addToDatabase
        #self.configure(fg_color=("#333333", "#333333"), border_color=("#333333", "#3333333"))

        self.tempFont = tk.CTkFont(family="Calibri", size=18)
        self.textBox = tk.CTkTextbox(self, height=100,font=self.tempFont)
        self.textBox.grid(row = 0, column = 0, sticky="ew")
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # set text
        self.textBox.insert("0.0", title)
        self.textBox.configure(state="disabled",wrap="word")
        self.leftLabel = tk.CTkLabel(self, text=date,padx=10)
        self.leftLabel.grid(row = 1, column=0,sticky="w", padx=2,pady=2)
        self.rightLabel = tk.CTkLabel(self, text=priority,padx=10)
        self.rightLabel.grid(row = 1, column=0,sticky="e",padx=2,pady=2)

        if self.addToDatabase:
            self.itemID = roughDraft.storage(title, description, date, priority, position)
        else:
            self.itemID = itemID
        
        if(priority == "Low"):
            self.rightLabel.configure(text_color=("green","light green"))
        if(priority == "Medium"):
            self.rightLabel.configure(text_color=("orange","orange"))
        if(priority == "High"):
            self.rightLabel.configure(text_color=("red","red"))
        

        # Making it clickable
        self.bind("<Button-1>", self.leftClick)
        self.textBox.bind("<Button-1>", self.leftClick)
        self.leftLabel.bind("<Button-1>", self.leftClick)
        self.rightLabel.bind("<Button-1>", self.leftClick)
        '''When user click on task frame, create a popup'''
    def leftClick(self,event):
        self.popupData = viewTask(self.itemID, self, mainObj= self.mainObj)
        self.popupData.attributes('-topmost',True)
        self.popupData.grab_set()

'''Popup for user to input data'''
class ToplevelTaskForm(tk.CTkToplevel):
    def __init__(self, frame=tk, listData=[], mainObj = tk,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.geometry("400x300")
        # self.resizable(False,False)
        self.title("Bug Form")
        self.frame = frame
        self.listData = listData
        self.mainObj = mainObj

        #form Frame
        self.formFrameTop = tk.CTkFrame(self)
        self.formFrameTop.pack(padx=10, pady=10)
        self.formFrameBottom = tk.CTkFrame(self)
        self.formFrameBottom.pack(padx=10,pady=10)

        # Title
        self.userTitleLabel = tk.CTkLabel(self.formFrameTop, text="Title")
        self.userTitleLabel.grid(row=0, column=0,)
        self.userTitleTextBox = tk.CTkTextbox(self.formFrameTop, height=80)
        self.userTitleTextBox.configure(wrap="word")
        self.userTitleTextBox.grid(row=0, column=1, padx=10, pady=10)

        # Description
        self.descriptionLabel = tk.CTkLabel(self.formFrameTop, text="Description")
        self.descriptionLabel.grid(row=1, column=0, padx=10)
        self.descriptionTextBox = tk.CTkTextbox(self.formFrameTop, height=150)
        self.descriptionTextBox.configure(wrap="word")
        self.descriptionTextBox.grid(row=1, column=1, padx=10, pady=10)

        # Priority
        self.priorityLabel = tk.CTkLabel(self.formFrameBottom, text="Select Priority")
        self.priorityLabel.grid(row=0,column=0, padx=2)
        self.priorityComboBox = tk.CTkComboBox(self.formFrameBottom, values=["Low", "Medium", "High"], state="readonly")
        self.priorityComboBox.set("Low")
        self.priorityComboBox.grid(row=0, column=1,padx=10,pady=10)

        # Date
        self.dateLabel = tk.CTkLabel(self.formFrameBottom, text="Date")
        self.dateLabel.grid(row=1,column=0)
        self.dateEntry = tk.CTkEntry(self.formFrameBottom, placeholder_text=datetime.date.today().strftime("%m/%d/%y"))
        self.dateEntry.grid(row=1,column=1,padx=10, pady=10)

        # Button
        self.confirmButton = tk.CTkButton(self, text="Confirm", command=self.confirmFunc)
        self.confirmButton.pack(padx=10, pady=10)
    '''get and check all user data, if passed, save to database, create task frame, and close popup'''
    def confirmFunc(self):
        #get data
        self.dataTitle = self.userTitleTextBox.get("1.0", "end-1c")
        self.dataDescription = self.descriptionTextBox.get("1.0","end-1c")
        self.dataPriority = self.priorityComboBox.get()
        self.dataDate = self.dateEntry.get()

        # Error Checking
        self.color = self.priorityLabel.cget("text_color")
        self.userTitleLabel.configure(text_color=self.color)
        self.descriptionLabel.configure(text_color=self.color)
        self.dateLabel.configure(text_color=self.color)
        self.failed = False
        if(len(self.dataTitle) == 0):
            self.userTitleLabel.configure(text_color="red")
            self.failed = True
        if(len(self.dataDescription) == 0):
            self.descriptionLabel.configure(text_color="red")
            self.failed = True
        if(not(len(self.dataDate) == 0) and not dateChecker(self.dataDate)):
            self.dateLabel.configure(text_color="red")
            self.failed = True
        if self.failed:
            return

        if(len(self.dataDate) == 0):
            self.dataDate = self.dateEntry.cget("placeholder_text")
        else:
            self.dataDate = datetime.datetime.strptime(self.dataDate, '%m/%d/%y').strftime("%m/%d/%y")
        # create Task Frame
        self.createTaskFrame(title=self.dataTitle, description=self.dataDescription,date=self.dataDate, priority=self.dataPriority, frameToPassTo=self.frame)
        # close popup
        self.destroy()

    '''Create Task Frame Func'''
    def createTaskFrame(self, title="", description="", priority="", date="", frameToPassTo=tk):
        self.listData.append(taskClass(frameToPassTo, title=title, description=description, priority=priority, date=date, position=0, mainObj=self.mainObj, addToDatabase=True))
        self.listData[-1].grid(sticky="ew",padx=10,pady=5)
        frameToPassTo.columnconfigure(0,weight=1)
'''Main gui that holds everything'''
class app(tk.CTk):
    def __init__(self):
        super().__init__()
        # add data
        roughDraft.fileChecker()

        self.title("Bug Tracker")
        self.popUpForm = None

        #linux config
        self.host = platform.system()
        if self.host == "Linux":
            self.attributes('-type', 'dialog')
        self.frame=tk.CTkFrame(self)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(row=0,column=0,sticky="nesw")
        self.tabView = tk.CTkTabview(self.frame)
        self.tabView.grid(row=0,column=0,padx=5, pady=5,sticky="nesw")
        self.tabView.add("Tracker")
        self.tabView.add("Settings")
        #four scrollable frames
        self.openContainerFrame = tk.CTkFrame(self.tabView.tab("Tracker"))
        self.openContainerFrame.grid(row=0,column=0, sticky = "nesw", padx = 15, pady=15)
        self.openFrame = tk.CTkScrollableFrame(self.openContainerFrame,label_text="Open")
        self.openFrame.grid(row=0,column=0, sticky = "nesw", padx=15,pady=15)
        self.openContainerFrame.columnconfigure(0, weight=1)
        self.openContainerFrame.grid_rowconfigure(0, weight=1)
        self.openFrame.configure(label_fg_color="#3194F0",label_text_color="white")

        self.progressContainerFrame = tk.CTkFrame(self.tabView.tab("Tracker"))
        self.progressContainerFrame.grid(row=0,column=1, sticky = "nesw", padx = 15, pady=15)
        self.progressFrame = tk.CTkScrollableFrame(self.progressContainerFrame,label_text="In Progress")
        self.progressFrame.grid(row=0,column=0, sticky = "nesw", padx = 15, pady=15)
        self.progressContainerFrame.columnconfigure(0, weight=1)
        self.progressContainerFrame.grid_rowconfigure(0, weight=1)
        self.progressFrame.configure(label_fg_color="#20B963", label_text_color="white")


        self.reviewContainerFrame = tk.CTkFrame(self.tabView.tab("Tracker"))
        self.reviewContainerFrame.grid(row=0,column=2, sticky = "nesw", padx = 15, pady=15)
        self.reviewFrame = tk.CTkScrollableFrame(self.reviewContainerFrame,label_text="Ready For Review")
        self.reviewFrame.grid(row=0,column=0, sticky = "nesw", padx = 15, pady=15)
        self.reviewContainerFrame.columnconfigure(0, weight=1)
        self.reviewContainerFrame.grid_rowconfigure(0, weight=1)
        self.reviewFrame.configure(label_fg_color="#FB6123", label_text_color="white")


        self.completeContainerFrame = tk.CTkFrame(self.tabView.tab("Tracker"))
        self.completeContainerFrame.grid(row=0,column=3, sticky = "nesw", padx = 15, pady=15)
        self.completedFrame= tk.CTkScrollableFrame(self.completeContainerFrame,label_text="Complete")
        self.completedFrame.grid(row=0,column=0,sticky="nesw", padx = 15, pady=15)
        self.completeContainerFrame.columnconfigure(0, weight=1)
        self.completeContainerFrame.grid_rowconfigure(0, weight=1)
        self.completedFrame.configure(label_fg_color="#768C90", label_text_color="white")

        # Button
        self.addTaskButton =tk.CTkButton(master=self.openContainerFrame, text="Add Task", command=self.createTask)
        self.addTaskButton.grid(row=1,column=0, sticky="nesw",pady=15, padx=15)

        #Settings stuff
        self.settingFrame = tk.CTkFrame(self.tabView.tab("Settings"))
        self.settingFrame.place(relx=.5,rely=.5,anchor=tk.CENTER)
        self.themeLabel = tk.CTkLabel(self.settingFrame,text="Light/Dark")
        self.themeLabel.grid(row=0, column=0,padx=10,pady=10)
        self.themeOptionMenu = tk.CTkOptionMenu(master = self.settingFrame, values = ["System Theme","Light","Dark"], command=self.themeSelect)
        self.themeOptionMenu.grid(row=0, column=1, padx=10,pady=10)
        self.colorLabel = tk.CTkLabel(self.settingFrame, text="Themes")
        self.colorLabel.grid(row=1,column=0)
        self.colorOptionMenu = tk.CTkOptionMenu(master = self.settingFrame, values= ["Blue", "Dark Blue", "Green","Orange","Pink", "Retro", "Violet", "Yellow"], command=self.colorSelect)
        self.colorOptionMenu.grid(row=1, column=1)
        # Color
        if roughDraft.getter()[0] == "src/orange.json":
            self.colorOptionMenu.set("Orange")
        elif roughDraft.getter()[0] == "src/pink.json":
            self.colorOptionMenu.set("Pink")
        elif roughDraft.getter()[0] == "src/retro.json":
            self.colorOptionMenu.set("Retro")
        elif roughDraft.getter()[0] == "src/violet.json":
            self.colorOptionMenu.set("Violet")
        elif roughDraft.getter()[0] == "src/yellow.json":
            self.colorOptionMenu.set("Yellow")
        elif roughDraft.getter()[0] == "blue":
            self.colorOptionMenu.set("Blue")
        elif roughDraft.getter()[0] == "dark-blue":
            self.colorOptionMenu.set("Dark Blue")
        elif roughDraft.getter()[0] == "green":
            self.colorOptionMenu.set("Green")
        if roughDraft.getter()[1] == "light":
            self.themeOptionMenu.set("Light")
        elif roughDraft.getter()[1] == "dark":
            self.themeOptionMenu.set("Dark")
        elif roughDraft.getter()[1] == "system":
            self.themeOptionMenu.set("System Theme")

        # images
        self.foxLogo = tk.CTkImage(light_image=Image.open("src/logo.png"),
                                  dark_image=Image.open("src/logo.png"),
                                  size=(100,100))
        self.imageLabel = tk.CTkLabel(self.settingFrame, image=self.foxLogo,text="")
        self.imageLabel.grid(row=2,column=0, padx=10, pady=10)
        self.foxFont = tk.CTkFont(family="Calibri", size=24)
        self.foxLabel = tk.CTkLabel(self.settingFrame, text="FoxFile Inc.", font=self.foxFont)
        self.foxLabel.grid(row=2,column=1)

        # Weight for the scrollable frames
        for x in range(4):
            self.tabView.tab("Tracker").columnconfigure(x, weight=1)
            self.tabView.tab("Tracker").grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        #currently holding all the task frame in a list
        self.allTaskList = []
        self.startupLoadData()
    '''set color theme'''
    def colorSelect(self, color):
        if color == "Orange":
            roughDraft.setter("src/orange.json", roughDraft.getter()[1])
            tk.set_default_color_theme("src/orange.json")
        if color == "Pink":
            roughDraft.setter("src/pink.json", roughDraft.getter()[1])
            tk.set_default_color_theme("src/pink.json")
        if color == "Retro":
            roughDraft.setter("src/retro.json", roughDraft.getter()[1])
            tk.set_default_color_theme("src/retro.json")
        if color == "Violet":
            roughDraft.setter("src/violet.json", roughDraft.getter()[1])
            tk.set_default_color_theme("src/violet.json")
        if color == "Yellow":
            roughDraft.setter("src/yellow.json", roughDraft.getter()[1])
            tk.set_default_color_theme("src/yellow.json")
        if color == "Blue":
            roughDraft.setter("blue", roughDraft.getter()[1])
            tk.set_default_color_theme("blue")
        if color == "Dark Blue":
            roughDraft.setter("dark-blue", roughDraft.getter()[1])
            tk.set_default_color_theme("dark-blue")
        if color == "Green":
            roughDraft.setter("green", roughDraft.getter()[1])
            tk.set_default_color_theme("green")
        self.restartPopup = tk.CTkToplevel()
        self.restartPopup.grab_set()
        self.restartLabel = tk.CTkLabel(self.restartPopup, text="restart to apply Color",padx=50,pady=50, font=self.foxFont)
        self.restartLabel.pack()
        self.restartButton =tk.CTkButton(master=self.restartPopup, text="Restart", command=self.exitFunc)
        self.restartButton.pack(padx=10,pady=20)
        self.restartPopup.protocol("WM_DELETE_WINDOW", self.exitFunc)
    def exitFunc(self):
        self.destroy()
    def themeSelect(self, color):
        if color == "Dark":
            roughDraft.setter(roughDraft.getter()[0], "dark")
            tk.set_appearance_mode("dark")
        elif color == "Light":
            roughDraft.setter(roughDraft.getter()[0], "light")
            tk.set_appearance_mode("light")
        elif color == "System Theme":
            roughDraft.setter(roughDraft.getter()[0], "system")
            tk.set_appearance_mode("system")
    '''Create all frame from database for startup'''
    def startupLoadData(self):
        self.allID = roughDraft.getAllKeys()
        print(self.allID)
        for data in self.allID:
            self.tempList = roughDraft.getValue(data)
            if (self.tempList[4] == 0):
                self.addTaskFrame(title=self.tempList[0], description=self.tempList[1], priority=self.tempList[3], date=self.tempList[2],
                                     position=self.tempList[4], frameToPassTo=self.openFrame, itemID=data)
            elif (self.tempList[4] == 1):
                self.addTaskFrame(title=self.tempList[0], description=self.tempList[1], priority=self.tempList[3], date=self.tempList[2],
                                     position=self.tempList[4], frameToPassTo=self.progressFrame, itemID=data)
            elif (self.tempList[4] == 2):
                self.addTaskFrame(title=self.tempList[0], description=self.tempList[1], priority=self.tempList[3], date=self.tempList[2],
                                     position=self.tempList[4], frameToPassTo=self.reviewFrame, itemID=data)
            elif (self.tempList[4] == 3):
                self.addTaskFrame(title=self.tempList[0], description=self.tempList[1], priority=self.tempList[3], date=self.tempList[2],
                                     position=self.tempList[4], frameToPassTo=self.completedFrame,itemID=data)
    '''Create task frame'''
    def createTaskFrame(self, title="", description="", priority="", date="", frameToPassTo=tk, position=-1):
        self.allTaskList.append(taskClass(frameToPassTo, title=title, description=description, priority=priority, date=date, position=position, mainObj=self, addToDatabase=True))
        self.allTaskList[-1].grid(sticky="ew",padx=10,pady=5)
        frameToPassTo.columnconfigure(0,weight=1)
            
    '''add task frame'''
    def addTaskFrame(self, title="", description="", priority="", date="", frameToPassTo=tk, position=-1, itemID = ""):
        self.allTaskList.append(taskClass(frameToPassTo, title=title, description=description, priority=priority, date=date, position=position, mainObj=self, itemID = itemID))
        self.allTaskList[-1].grid(sticky="ew",padx=10,pady=5)
        frameToPassTo.columnconfigure(0,weight=1)

    '''Popup for add task'''
    def createTask(self):
        if self.popUpForm is None or not self.popUpForm.winfo_exists():
            self.popUpForm = ToplevelTaskForm(frame=self.openFrame, listData=self.allTaskList, mainObj = self)  # create window if its None or destroyed
            self.popUpForm.attributes('-topmost',True)
            self.popUpForm.grab_set()
        else:
            self.popUpForm.focus()  # if window exists focus it

if __name__ == "__main__":
    roughDraft.ofileChecker()
    print(roughDraft.getter()[0])
    print(roughDraft.getter()[1])
    tk.set_appearance_mode(roughDraft.getter()[1])
    tk.set_default_color_theme(roughDraft.getter()[0])
    app = app()
    app.geometry("1200x600")
    app.mainloop()