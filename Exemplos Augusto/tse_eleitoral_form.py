import json
import unidecode

from django.conf import settings
from sep_scrapers.contrib.dbc_api_python3 import deathbycaptcha

from sep_scrapers.exceptions import TargetNotFound, InsufficientInformation
from sep_scrapers import session

# ok 25/07 7pm

TSE_PGURL = "http://www.tse.jus.br/eleitor/servicos/titulo-de-eleitor/situacao-eleitoral/consulta-por-nome"
TSE_GKEY = "6Lc0k1MUAAAAAJgAqPTO0dutvMB_m4ZVuvcvUMhA"

POST_URL = "http://www.tse.jus.br/eleitor/servicos/titulo-de-eleitor/situacao-eleitoral/consulta-por-nome/@@consulta_situacao_eleitoral"

def get_form(s):
    cd = {
        'googlekey': TSE_GKEY,
        'pageurl': TSE_PGURL,
    }

    client = deathbycaptcha.SocketClient(settings.DBC_USER, settings.DBC_PASS)
    captcha = client.decode(type = 4, token_params = json.dumps(cd))

    return captcha

def post_form(s, captcha, nome, dob):
    data = {
        'nomeTituloEleitor': nome,
        'dataNascimento': dob,
        'g-recaptcha-response': captcha,
    }

    return s.post(POST_URL, data=data, timeout=10)

def parse_result(dict):
    lines = dict['output'].split('\n')

    return {
        'nome': lines[4].strip(),
        'nascimento': lines[9].strip(),
        'situacao': lines[14].strip(),
    }

def scrape(nome, dob):
    if not nome or not dob:
        raise InsufficientInformation

    s = session.requests_retry_session()
    captcha = get_form(s)
    result = post_form(s, captcha['text'], nome, dob)

    if "conferem com aqueles constantes" in result.text:
        raise TargetNotFound

    return parse_result(json.loads(result.text))
