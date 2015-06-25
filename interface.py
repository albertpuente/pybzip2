'''
Implments a graphical user interface.
'''
import sys # Show exceptions

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from pybzip2 import *

class Application(tk.Frame):
    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.grid(padx = 40, pady = 40)
        self.createWidgets()
        self.bzip2 = None
        
    def createWidgets(self):
        
        # Open file
        self.openButton = tk.Button(self, text = 'Select file', width = 30,
            font=("TkTextFont", 10), command = self.selectAction,bg='#BBBBBB')
        self.openButton.grid(column = 1,row = 0, columnspan=3)
        
        # Compression branch widgets
        self.compressButton = tk.Button(self, text = 'Compress', width = 20,
            font=("TkTextFont", 10), command = self.compressAction,
            state = 'disabled',bg='#BBBBBB')
        self.compressButton.grid(column = 0,row = 2, columnspan=2)
        
        self.testButton = tk.Button(self, text = 'Test compression',width = 20,
            font=("TkTextFont", 10), command = self.testCompressionAction,
            state = 'disabled',bg='#BBBBBB')
        self.testButton.grid(column = 0,row = 4, columnspan=2)
        
        self.saveButton = tk.Button(self, text = 'Save compressed file', 
            width = 20, font=("TkTextFont", 10), 
            command = self.saveCompressionAction,
            state = 'disabled',bg='#BBBBBB')
        self.saveButton.grid(column = 0,row = 6, columnspan=2)
        
        self.arrow1 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '   ↙',pady = 7)
        self. arrow1.grid(column = 0,row = 1, columnspan=2)
        
        self.arrow3 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7)
        self.arrow3.grid(column = 0,row = 3, columnspan=2)
        
        self.arrow5 = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7)
        self.arrow5.grid(column = 0,row = 5, columnspan=2)
        
        # Space widget (middle)
        self.space = tk.Label(self,text = ' ', padx = 20)
        self.space.grid(column = 2,row = 2, columnspan=1,sticky='EW')
        
        # Decompression branch widgets
        self.decompressButton = tk.Button(self, text = 'Decompress', width = 20,
            font=("TkTextFont", 10), command = self.decompressAction,
            state = 'disabled',bg='#BBBBBB')
        self.decompressButton.grid(column = 3,row = 2, columnspan=2)
        
        self.testDecButton = tk.Button(self, text = 'Compare (optional)',
            width = 20,
            font=("TkTextFont", 10), command = self.testDecompressionAction,
            state = 'disabled',bg='#BBBBBB')
        self.testDecButton.grid(column = 3,row = 4, columnspan=2)
        
        self.saveDecButton = tk.Button(self, text = 'Save file', width = 20,
            font=("TkTextFont", 10), command = self.saveDecompressionAction,
            state = 'disabled',bg='#BBBBBB')
        self.saveDecButton.grid(column = 3,row = 6, columnspan=2)
        
        self.arrow1d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↘   ',pady = 7)
        self.arrow1d.grid(column = 3,row = 1, columnspan=2)
        
        self.arrow3d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7)
        self.arrow3d.grid(column = 3,row = 3, columnspan=2)
        
        self.arrow5d = tk.Label(self, fg='#333333',
            font=("TkTextFont", 20),
            text = '↓',pady = 7)
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
        if self.bzip2 != None:
            result = messagebox.askyesno("Restart", "Do you want to erase the"\
                " previous \nloaded file and load another one?", 
                icon = 'warning')
            if not result:
                return
            else:
                self.testButton.configure(state = 'disabled')
                self.testDecButton.configure(state = 'disabled')
                self.saveButton.configure(state = 'disabled')
                self.saveDecButton.configure(state = 'disabled')
                
        
        path = filedialog.askopenfilename()
        if path != '':
            print ("Loading file from: ", path)
            with open(path, "rb") as file:
                bytes = file.read(file_size)

            self.bzip2 = pybzip2compressor(list(bytes))
            
            self.compressButton.configure(state='normal')
            self.decompressButton.configure(state='normal')
        else:
            print ("Loading cancelled")
        
    def compressAction(self):
        self.bzip2.compress()
        ratio = 100*len(self.bzip2.compressed)/len(self.bzip2.msg)
        messagebox.showinfo('Compression done', 
                'Compression ratio: %f%%'%ratio, icon = 'info')
        self.compressButton.configure(state='normal')
        self.testButton.configure(state='normal')
    
    def decompressAction(self):
        self.bzip2.decompress()
        
        self.compressButton.configure(state='normal')
        self.testDecButton.configure(state='normal')
        self.saveDecButton.configure(state='normal')
        
    def testCompressionAction(self):
        self.bzip2.decompress()
        if self.bzip2.msg == self.bzip2.decompressed:
            messagebox.showinfo('Validation', 
                'Compression/decompression OK.', icon = 'info')
            self.saveButton.configure(state='normal')
        else :
            messagebox.showinfo('Validation', 
                'Compression/decompression error.',
                icon = 'error')
        
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
    root.title('bzip2 - CDI')
    try:
        app = Application(master = root)
        app.mainloop()
    except:
        print ("Error:\n",sys.exc_info())
        root.destroy()
        
launchInterface()