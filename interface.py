'''
Implments a graphical user interface.
'''
import sys # Show exceptions

import tkinter as tk
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(padx = 40, pady = 40)
        self.createWidgets()
        
    def createWidgets(self):
        
        # Open file
        self.openButton = tk.Button(self, text = 'Select file', width = 30,
            font=("TkTextFont", 10), command = self.selectAction)
        self.openButton.grid(column = 1,row = 0, columnspan=3)
        
        # Compression branch widgets
        self.compressButton = tk.Button(self, text = 'Compress', width = 20,
            font=("TkTextFont", 10), command = self.compressAction,
            state = 'disabled')
        self.compressButton.grid(column = 0,row = 2, columnspan=2)
        
        self.testButton = tk.Button(self, text = 'Test compression',width = 20,
            font=("TkTextFont", 10), command = self.testCompressionAction,
            state = 'disabled')
        self.testButton.grid(column = 0,row = 4, columnspan=2)
        
        self.saveButton = tk.Button(self, text = 'Save compressed file', 
            width = 20, font=("TkTextFont", 10), 
            command = self.saveCompressionAction,
            state = 'disabled')
        self.saveButton.grid(column = 0,row = 6, columnspan=2)
        
        self.arrow1 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = ' ↙',pady = 7)
        self. arrow1.grid(column = 0,row = 1, columnspan=2)
        
        self.arrow3 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7, state = 'disabled')
        self.arrow3.grid(column = 0,row = 3, columnspan=2)
        
        self.arrow5 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7, state = 'disabled')
        self.arrow5.grid(column = 0,row = 5, columnspan=2)
        
        # Space widget (middle)
        self.space = tk.Label(self,text = ' ', padx = 20)
        self.space.grid(column = 2,row = 2, columnspan=1,sticky='EW')
        
        # Decompression branch widgets
        self.decompressButton = tk.Button(self, text = 'Decompress', width = 20,
            font=("TkTextFont", 10), command = self.decompressAction,
            state = 'disabled')
        self.decompressButton.grid(column = 3,row = 2, columnspan=2)
        
        self.testDecButton = tk.Button(self, text = 'Compare (optional)',
            width = 20,
            font=("TkTextFont", 10), command = self.testDecompressionAction,
            state = 'disabled')
        self.testDecButton.grid(column = 3,row = 4, columnspan=2)
        
        self.saveDecButton = tk.Button(self, text = 'Save file', width = 20,
            font=("TkTextFont", 10), command = self.saveDecompressionAction,
            state = 'disabled')
        self.saveDecButton.grid(column = 3,row = 6, columnspan=2)
        
        self.arrow1d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↘ ',pady = 7)
        self.arrow1d.grid(column = 3,row = 1, columnspan=2)
        
        self.arrow3d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7, state = 'disabled')
        self.arrow3d.grid(column = 3,row = 3, columnspan=2)
        
        self.arrow5d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7, state = 'disabled')
        self.arrow5d.grid(column = 3,row = 5, columnspan=2)
        
        # About (information) widgets
        self.infoLabel = tk.Label(self, fg='#3088F0',
            font=('TkDefaultFont', 40), padx = 40,
            text = 'bzip2')
        self.infoLabel.grid(column = 5,row = 0, columnspan=10,rowspan=2,
            sticky='N')
        self.cdiLabel = tk.Label(self, fg='#444444',
            font=('TkDefaultFont', 18), padx = 40,
            text = 'CDI - FIB 2015')
        self.cdiLabel.grid(column = 5,row = 3, columnspan=10,rowspan=2,
            sticky='N')
        self.aboutLabel = tk.Label(self, fg='#444444',
            font=("TkDefaultFont", 14), padx = 40,
            text = 'Joan Ginés Ametllé\n'\
            'Andrés Mingorance López\n'\
            'Albert Puente Encinas')
        self.aboutLabel.grid(column = 5,row = 4, columnspan=10,rowspan=3,
            sticky='N')
        
        
    # Signal functions
    def selectAction(self):
        path = filedialog.askopenfilename()
        print ("Load file from: ", path)
        if path != '':
            # self.data = andres.read(path)
            self.compressButton.configure(state='normal')
            self.decompressButton.configure(state='normal')
        
    def compressAction(self):
        print("compression!")
        
        # self.compression = andres.read(self.data)
        
        self.compressButton.configure(state='normal')
        self.testButton.configure(state='normal')
    
    def decompressAction(self):
        print("decompression!")
        
        # self.decompression = andres.decompress(self.data)
        
        self.compressButton.configure(state='normal')
        self.testDecButton.configure(state='normal')
        self.saveDecButton.configure(state='normal')
        
    def testCompressionAction(self):
        print("test compression!")
        
        # self.info = andres.compare(self.data,
        #     andres.decompress( andres.compress(data) )
        
        self.saveButton.configure(state='normal')
        
    def testDecompressionAction(self):
        print("test decompression (optional)!")
        
        path = filedialog.askopenfilename()
        # originalData = andres.read(path)
        # self.info = andres.compare(originalData, self.decompression)
        
    def saveCompressionAction(self):
        print("save compression!")
        path = filedialog.asksaveasfilename()
        print(path)
        # andres.save(self.compression, path)
        
    def saveDecompressionAction(self):
        print("save decompression!")
        path = filedialog.asksaveasfilename()
        print(path)
        # andres.save(self.decompression, path)

def launchInterface():
    root = tk.Tk()
    root.geometry('800x380') # Window size
    root.resizable(0,0) # Disable resize
    root.title('bzip2 - CDI Project')
    root.iconbitmap('icon.ico')
    try:
        app = Application(master = root)
        app.mainloop()
    except:
        print ("Error:\n",sys.exc_info())
        root.destroy()
        
launchInterface()