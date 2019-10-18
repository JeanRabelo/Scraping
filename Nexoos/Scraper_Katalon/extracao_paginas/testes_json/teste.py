from datetime import datetime
from datetime import timedelta
from time import sleep

primeiro_momento = datetime.now()

sleep(2)

segundo_momento = datetime.now()

diferenca_de_tempo = segundo_momento - primeiro_momento

print(primeiro_momento)
