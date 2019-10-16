import pdftotext
import re

MULTI_SPACES = re.compile(r'\s\s+')

def clear_dict():
    return {
        'nome': None,
        'endereco': None,
        'numero': None,
        'complemento': None,
        'bairro': None,
        'municipio': None,
        'uf': None,
        'cep': None,
        'rg': None,
        'cpf': None,
        'cargo': None,
        'cotas': None,
    }

def parse_cert_simpl(filename):
    with open(filename, 'rb') as f:
        p = pdftotext.PDF(f)

    joined_pages = '\n'.join(p)
    lines = joined_pages.split('\n')
    clean_lines = [ l for l in lines if l.strip() and not l.startswith(('Documento Gratuito', 'Proibida a Comercialização')) ]

    board = []

    trailing_block_idx = None
    p = clear_dict()
    for i, l in enumerate(clean_lines):
        if l == "NOME":
            p['nome'] = clean_lines[i + 1]
        elif p['nome'] and l.startswith('ENDEREÇO') and l.endswith('COMPLEMENTO'):
            nl = clean_lines[i + 1]
            if nl.startswith('BAIRRO'): # no data
                continue
            else:
                end_idx = l.index('ENDEREÇO')
                nro_idx = l.index('NÚMERO')
                cmpl_idx = l.index('COMPLEMENTO')
                p['endereco'] = nl[end_idx:nro_idx].strip()
                p['numero'] = nl[nro_idx:cmpl_idx].strip()
                p['complemento'] = nl[cmpl_idx:].strip()

        elif p['nome'] and l.startswith('BAIRRO') and l.endswith(('RG', 'CEP')):
            nl = clean_lines[i + 1]
            if nl.startswith(('DOCUMENTO', 'CPF')): # no data
                continue
            else:
                bairro_idx = l.index('BAIRRO')
                munic_idx = l.index('MUNICÍPIO')
                uf_idx = l.index('UF')
                cep_idx = l.index('CEP')
                rg_idx = l.index('RG') if 'RG' in l else -1

                p['bairro'] = nl[bairro_idx:munic_idx].strip()
                p['municipio'] = nl[munic_idx:uf_idx].strip()
                p['uf'] = nl[uf_idx:cep_idx].strip()
                p['cep'] = nl[cep_idx:rg_idx].strip()
                p['rg'] = nl[rg_idx:].strip() if rg_idx != 1 else None

        elif p['nome'] and l.startswith(('CPF', 'DOCUMENTO')): # documento é para estrangeiros
            nl = clean_lines[i + 1]
            trailing_block_idx = i + 2

            cpf_idx = l.index('CPF') if 'CPF' in l else l.index('DOCUMENTO')
            cargo_idx = l.index('CARGO')
            cotas_idx = l.index('QUANTIDADE COTAS')

            p['cpf'] = nl[cpf_idx:cargo_idx].strip()
            p['cargo'] = nl[cargo_idx:cotas_idx].strip()
            p['cotas'] = nl[cotas_idx:].strip()

        elif p['nome'] and trailing_block_idx and i >= trailing_block_idx:
            if not l[cpf_idx:cargo_idx].strip() and l[cargo_idx].strip():
                p['cargo'] += ' ' + l[cargo_idx:cotas_idx].strip()
            else:
                board.append(p)
                trailing_block_idx = None
                p = clear_dict()

    return board
