import json
import tkinter as tk
import yaml
from tkinter.filedialog import askopenfilename, asksaveasfilename, askopenfilenames
from PIL import Image
from tkscrolledframe import ScrolledFrame
from functools import partial


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Sprite Sheet Maker')
        self.root.geometry("480x480")
        self.root.resizable(width=True, height=True)

        sf = ScrolledFrame(self.root, width=640, height=480)
        sf.pack(side="top", expand=1, fill="both")
        sf.bind_arrow_keys(self.root)
        sf.bind_scroll_wheel(self.root)

        self.innerFrame = sf.display_widget(tk.Frame)

        self.ofset = 0

        self.controlers: dict[int: list[tk.Entry]] = {}

        self.saveW, self.savaH = 0, 0

        self.buttonadd = tk.Button(self.innerFrame, command=self.add_row, text='ADdd')
        self.addMultiple = tk.Button(self.innerFrame, command=self.add_rows, text='Add rows')
        self.update = tk.Button(self.innerFrame, command=self.update_cells, text='Update')
        self.save = tk.Button(self.innerFrame, command=self.save_img, text='save!')
        self.savYaml = tk.Button(self.innerFrame, command=self.save_yaml, text='Export yaml or json!')
        self.view = tk.Button(self.innerFrame, command=self.view_image, text='view')

        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2, sticky=tk.W)
        self.addMultiple.grid(row=self.ofset, column=2, columnspan=2, sticky=tk.W)
        self.update.grid(row=self.ofset, column=4, columnspan=2, sticky=tk.W)
        self.save.grid(row=self.ofset + 1, column=0, columnspan=2, sticky=tk.W)
        self.savYaml.grid(row=self.ofset + 1, column=2, columnspan=2, sticky=tk.W)
        self.view.grid(row=self.ofset + 1, column=4, columnspan=2, sticky=tk.W)

        self.currentDir = r"/"

        self.rowAdded = 0

    def view_image(self):
        newImg = self._proses_img()
        newImg.show()

    def add_rows(self):
        filez = askopenfilenames(title='Choose a file')
        print(filez)
        print(len(filez))
        for path in filez:
            self._add_row(path)

    def add_row(self):
        imgLoc = askopenfilename(initialdir=self.currentDir, title="Select Image")
        if imgLoc != "":
            self.currentDir = imgLoc

        self._add_row(imgLoc)

    def _add_row(self, imgLoc):
        self.update_buttons_locatons()

        e1 = tk.Entry(self.innerFrame, width=5)
        e1.insert(0, 0)
        e1.grid(row=self.rowAdded, column=0)

        e2 = tk.Entry(self.innerFrame, width=5)
        e2.insert(0, 0)
        e2.grid(row=self.rowAdded, column=1)

        e3 = tk.Entry(self.innerFrame, width=len(imgLoc))
        e3.insert(0, imgLoc)
        e3.grid(row=self.rowAdded, column=2, columnspan=3)

        l1 = tk.Label(self.innerFrame, text='x')
        e4 = tk.Entry(self.innerFrame, width=5)
        e4.insert(0, 0)
        l1.grid(row=self.rowAdded, column=6)
        e4.grid(row=self.rowAdded, column=7)

        e5 = tk.Entry(self.innerFrame, width=5)
        e5.insert(0, 0)
        e5.grid(row=self.rowAdded, column=8)

        l2 = tk.Label(self.innerFrame, text='y')
        e6 = tk.Entry(self.innerFrame, width=5)
        e6.insert(0, 0)
        l2.grid(row=self.rowAdded, column=9)
        e6.grid(row=self.rowAdded, column=10)

        e7 = tk.Entry(self.innerFrame, width=5)
        e7.insert(0, 0)
        e7.grid(row=self.rowAdded, column=11)

        b = tk.Button(self.innerFrame, text='pop', command=partial(self.remove_row, self.rowAdded), font=('Helvetica', '7'), width=5)
        b.grid(row=self.rowAdded, column=12)

        self.controlers[self.rowAdded] = [e1, e2, imgLoc, e4, e5, e6, e7, e3, l1, l2, b]
        self.rowAdded += 1

    def remove_row(self, row):
        for ele in self.controlers[row]:
            if isinstance(ele, (tk.Entry, tk.Button, tk.Label)):
                ele.destroy()
        del self.controlers[row]

    def update_buttons_locatons(self):
        self.ofset += 1
        self.buttonadd.grid(row=self.ofset, column=0, columnspan=2, sticky=tk.W)
        self.addMultiple.grid(row=self.ofset, column=2, columnspan=2, sticky=tk.W)
        self.update.grid(row=self.ofset, column=4, columnspan=2, sticky=tk.W)
        self.save.grid(row=self.ofset + 1, column=0, columnspan=2, sticky=tk.W)
        self.savYaml.grid(row=self.ofset + 1, column=2, columnspan=2, sticky=tk.W)
        self.view.grid(row=self.ofset + 1, column=4, columnspan=2, sticky=tk.W)

    def update_cells(self):
        for row in self.controlers.values():
            imgRow = row[0]
            imgCol = row[1]

            img = row[2]

            xStart = row[3]
            xEnd = row[4]

            yStart = row[5]
            yEnd = row[6]

            img = Image.open(img)
            width, height = img.size
            img.close()

            xStart.delete(0, tk.END)
            xStart.insert(0, int(imgCol.get()) * width)

            xEnd.delete(0, tk.END)
            xEnd.insert(0, int(xStart.get()) + width)

            yStart.delete(0, tk.END)
            yStart.insert(0, int(imgRow.get()) * height)

            yEnd.delete(0, tk.END)
            yEnd.insert(0, int(yStart.get()) + height)

            if int(yEnd.get()) > self.savaH:
                self.savaH = int(yEnd.get())
            if int(xEnd.get()) > self.saveW:
                self.saveW = int(xEnd.get())

        print(self.savaH, self.saveW)

    def _proses_img(self):
        self.update_cells()
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
        newImg = self._proses_img()
        saveimgLoc = asksaveasfilename(
            initialfile="Untitle.png",
            defaultextension=".png",
            filetypes=[("All files", "*.*"),
                       ("PNG files", "*.png"),
                       ("JPG files", "*.jpg")])

        newImg.save(saveimgLoc)

    def save_yaml(self):
        self.update_cells()
        print('saveing')
        ymalfile = {}
        for i, row in enumerate(self.controlers.values()):
            # imgRow = row[0]
            # imgCol = row[1]

            img = row[2]

            xStart = row[3]
            xEnd = row[4]

            yStart = row[5]
            yEnd = row[6]

            ymalfile[f"{img}{i}"] = {
                    'x': [xStart.get(), xEnd.get()],
                    'y': [yStart.get(), yEnd.get()]
                 }

        print(ymalfile)
        saveimgLoc:str = asksaveasfilename(
            initialfile="Untitle.yaml",
            defaultextension=".yaml",
            filetypes=[("All files", "*.*"),
                       ("YAML files", "*.yaml"),
                       ("JSON files", "*.json")])



        with open(saveimgLoc, "w") as f:
            if saveimgLoc.endswith(".yaml"):
                yaml.dump(ymalfile, f, default_flow_style=None)
            else:
                json.dump(ymalfile, f, ensure_ascii=False, indent=4)









