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
        self.root.iconbitmap('./ssm2.ico')

        sf = ScrolledFrame(self.root, width=680, height=680)
        sf.pack(side="top", expand=1, fill="both")
        # sf.bind_arrow_keys(self.root)
        sf.bind_scroll_wheel(self.root)

        self.innerFrame = sf.display_widget(tk.Frame)

        self.ofset = 0

        self.controlers: dict[int, tuple[tk.Entry, tk.Entry, str, tk.Entry, tk.Entry, tk.Entry, tk.Entry, tk.Entry, tk.Label, tk.Label, tk.Label, tk.Label, tk.Label, tk.Button, tk.Entry]] = {}
        self.indent = []

        self.saveW, self.savaH = 0, 0

        self.buttonadd = tk.Button(self.innerFrame, command=self.add_row, text='Add one row')
        self.addMultiple = tk.Button(self.innerFrame, command=self.add_rows, text='Add rows')
        self.update = tk.Button(self.innerFrame, command=self.update_cells, text='Update')
        self.save = tk.Button(self.innerFrame, command=self.save_img, text='Save image!')
        self.savYaml = tk.Button(self.innerFrame, command=self.save_yaml, text='Export yaml or json!')
        self.view = tk.Button(self.innerFrame, command=self.view_image, text='View')
        self.autoupdateInt = tk.IntVar()
        self.autoUpdateCheckbox = tk.Checkbutton(self.innerFrame, text='auto update', var=self.autoupdateInt)

        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2)
        self.addMultiple.grid(row=self.ofset, column=4, columnspan=2)
        self.update.grid(row=self.ofset, column=8, columnspan=2)
        self.autoUpdateCheckbox.grid(row=self.ofset, column=10, columnspan=6)

        self.save.grid(row=self.ofset + 1, column=0, columnspan=2)
        self.savYaml.grid(row=self.ofset + 1, column=4, columnspan=2)
        self.view.grid(row=self.ofset + 1, column=8, columnspan=4)
        self.currentDir = r"/"

        self.rowAdded = 0

        self.lastNumberInFile = None
        self.row = 0
        self.mb = MenuBar(self)
        self.lnta = tk.Label(self.root, text='http://www.paypal.me/', relief=tk.SUNKEN, anchor=tk.W, fg='blue')
        self.lnta.bind("<Button-1>", lambda e: webbrowser.open_new("http://www.paypal.me/JikoUnderscore/1"))
        self.lnta.place(anchor=tk.S, relx=0.50, rely=1, relwidth=1)

    def view_image(self) -> None:
        if self.controlers:
            newImg: Image = self._proses_img()
            newImg.show()

    def add_rows(self) -> None:
        filez: str = askopenfilenames(title='Choose a file')
        for path in filez:
            self._add_row(path)

        if self.autoupdateInt.get():
            self.update_cells()

    def add_row(self) -> None:
        imgLoc: str = askopenfilename(title="Select Image")
        if imgLoc != "":
            self.currentDir = imgLoc
            self._add_row(imgLoc)
        if self.autoupdateInt.get():
            self.update_cells()

    def _add_row(self, imgLoc: str) -> None:
        self.update_buttons_locatons()

        fileName: str = imgLoc.split(r'/')[-1]

        fileNameNumber: re.Match | None = re.search(r'\d+', fileName)
        if fileNameNumber is None:
            numberInTheFileName: str = '0'
        else:
            numberInTheFileName: str = fileNameNumber.group()

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
        # e5.grid(row=self.rowAdded, column=10)

        l2 = tk.Label(self.innerFrame, text='y')
        e6 = tk.Entry(self.innerFrame, width=5)
        e6.insert(0, 0)
        l2.grid(row=self.rowAdded, column=11)
        e6.grid(row=self.rowAdded, column=12)

        e7 = tk.Entry(self.innerFrame, width=5)
        e7.insert(0, 0)
        # e7.grid(row=self.rowAdded, column=13)

        b = tk.Button(self.innerFrame, text='pop', command=partial(self.remove_row, self.rowAdded), font=('Helvetica', '7'), width=5)
        b.grid(row=self.rowAdded, column=14)

        l3 = tk.Label(self.innerFrame, text="frames")
        ind = tk.Entry(self.innerFrame, width=30)
        ind.insert(0, f"{fileName.split('.')[0]}_n{self.row}")
        l3.grid(row=self.rowAdded, column=15)
        ind.grid(row=self.rowAdded, column=16)

        self.controlers[self.rowAdded] = (e1, e2, imgLoc, e4, e5, e6, e7, e3, l1, l2, l3, row, col, b, ind)
        self.rowAdded += 1

    def remove_row(self, row: int) -> None:
        for ele in self.controlers[row]:
            if isinstance(ele, (tk.Entry, tk.Button, tk.Label)):
                ele.destroy()
        del self.controlers[row]

    def update_buttons_locatons(self) -> None:
        self.ofset += 1
        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2)
        self.addMultiple.grid(row=self.ofset, column=4, columnspan=2)
        self.update.grid(row=self.ofset, column=8, columnspan=2)
        self.autoUpdateCheckbox.grid(row=self.ofset, column=10, columnspan=6)

        self.save.grid(row=self.ofset + 1, column=0, columnspan=2)
        self.savYaml.grid(row=self.ofset + 1, column=4, columnspan=2)
        self.view.grid(row=self.ofset + 1, column=8, columnspan=2)

    def update_cells(self) -> None:
        if not self.controlers:
            return
        self.indent.clear()
        self.saveW, self.savaH = 0, 0
        d = {}

        for row in self.controlers.values():
            imgRow = int(row[0].get())
            imgCol = int(row[1].get())

            img: str = row[2]

            imgI: Image = Image.open(img)
            d[(imgRow, imgCol)] = imgI.size
            imgI.close()

        for row in self.controlers.values():
            imgRow = int(row[0].get())
            imgCol = int(row[1].get())

            img = row[2]

            xStart = row[3]
            xEnd = row[4]

            yStart = row[5]
            yEnd = row[6]

            self.indent.append(row[-1].get())

            imgI = Image.open(img)
            width, height = imgI.size
            imgI.close()

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
    def _calulate(d: dict, row: int, col: int) -> tuple[int, int]:
        newW = 0
        newH = 0

        for k, v in d.items():
            r, c = k
            w, h = v

            if row > r and col == c:
                newH += h
            if col > c and row == r:
                newW += w

        return newW, newH

    def _proses_img(self) -> Image:
        if self.autoupdateInt.get():
            self.update_cells()
        newImg = Image.new('RGBA', (self.saveW, self.savaH))
        for row in self.controlers.values():
            img = row[2]

            xStart = row[3]

            yStart = row[5]

            imgI = Image.open(img)

            newImg.paste(imgI, (int(xStart.get()), int(yStart.get())))

            imgI.close()
        return newImg

    def save_img(self) -> None:
        if not self.controlers:
            return
        newImg: Image = self._proses_img()
        saveimgLoc: str = asksaveasfilename(
            initialfile="Untitle.png",
            defaultextension=".png",
            filetypes=[("All files", "*.*"),
                       ("PNG files", "*.png"),
                       ("JPG files", "*.jpg")])
        if saveimgLoc != '':
            newImg.save(saveimgLoc)

    def save_yaml(self) -> None:
        if not self.controlers:
            return

        if self.autoupdateInt.get():
            self.update_cells()
        ymalfile = {non: {} for non in self.indent}

        for row in self.controlers.values():
            imgPath: str = row[2]
            img: str = imgPath.split(r'/')[-1].rsplit('.', 1)[0]

            width, height = Image.open(imgPath).size

            xStart = int(row[3].get())

            yStart = int(row[5].get())

            ymalfile[row[-1].get()][img] = {
                'h': height,
                'w': width,
                'y': yStart,
                'x': xStart,
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
        file.add_command(label='Save to CSV', command=self.save_table)
        file.add_command(label='Open CSV', command=self.load_tabel)
        file.add_separator()
        file.add_command(label="Exit", command=sys.exit)

        menubar.add_cascade(label="File", menu=file)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: windowObj.root.focus_get().event_generate('<<Cut>>'))
        editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: windowObj.root.focus_get().event_generate('<<Copy>>'))
        editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: windowObj.root.focus_get().event_generate('<<Paste>>'))
        editmenu.add_command(label="Select all", accelerator="Ctrl+A", command=lambda: windowObj.root.focus_get().event_generate('<<SelectAll>>'))
        # editmenu.add_separator()
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

    def save_table(self) -> None:
        if not self.windowObj.controlers:
            return
        saveFileName: str = asksaveasfilename(
            initialfile="Untitle.csv",
            defaultextension=".csv",
            filetypes=[("All files", "*.*"),
                       ("CSV files", "*.csv")]
        )
        with open(saveFileName, "w", encoding='utf-8') as sf:
            for row in self.windowObj.controlers.values():
                rCol: str = row[0].get()
                rRow: str = row[1].get()

                filepath = row[2]

                xStart: str = row[3].get()
                yStart: str = row[5].get()

                sprFrame: str = row[-1].get()

                sf.write(f'{rCol},{rRow},{filepath},{sprFrame},{xStart},{yStart}\n')

    def load_tabel(self) -> None:
        csvLoc: str = askopenfilename(title="Open CSV")
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
                    e4.insert(0, csv[4])
                    l1.grid(row=self.windowObj.rowAdded, column=8)
                    e4.grid(row=self.windowObj.rowAdded, column=9)

                    e5 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e5.insert(0, 0)
                    # e5.grid(row=self.windowObj.rowAdded, column=10)

                    l2 = tk.Label(self.windowObj.innerFrame, text='y')
                    e6 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e6.insert(0, csv[5])
                    l2.grid(row=self.windowObj.rowAdded, column=11)
                    e6.grid(row=self.windowObj.rowAdded, column=12)

                    e7 = tk.Entry(self.windowObj.innerFrame, width=5)
                    e7.insert(0, 0)
                    # e7.grid(row=self.windowObj.rowAdded, column=13)

                    b = tk.Button(self.windowObj.innerFrame, text='pop', command=partial(self.windowObj.remove_row, self.windowObj.rowAdded), font=('Helvetica', '7'), width=5)
                    b.grid(row=self.windowObj.rowAdded, column=14)

                    l3 = tk.Label(self.windowObj.innerFrame, text="frames")
                    ind = tk.Entry(self.windowObj.innerFrame, width=30)
                    ind.insert(0, csv[3])
                    l3.grid(row=self.windowObj.rowAdded, column=15)
                    ind.grid(row=self.windowObj.rowAdded, column=16)

                    self.windowObj.controlers[self.windowObj.rowAdded] = (e1, e2, csv[2], e4, e5, e6, e7, e3, l1, l2, l3, row, col, b, ind)
                    self.windowObj.rowAdded += 1
