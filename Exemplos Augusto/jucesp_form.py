from bs4 import BeautifulSoup
import tempfile
import time
import pdftotext

from django.conf import settings

from sep_scrapers.captcha import CaptchaSolver
from sep_scrapers.exceptions import TargetNotFound, BadCaptchaSolution, InsufficientInformation
from sep_scrapers import session
from sep_scrapers.util import norm_cnpj

from . import jucesp_cert_simpl

# ok 25/07

BASE_URL = 'https://www.jucesponline.sp.gov.br/'
FIRST_FORM = 'ResultadoBusca.aspx'
NIRE_PAGE = 'Pre_Visualiza.aspx?nire={}&idproduto='
LOGIN_AND_DL_URL = "login.aspx?ReturnUrl=%2fRestricted%2fGeraDocumento.aspx%3fnire%3d{nire}%26tipoDocumento%3d4&nire={nire}&tipoDocumento=4"

def first_form(s, search_term):
    ff = s.get(BASE_URL + FIRST_FORM)
    time.sleep(3)

    ffs = BeautifulSoup(ff.text, 'html.parser')

    form_data = {
        'ctl00$ajaxMaster': 'ctl00$cphContent$ajaxForm|ctl00$cphContent$frmBuscaSimples$btPesquisar',
        'ctl00$cphContent$frmBuscaSimples$txtPalavraChave': search_term,
        'ctl00$cphContent$frmBuscaSimples$btPesquisar': "Buscar",
        '__ASYNCPOST': True,
    }

    for hi in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        form_data[hi] = ffs.find(id = hi)['value']

    sf = s.post(BASE_URL + FIRST_FORM, data=form_data)
    time.sleep(3)

    sfs = BeautifulSoup(sf.text, 'html.parser')

    for hi in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        form_data[hi] = sfs.find(id = hi)['value']

    img_url = BASE_URL + sfs.find('img', height=50)['src']

    r = s.get(img_url, allow_redirects=True)
    time.sleep(3)

    fd, imgpath = tempfile.mkstemp(prefix='jucesp_', suffix='.jpg')
    with open(fd, 'wb') as fp:
        fp.write(r.content)

    return imgpath, form_data

def second_form(s, prev_form_data, captcha_val):
    form_data = {
        'ctl00$ajaxMaster': 'ctl00$cphContent$ajaxGrid|ctl00$cphContent$gdvResultadoBusca$btEntrar',
        'ctl00$cphContent$gdvResultadoBusca$CaptchaControl1': captcha_val,
        'ctl00$cphContent$gdvResultadoBusca$btEntrar': 'Continuar',
        '__ASYNCPOST': True,
    }

    for hi in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        form_data[hi] = prev_form_data[hi]

    form_data['ctl00$cphContent$frmBuscaSimples$txtPalavraChave'] = \
        prev_form_data['ctl00$cphContent$frmBuscaSimples$txtPalavraChave']

    return s.post(BASE_URL + FIRST_FORM, data=form_data)

def process_search_results(sf):
    sfs = BeautifulSoup(sf.text, 'html.parser')
    results_table = sfs.find('table', id='ctl00_cphContent_gdvResultadoBusca_gdvContent')

    results = []

    for tr in results_table.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) < 3:
            continue

        results.append({
            'nire': tds[0].a.text,
            'razao': tds[1].span.text,
            'municipio': tds[2].text,
        })

    return results

def nire_search(s, nire):
    np = s.get(BASE_URL + NIRE_PAGE.format(nire))
    nps = BeautifulSoup(np.text, 'html.parser')
    return {
        'emissao': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblEmissao').text,
        'razao': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblEmpresa').text,
        'nire': nps.find(id="ctl00_cphContent_frmPreVisualiza_lblNire").text,
        'tipo': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblDetalhes').text,
        'data_da_constituicao': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblConstituicao').text,
        'inicio_de_atividade': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblAtividade').text,
        'cnpj': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblCnpj').text,
        'inscricao_estadual': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblInscricao').text,
        'objeto': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblObjeto').text,
        'capital': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblCapital').text,
        'logradouro': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblLogradouro').text,
        'numero': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblNumero').text,
        'bairro': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblBairro').text,
        'complemento': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblComplemento').text,
        'municipio': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblMunicipio').text,
        'cep': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblCep').text,
        'uf': nps.find(id='ctl00_cphContent_frmPreVisualiza_lblUf').text,
    }

def get_login_form(s, nire):
    np = s.get(BASE_URL + LOGIN_AND_DL_URL.format(nire = nire))
    nps = BeautifulSoup(np.text, 'html.parser')

    img_url = BASE_URL + nps.find('img', height=50)['src']

    r = s.get(img_url, allow_redirects=True)
    fd, imgpath = tempfile.mkstemp(prefix='jucesp_', suffix='.jpg')
    with open(fd, 'wb') as fp:
        fp.write(r.content)

    form_data = {}
    for hi in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        form_data[hi] = nps.find(id = hi)['value']

    return imgpath, form_data

def post_login_form(s, prev_form_data, captcha, nire):
    form_data = {
        'ctl00$cphContent$txtEmail': settings.JUCESP_USER,
        'ctl00$cphContent$txtSenha': settings.JUCESP_PASS,
        'ctl00$cphContent$CaptchaControl1': captcha,
        'ctl00$cphContent$btEntrar': 'Entrar',
    }

    for hi in ['__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION']:
        form_data[hi] = prev_form_data[hi]

    return s.post(BASE_URL + LOGIN_AND_DL_URL.format(nire = nire), data=form_data, allow_redirects=True)

def scrape(cnpj=None, razao_social=None):
    if not cnpj or not razao_social:
        raise InsufficientInformation

    cs = CaptchaSolver('jucesp')
    s = session.requests_retry_session()
    captcha_img, form_data = first_form(s, razao_social)
    captcha_val = cs.solve(captcha_img)

    time.sleep(3) # dunno either, but it works

    sf = second_form(s, form_data, captcha_val)

    # we might've failed captcha here, but it's fine
    if 'nenhuma empresa correspondente' in sf.text:
        cs.good_solve()
        raise TargetNotFound

    try:
        raz_search = process_search_results(sf)
        cs.good_solve()
    except AttributeError:
        cs.bad_solve()
        raise BadCaptchaSolution

    dict = None
    if len(raz_search) == 1:
        tmp_dict = nire_search(s, raz_search[0]['nire'])
        if not tmp_dict['cnpj'].strip() or norm_cnpj(tmp_dict['cnpj']) == norm_cnpj(cnpj):
            dict = tmp_dict

    else:
        for e in raz_search:
            tmp_dict = nire_search(s, e['nire'])
            if norm_cnpj(tmp_dict['cnpj']) == norm_cnpj(cnpj):
                dict = tmp_dict
                break

    if dict:
        captcha_img, form_data = get_login_form(s, dict['nire'])
        captcha_val = cs.solve(captcha_img)
        time.sleep(3) # dunno either, but it works
        pdf_data = post_login_form(s, form_data, captcha_val, dict['nire'])
        fd, pdfpath = tempfile.mkstemp(prefix='jucesp_', suffix='.pdf')
        with open(fd, 'wb') as fp:
            fp.write(pdf_data.content)

        try:
            dict['diretoria'] = jucesp_cert_simpl.parse_cert_simpl(pdfpath)
            cs.good_solve()
        except pdftotext.Error:
            cs.bad_solve()
            raise BadCaptchaSolution

        return dict, pdfpath
    else:
        # fell through with no matches
        raise TargetNotFound
