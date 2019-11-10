import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup as BS

# url_beginning = 'https://cvmweb.cvm.gov.br/swb/default.asp?sg_sistema=fundosreg'
url_beginning = r'https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx'

s = requests.Session()
# input("Pressione enter para continuar...")
response = s.get(url_beginning)
# print(response.content)
soup = BS(response.content, 'html.parser')
txt_code = soup.find('img').get('src')[2:]
print(txt_code)
# input("Pressione enter para continuar...")
root = tk.Tk()

# def on_button():
#     print(entry.get())

# url_img = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/RandomTxt.aspx?v1=0,189657236537736"
url_img = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica" + txt_code
response = requests.get(url_img)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

class gui:
    def __init__(self, root):
        self.master = root
        # master.title = 'Uma GUI'
        self.panel = tk.Label(root, image=img)
        self.panel.pack() #side="top", fill="both", expand="yes")
        self.entry = tk.Entry(root)
        self.entry.pack() #side="top", fill="both", expand="yes")
        self.botao = tk.Button(root, text='Ok', command=self.on_button)
        self.botao.pack() #side="top", fill="both", expand="yes"

    def on_button(self):
        print(self.entry.get())
        # print('botao apertado')

# panel = tk.Label(root, image=img)
# panel.pack() #side="top", fill="both", expand="yes")
# entry = tk.Entry(root)
# entry.pack() #side="top", fill="both", expand="yes")
#
# botao = tk.Button(root, text='Ok', command=print(entry.get()))
# botao.pack(side="top", fill="both", expand="yes")
my_gui = gui(root)
root.mainloop()
