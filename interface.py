'''
Implments a graphical user interface.
'''
import sys # Show exceptions

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from pybzip2 import *
from utils.packaging import *
from utils.convert import *

class Application(tk.Frame):
    def __init__(self, master = None):
        
        tk.Frame.__init__(self, master)
        
        self.grid(padx = 40, pady = 40)
        self.createWidgets()
        self.bzip2Blocks = None
        self.lastName = ''
        
    def createWidgets(self):
        
        # Open file
        self.openButton = tk.Button(self, text = 'Select file', width = 30,
            font=("TkTextFont", 10), command = self.openFile,bg='#BBBBBB')
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
            font=('TkDefaultFont', 38), padx = 40,
            text = 'pybzip2')
        self.infoLabel.grid(column = 5,row = 0, columnspan=10,rowspan=2,
            sticky='N')
        self.cdiLabel = tk.Label(self, fg='#444444',
            font=('TkDefaultFont', 18), padx = 40,
            text = 'CDI - FIB 2015')
        self.cdiLabel.grid(column = 5,row = 3, columnspan=10,rowspan=2,
            sticky='N')
        self.aboutLabel = tk.Label(self, fg='#444444',
            font=("TkDefaultFont", 14), padx = 40,
            text = 'Joan Ginés i Ametllé\n'\
            'Andrés Mingorance López\n'\
            'Albert Puente Encinas')
        self.aboutLabel.grid(column = 5,row = 4, columnspan=10,rowspan=3,
            sticky='N')
        
        
    # Signal functions
    def openFile(self):
        if self.bzip2Blocks != None:
            result = messagebox.askyesno("Restart", "Do you want to erase the"\
                " previous \nloaded file and load another one?", 
                icon = 'warning')
            if not result:
                return
            else:
                self.compressButton.configure(state = 'disabled')
                self.decompressButton.configure(state = 'disabled')
                self.testButton.configure(state = 'disabled')
                self.testDecButton.configure(state = 'disabled')
                self.saveButton.configure(state = 'disabled')
                self.saveDecButton.configure(state = 'disabled')
        
        path = filedialog.askopenfilename()
        if path != '':
            parts = path.split('/')
            self.lastName = parts[len(parts)-1]
            
            print ("Loading file from: ", path)
            (fileType, self.bzip2Blocks) = read_bz2(path)
            print ("Done,", len(self.bzip2Blocks), "blocks read.")
            
            if fileType == 'raw':
                self.compressButton.configure(state='normal')
                print ("Compression path unlocked.")
                
            elif fileType == 'bz2':
                self.decompressButton.configure(state='normal')
                print ("Decmpression path unlocked.")
            else:
                raise Exception('Unknown filetype')
                    
        else:
            print ("Loading cancelled.")
            self.compressButton.configure(state = 'disabled')
            self.decompressButton.configure(state = 'disabled')
            self.testButton.configure(state = 'disabled')
            self.testDecButton.configure(state = 'disabled')
            self.saveButton.configure(state = 'disabled')
            self.saveDecButton.configure(state = 'disabled')
        
        
    def compressAction(self):
        i = 0
        for block in self.bzip2Blocks:
            print ('Compressing block:', i+1)
            block.compress()
            i += 1
        
        print ('Computing ratio of compression...')
        totalSize = sum([len(block.msg) for block in self.bzip2Blocks])
        compressedSize = sum([len(block.content.toBytes()) for block in self.bzip2Blocks])
        ratio = 100*compressedSize/totalSize
        
        messagebox.showinfo('Compression done', 
            '{} {}\n{} {}%'.format(i, 'blocks compressed.',
                'Compression ratio:', "%.4f"%ratio), icon = 'info')
            
        self.compressButton.configure(state='normal')
        self.testButton.configure(state='normal')
        self.saveButton.configure(state='normal')
    
    def decompressAction(self):
        i = 0
        for block in self.bzip2Blocks:
            print ('Decompressing block:', i+1,'of',len(self.bzip2Blocks))
            block.decompress()
            i += 1
            
        print ('Computing ratio of compression...')
        totalSize = sum([len(intlist2bytes(block.decompressed)) for block in self.bzip2Blocks])
        compressedSize = sum([len(block.content.toBytes()) for block in self.bzip2Blocks])
        ratio = 100*compressedSize/totalSize
        
        messagebox.showinfo('Decompression done', 
            '{} {}\n{} {}%'.format(i, 'blocks decompressed.',
                'Compression ratio:', "%.4f"%ratio), icon = 'info')
        
        self.compressButton.configure(state='normal')
        self.testDecButton.configure(state='normal')
        self.saveDecButton.configure(state='normal')
        
    def testCompressionAction(self):
        for block in self.bzip2Blocks:
            block.decompress()
        
        original = [x.msg for x in self.bzip2Blocks]
        decompression = [x.decompressed for x in self.bzip2Blocks]
        
        if original == decompression:
            messagebox.showinfo('Validation', 
                'Compression/decompression OK.', icon = 'info')
            self.saveButton.configure(state='normal')
        else :
            messagebox.showinfo('Validation', 
                'Compression/decompression error.',
                icon = 'error')
        
    def testDecompressionAction(self):
        print("Testing decompression.")
        
        path = filedialog.askopenfilename()
        if path != '':
            print ("Loading file from: ", path)
            (fileType, rawBlocks) = read_bz2(path)

            if fileType == 'raw':
                original = [block.msg for block in rawBlocks]
                decompression = [x.decompressed for x in self.bzip2Blocks]
                if original == decompression:
                    messagebox.showinfo('Validation', 
                        'Compression/decompression OK.', icon = 'info')
                else :
                    messagebox.showinfo('Validation', 
                        'Compression/decompression error.', icon = 'error')
            else:
                print ("An uncompressed original file is required.")

        
    def saveCompressionAction(self):
        print("Saving compression...")
        
        options = {}
        options['filetypes'] = [('bzip2', '.bz2')]
        options['initialfile'] = self.lastName + '.pybz2'
        
        path = filedialog.asksaveasfilename(**options)
        if path != '':
            write_bz2(path, self.bzip2Blocks)
            messagebox.showinfo('Compression saved.', 
            'The compressed file has been saved correclty.' , icon = 'info')
        
    def saveDecompressionAction(self):
        print("Saving file...")
        options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
        
        options['initialfile'] = self.lastName.split('.pybz2')[0]
        
        path = filedialog.asksaveasfilename(**options)
        if path != '':
            write_file(path, self.bzip2Blocks)
            messagebox.showinfo('File saved.', 
            'The decompressed file has been saved correclty.' , icon = 'info')

def launchInterface():
    root = tk.Tk()
    root.geometry('800x380') # Window size
    root.resizable(0,0) # Disable resize
    root.title('pybzip2 - CDI')
    try:
        app = Application(master = root)
        app.mainloop()
    except:
        print ("Error:\n",sys.exc_info())
        root.destroy()
        
launchInterface()