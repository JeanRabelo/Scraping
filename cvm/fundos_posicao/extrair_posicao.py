import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup as BS

# url_beginning = 'https://cvmweb.cvm.gov.br/swb/default.asp?sg_sistema=fundosreg'
url_beginning = r'https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx'

s = requests.Session()
response = s.get(url_beginning)
soup = BS(response.content, 'html.parser')
txt_code = soup.find('img').get('src')[2:]
print(txt_code)
root = tk.Tk()

url_img = "https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica" + txt_code
        # https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/RandomTxt.aspx?v1=0,340107971029406
print(url_img)
response = requests.get(url_img)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

def pegar(senha):
    args = dict()
    args['txtCNPJNome'] = 'Mantiqueira'
    args['numRandom'] = senha
    args['ddlTpFdo'] = 0
    args['btnContinuar'] = 'Continuar >'

    url_post2 = r'https://cvmweb.cvm.gov.br/SWB//Sistemas/SCW/CPublica/CConsolFdo/FormBuscaParticFdo.aspx'
    url_post3 = r'https://cvmweb.cvm.gov.br/SWB/Sistemas/SCW/CPublica/CConsolFdo/ResultBuscaParticFdo.aspx?CNPJNome=Mantiqueira&TpPartic=0&Adm=false&numRandom='+senha+'&SemFrame='
    response2 = s.post(url_post2, args)
    response3 = s.get(url_post3)
    soup3 = BS(response3.content, 'html.parser')
    print(senha)
    print(soup3)

class gui_captcha:
    def __init__(self, root):
        self.master = root
        self.panel = tk.Label(root, image=img)
        self.panel.pack() #side="top", fill="both", expand="yes")
        self.entry = tk.Entry(root)
        self.entry.pack() #side="top", fill="both", expand="yes")
        self.botao = tk.Button(root, text='Ok', command=self.on_button)
        self.botao.pack() #side="top", fill="both", expand="yes"

    def on_button(self):
        pegar(self.entry.get())
        self.master.destroy()

my_gui = gui_captcha(root)
root.mainloop()
