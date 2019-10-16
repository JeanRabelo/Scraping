from bs4 import BeautifulSoup
import base64
import tempfile

from sep_scrapers.captcha import CaptchaSolver
from sep_scrapers.exceptions import TargetNotFound, BadCaptchaSolution, InsufficientInformation
from sep_scrapers import session

# KNOWN PROBLEMS works only off commercial hours

GET_FORM = 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublicaSonoro.asp'
POST_FORM = 'https://servicos.receita.fazenda.gov.br/Servicos/CPF/ConsultaSituacao/ConsultaPublicaExibir.asp'

def get_form(s):
    first_form = s.get(GET_FORM, verify=False, timeout=10)

    fs = BeautifulSoup(first_form.text, 'html.parser')

    captcha_el = fs.find(id='imgCaptcha')
    captcha_attr = captcha_el['src']
    _, imgdata = captcha_attr.split(",", 1)
    fd, imgpath = tempfile.mkstemp(prefix='rfb_cpf_', suffix='.png')
    with open(fd, 'wb') as fp:
        fp.write(base64.b64decode(imgdata))

    return imgpath

def post_form(s, cpf, dob, captcha):
    form_data = {
        'txtCPF': cpf,
        'txtDataNascimento': dob,
        'txtTexto_captcha_serpro_gov_br': captcha,
        'Enviar': 'Consultar',
        'idCheckedReCaptcha': 'false',
        'CPF': '',
        'NASCIMENTO': '',
    }

    return s.post(POST_FORM, data=form_data, verify=False, timeout=10)

def parse_report(page):
    response = {}
    ps = BeautifulSoup(page.text, 'html.parser')

    fields = [
        'cpf',
        'nome',
        'nascimento',
        'situacao',
        'inscricao',
        'digito',
        'emitido',
        'controle',
    ]

    for i, d in enumerate(ps.find_all('span', class_='clConteudoDados')):
        response[fields[i]] = d.b.text

    comps = ps.find_all('span', class_='clConteudoComp')
    response['emitido'] = ' '.join([ x.text for x in comps[0].find_all('b') ])
    response['controle'] = comps[1].b.text

    return response

def scrape(cpf, dob):
    if not cpf or not dob:
        raise InsufficientInformation

    cs = CaptchaSolver('rfb_cpf')
    s = session.requests_retry_session()

    captcha_img = get_form(s)
    captcha = cs.solve(captcha_img)
    result = post_form(s, cpf, dob, captcha)

    # we might've failed captcha here, but it's fine
    if ("CPF não encontrado" in result.text) or \
            ("Data de nascimento informada" in result.text):
        cs.good_solve()
        raise TargetNotFound

    try:
        dict = parse_report(result)
    except IndexError: # parse fail, bad captcha
        cs.bad_solve()
        raise BadCaptchaSolution

    cs.good_solve()
    return dict
