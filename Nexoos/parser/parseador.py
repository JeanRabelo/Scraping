PATH_FILE = r'C:\Users\jean_\Documents\GitHub\Scraping\Nexoos\pagina_salva\Nexoos - Um novo jeito de fazer empréstimo.html'

with open(PATH_FILE,'r', errors='ignore') as arquivo: #, encoding='utf32'
    print(arquivo.read())
