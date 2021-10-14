import json
import sys
import tkinter as tk
import yaml
import re
from tkinter.filedialog import askopenfilename, asksaveasfilename, askopenfilenames
from PIL import Image
from tkscrolledframe import ScrolledFrame
from functools import partial
import webbrowser


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sprite Sheet Maker')
        self.root.geometry("1280x680")
        self.root.resizable(width=True, height=True)

        sf = ScrolledFrame(self.root, width=680, height=680)
        sf.pack(side="top", expand=1, fill="both")
        # sf.bind_arrow_keys(self.root)
        sf.bind_scroll_wheel(self.root)

        self.innerFrame = sf.display_widget(tk.Frame)

        self.ofset = 0

        self.controlers: dict[int: list[tk.Entry]] = {}
        self.indent = []

        self.saveW, self.savaH = 0, 0

        self.buttonadd = tk.Button(self.innerFrame, command=self.add_row, text='Add one row')
        self.addMultiple = tk.Button(self.innerFrame, command=self.add_rows, text='Add rows')
        self.update = tk.Button(self.innerFrame, command=self.update_cells, text='Update')
        self.save = tk.Button(self.innerFrame, command=self.save_img, text='Save image!')
        self.savYaml = tk.Button(self.innerFrame, command=self.save_yaml, text='Export yaml or json!')
        self.view = tk.Button(self.innerFrame, command=self.view_image, text='View')

        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2)
        self.addMultiple.grid(row=self.ofset, column=4, columnspan=2)
        self.update.grid(row=self.ofset, column=8, columnspan=2)

        self.save.grid(row=self.ofset + 1, column=0, columnspan=2)
        self.savYaml.grid(row=self.ofset + 1, column=4, columnspan=2)
        self.view.grid(row=self.ofset + 1, column=8, columnspan=2)
        self.currentDir = r"/"

        self.rowAdded = 0

        self.lastNumberInFile = None
        self.row = 0
        self.mb = MenuBar(self)
        self.lnta = tk.Label(self.root, text='Click to donate to my PAYPAL', relief=tk.SUNKEN, anchor=tk.W)
        self.lnta.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.paypal.me/JikoUnderscore/1"))
        self.lnta.place(anchor=tk.S, relx=0.50, rely=1, relwidth=1)

    def view_image(self):
        if self.controlers:
            newImg = self._proses_img()
            newImg.show()

    def add_rows(self):
        filez = askopenfilenames(title='Choose a file')
        for path in filez:
            self._add_row(path)

    def add_row(self):
        imgLoc = askopenfilename(title="Select Image")
        if imgLoc != "":
            self.currentDir = imgLoc

            self._add_row(imgLoc)

    def _add_row(self, imgLoc):
        self.update_buttons_locatons()

        fileName = imgLoc.split(r'/')[-1]
        numberInTheFileName = (re.search(r'\d+', fileName).group())
        if self.lastNumberInFile == numberInTheFileName:
            self.row += 1

        if self.lastNumberInFile is None:
            self.lastNumberInFile = numberInTheFileName

        row = tk.Label(self.innerFrame, text='row')
        e1 = tk.Entry(self.innerFrame, width=5)
        e1.insert(0, self.row)
        row.grid(row=self.rowAdded, column=0)
        e1.grid(row=self.rowAdded, column=1)

        col = tk.Label(self.innerFrame, text='col')
        e2 = tk.Entry(self.innerFrame, width=5)
        e2.insert(0, numberInTheFileName)
        col.grid(row=self.rowAdded, column=2)
        e2.grid(row=self.rowAdded, column=3)

        e3 = tk.Entry(self.innerFrame, width=len(imgLoc))
        e3.insert(0, imgLoc)
        e3.grid(row=self.rowAdded, column=4, columnspan=3)

        l1 = tk.Label(self.innerFrame, text='x')
        e4 = tk.Entry(self.innerFrame, width=5)
        e4.insert(0, 0)
        l1.grid(row=self.rowAdded, column=8)
        e4.grid(row=self.rowAdded, column=9)

        e5 = tk.Entry(self.innerFrame, width=5)
        e5.insert(0, 0)
        e5.grid(row=self.rowAdded, column=10)

        l2 = tk.Label(self.innerFrame, text='y')
        e6 = tk.Entry(self.innerFrame, width=5)
        e6.insert(0, 0)
        l2.grid(row=self.rowAdded, column=11)
        e6.grid(row=self.rowAdded, column=12)

        e7 = tk.Entry(self.innerFrame, width=5)
        e7.insert(0, 0)
        e7.grid(row=self.rowAdded, column=13)

        b = tk.Button(self.innerFrame, text='pop', command=partial(self.remove_row, self.rowAdded), font=('Helvetica', '7'), width=5)
        b.grid(row=self.rowAdded, column=14)

        l3 = tk.Label(self.innerFrame, text="frames")
        ind = tk.Entry(self.innerFrame, width=30)
        ind.insert(0, f"{fileName.split('.')[0]}_n{self.row}")
        l3.grid(row=self.rowAdded, column=15)
        ind.grid(row=self.rowAdded, column=16)


        self.controlers[self.rowAdded] = [e1, e2, imgLoc, e4, e5, e6, e7, e3, l1, l2, l3, row, col, b, ind]
        self.rowAdded += 1

    def remove_row(self, row):
        for ele in self.controlers[row]:
            if isinstance(ele, (tk.Entry, tk.Button, tk.Label)):
                ele.destroy()
        del self.controlers[row]

    def update_buttons_locatons(self):
        self.ofset += 1
        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2)
        self.addMultiple.grid(row=self.ofset, column=4, columnspan=2)
        self.update.grid(row=self.ofset, column=8, columnspan=2)

        self.save.grid(row=self.ofset + 1, column=0, columnspan=2)
        self.savYaml.grid(row=self.ofset + 1, column=4, columnspan=2)
        self.view.grid(row=self.ofset + 1, column=8, columnspan=2)

    def update_cells(self):
        if not self.controlers:
            return
        self.indent.clear()
        self.saveW, self.savaH = 0, 0
        d = {}

        for row in self.controlers.values():
            imgRow = int(row[0].get())
            imgCol = int(row[1].get())

            img = row[2]

            img = Image.open(img)
            d[(imgRow, imgCol)] = img.size
            img.close()

        for row in self.controlers.values():
            imgRow = int(row[0].get())
            imgCol = int(row[1].get())

            img = row[2]

            xStart = row[3]
            xEnd = row[4]

            yStart = row[5]
            yEnd = row[6]

            self.indent.append(row[-1].get())

            img = Image.open(img)
            width, height = img.size
            img.close()

            w, h = self._calulate(d, imgRow, imgCol)

            xStart.delete(0, tk.END)
            xStart.insert(0, w)

            xEnd.delete(0, tk.END)
            xEnd.insert(0, w + width)

            yStart.delete(0, tk.END)
            yStart.insert(0, h)

            yEnd.delete(0, tk.END)
            yEnd.insert(0, h + height)

            if int(yEnd.get()) > self.savaH:
                self.savaH = int(yEnd.get())
            if int(xEnd.get()) > self.saveW:
                self.saveW = int(xEnd.get())

    @staticmethod
    def _calulate(d: dict, row: int, col: int):
        newW = 0
        newH = 0

        for k, v in d.items():
            r, c = k
            w, h = v

            if r < row and c == col:
                newH += h
            if c < col and r == row:
                newW += w
        return newW, newH


    def _proses_img(self):
        # self.update_cells()
        newImg = Image.new('RGBA', (self.saveW, self.savaH))
        for row in self.controlers.values():
            # imgRow = row[0]
            # imgCol = row[1]

            img = row[2]

            xStart = row[3]
            # xEnd = row[4]

            yStart = row[5]
            # yEnd = row[6]

            img = Image.open(img)

            newImg.paste(img, (int(xStart.get()), int(yStart.get())))

            img.close()
        return newImg

    def save_img(self):
        if not self.controlers:
            return
        newImg = self._proses_img()
        saveimgLoc = asksaveasfilename(
            initialfile="Untitle.png",
            defaultextension=".png",
            filetypes=[("All files", "*.*"),
                       ("PNG files", "*.png"),
                       ("JPG files", "*.jpg")])
        if saveimgLoc != '':
            newImg.save(saveimgLoc)

    def save_yaml(self):
        if not self.controlers:
            return

        # self.update_cells()
        ymalfile = {non: {} for non in self.indent}

        for i, row in enumerate(self.controlers.values()):
            # imgRow = row[0]
            # imgCol = row[1]

            imgPath = row[2]
            img = imgPath.split(r'/')[-1]

            width, height = Image.open(imgPath).size


            xStart = row[3]
            xEnd = row[4]

            yStart = row[5]
            yEnd = row[6]

            ymalfile[row[-1].get()][f"{img}{i}"] = {
                'x': [xStart.get(), xEnd.get()],
                'y': [yStart.get(), yEnd.get()],
                'w': width,
                'h': height
            }


        saveimgLoc: str = asksaveasfilename(
            initialfile="Untitle.yaml",
            defaultextension=".yaml",
            filetypes=[("All files", "*.*"),
                       ("YAML files", "*.yaml"),
                       ("JSON files", "*.json")])
        if saveimgLoc != '':
            with open(saveimgLoc, "w") as f:
                if saveimgLoc.endswith(".yaml"):
                    yaml.dump(ymalfile, f, default_flow_style=None)
                else:
                    json.dump(ymalfile, f, ensure_ascii=False, indent=4)



class MenuBar:
    def __init__(self, windowObj: Window):
        menubar = tk.Menu(windowObj.root)
        windowObj.root.config(menu=menubar)

        self.windowObj = windowObj

        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label='Save to CSV', command=self.seve_table)
        file.add_command(label='Open CSV', command=self.load_tabel)
        file.add_separator()
        file.add_command(label="Exit", command=sys.exit)

        menubar.add_cascade(label="File", menu=file)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: windowObj.root.focus_get().event_generate('<<Cut>>'))
        editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: windowObj.root.focus_get().event_generate('<<Copy>>'))
        editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: windowObj.root.focus_get().event_generate('<<Paste>>'))
        editmenu.add_command(label="Select all", accelerator="Ctrl+A", command=lambda: windowObj.root.focus_get().event_generate('<<SelectAll>>'))
        editmenu.add_separator()
        # editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=rodi.ent_txt.edit_undo)
        # editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=rodi.ent_txt.edit_redo)
        menubar.add_cascade(label="Edit", menu=editmenu)

        options = tk.Menu(menubar, tearoff=0)
        options.add_command(label='Add one row!', accelerator="F1", command=windowObj.add_row)
        options.add_command(label='Add rows!', accelerator="F2", command=windowObj.add_rows)
        options.add_command(label='Update!', accelerator="F5", command=windowObj.update_cells)
        options.add_separator()
        options.add_command(label='View!', command=windowObj.view_image)
        options.add_separator()
        options.add_command(label='Save image!', command=windowObj.save_img)
        options.add_command(label='Export json or yaml', command=windowObj.save_yaml)
        menubar.add_cascade(label="Options", menu=options)

        windowObj.root.bind('<F1>', lambda x: windowObj.add_row())
        windowObj.root.bind('<F2>', lambda x: windowObj.add_rows())
        windowObj.root.bind('<F5>', lambda x: windowObj.update_cells())

    def seve_table(self):
        if not self.windowObj.controlers:
            return
        saveFileName = asksaveasfilename(
            initialfile="Untitle.csv",
            defaultextension=".csv",
            filetypes=[("All files", "*.*"),
                       ("CSV files", "*.csv")]
        )
        with open(saveFileName, "w", encoding='utf-8') as sf:
            for row in self.windowObj.controlers.values():

                rCol = row[0].get()
                rRow = row[1].get()


                filepath = row[2]

                sprFrame = row[-1].get()


                sf.write(f'{rCol},{rRow},{filepath},{sprFrame}\n')

    def load_tabel(self):
        csvLoc = askopenfilename(title="Open CSV")



        if csvLoc != '':
            self.windowObj.controlers.clear()
            self.windowObj.rowAdded = 0

            with open(csvLoc, 'r') as fr:
                for csvRow in fr:
                    csv = csvRow.split(',')
                    self.windowObj.update_buttons_locatons()

                    row = tk.Label(self.windowObj.innerFrame, text='row')
                    e1 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e1.insert(0, csv[0])
                    row.grid(row=self.windowObj.rowAdded, column=0)
                    e1.grid(row=self.windowObj.rowAdded, column=1)

                    col = tk.Label(self.windowObj.innerFrame, text='col')
                    e2 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e2.insert(0, csv[1])
                    col.grid(row=self.windowObj.rowAdded, column=2)
                    e2.grid(row=self.windowObj.rowAdded, column=3)

                    e3 = tk.Entry(self.windowObj.innerFrame, width=len(csv[2]))
                    e3.insert(0, csv[2])
                    e3.grid(row=self.windowObj.rowAdded, column=4, columnspan=3)

                    l1 = tk.Label(self.windowObj.innerFrame, text='x')
                    e4 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e4.insert(0, 0)
                    l1.grid(row=self.windowObj.rowAdded, column=8)
                    e4.grid(row=self.windowObj.rowAdded, column=9)

                    e5 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e5.insert(0, 0)
                    e5.grid(row=self.windowObj.rowAdded, column=10)

                    l2 = tk.Label(self.windowObj.innerFrame, text='y')
                    e6 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e6.insert(0, 0)
                    l2.grid(row=self.windowObj.rowAdded, column=11)
                    e6.grid(row=self.windowObj.rowAdded, column=12)

                    e7 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e7.insert(0, 0)
                    e7.grid(row=self.windowObj.rowAdded, column=13)

                    b = tk.Button(self.windowObj.innerFrame, text='pop', command=partial(self.windowObj.remove_row, self.windowObj.rowAdded), font=('Helvetica', '7'), width=5)
                    b.grid(row=self.windowObj.rowAdded, column=14)

                    l3 = tk.Label(self.windowObj.innerFrame, text="frames")
                    ind = tk.Entry(self.windowObj.innerFrame, width=30)
                    ind.insert(0, csv[3])
                    l3.grid(row=self.windowObj.rowAdded, column=15)
                    ind.grid(row=self.windowObj.rowAdded, column=16)

                    self.windowObj.controlers[self.windowObj.rowAdded] = [e1, e2, csv[2], e4, e5, e6, e7, e3, l1, l2, l3, row, col, b, ind]
                    self.windowObj.rowAdded += 1
