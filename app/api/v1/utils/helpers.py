import re

# La Ñ se conserva porque es una letra, no un acento
_VOWEL_ACCENTS = str.maketrans({
    "Á": "A",
    "É": "E",
    "Í": "I",
    "Ó": "O",
    "Ú": "U",
    "Ü": "U",
})



_SPECIAL_CHARS = {
    "\\": "",
    ":": "",
    "[": "",
    "]": "",
    "#": "",
    "°": "",
    "-": " ",
    '"': "",
    ",": "",
    "!": "",
    "¿": "",
    "¡": "",
    "“": "",
    "”": "",
}



STREET_ABBREVIATIONS = {
    "CALLE": "C.",
    "AVENIDA": "AV.",
    "BOULEVARD": "BLVD.",
    "CARRETERA": "CARR.",
    "SIN NUMERO": "SN.",
    "S/N": "SN.",
    "NUMERO": "NUM.",
    "EDIFICIO": "EDIF.",
    "KILOMETRO": "KM.",
    "CIRCUITO":"CTO."
}


ORG_ABBREVIATIONS = {
    "SERVICIO DE ADMINISTRACION TRIBUTARIA": "S.A.T.",
    "SECRETARIA DE ADMINISTRACION TRIBUTARIA": "S.A.T.",
    "SECRETARIA DE CONTRALORIA GENERAL": "S.C.E.",
    "CONTRALORIA GENERAL DEL ESTADO": "C.G.E.",
    "ORGANO INTERNO DE CONTROL": "O.I.C.",
    "ORGANO DE CONTROL INTERNO": "O.I.C.",
    "BAJA CALIFORNIA SUR": "B.C.S.",
    "SAN LUIS POTOSI": "S.L.P.",
    "UNIVERSIDAD": "UNI.",
    "AUTONOMA": "AUT.",
    "ADMINISTRACION": "ADMON.",
    "SECRETARIA": "SECRET.A",
    "ESTADO": "EDO.",
    "MUNICIPIO":"MPIO."
}


JOB_ROLE_ABBREVIATIONS = {
    "ADMINISTRADORA DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "ADMINISTRADOR DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "BAJA CALIFORNIA SUR": "B.C.S.",
    "SAN LUIS POTOSI": "S.L.P.",
    "ESTADO": "EDO",
    "ADMINISTRADORA": "ADMIN.",
    "ADMINISTRADOR": "ADMIN.",
    "ADMINISTRACION": "ADMON.",
    "PRESIDENTA": "PDTA.",
    "PRESIDENTE": "PDTE.",
    "DIRECTORA": "DIR.A",
    "DIRECTOR": "DIR.",
    "SECRETARIA": "SECRET.A",
    "SECRETARIO": "SEC.",
    "GOBERNADOR": "GOB.",
    "UNIVERSIDAD": "UNI",
    "AUTONOMA": "AUT.",
    "MAESTRA": "MTRA.",
    "MAESTRO": "MTRO.",
    "PROFESORA": "PROFA.",
    "PROFESOR": "PROF.",
    "DIPUTADA": "DIP.",
    "DIPUTADO": "DIP.",
    "SENADORA": "SEN.",
    "SENADOR": "SEN.",
    "DOCTORA": "DRA.",
    "DOCTOR": "DR.",
    "TITULAR": "TIT.",
    "GENERAL": "GRAL.",
}



TITLE_ABBREVIATIONS = {
    "CONTADOR PUBLICO": "C.P.",
    "CIUDADANO": "C.",
    "CIUDADANA": "C.",
    "ABOGADO": "ABG.",
    "ABOGADA": "ABG.",
    "ACTUARIO": "ACT.",
    "ACTUARIA": "ACT.",
    "DOCTORA": "DRA.",
    "DOCTOR": "DR.",
    "GOBERNADORA": "GOB.",
    "GOBERNADOR": "GOB.",
    "INGENIERA": "ING.",
    "INGENIERO": "ING.",
    "LICENCIADA": "LIC.",
    "LICENCIADO": "LIC.",
    "MAESTRA": "MTRA.",
    "MAESTRO": "MTRO.",
    "PROFESORA": "PROFA.",
    "PROFESOR": "PROF.",
    "SEÑORA": "SRA.",
    "SEÑOR": "SR.",
}


_SHIPMENT_NAME_RECEIVER = {
    "ADMINISTRADORA DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "ADMINISTRADOR DESCONCENTRADA DE RECAUDACION": "ADM. DESC. DE REC.",
    "BAJA CALIFORNIA SUR": "B.C.S.",
    "SAN LUIS POTOSI": "S.L.P.",
    "ESTADO": "EDO",
    "ADMINISTRADORA": "ADMIN.",
    "ADMINISTRADOR": "ADMIN.",
    "ADMINISTRACION": "ADMON.",
    "PRESIDENTA": "PDTA.",
    "PRESIDENTE": "PDTE.",
    "DIRECTORA": "DIR.A",
    "DIRECTOR": "DIR.",
    "SECRETARIA": "SECRET.A",
    "SECRETARIO": "SEC.",
    "GOBERNADOR": "GOB.",
    "UNIVERSIDAD": "UNI",
    "AUTONOMA": "AUT.",
    "MAESTRA": "MTRA.",
    "MAESTRO": "MTRO.",
    "PROFESORA": "PROFA.",
    "PROFESOR": "PROF.",
    "DIPUTADA": "DIP.",
    "DIPUTADO": "DIP.",
    "SENADORA": "SEN.",
    "SENADOR": "SEN.",
    "DOCTORA": "DRA.",
    "DOCTOR": "DR.",
    "TITULAR": "TIT.",
    "GENERAL": "GRAL.",
    "SERVICIO DE ADMINISTRACION TRIBUTARIA": "S.A.T.",
    "SECRETARIA DE CONTRALORIA GENERAL": "S.C.E.",
    "ORGANO INTERNO DE CONTROL": "O.I.C.",
    "ORGANO DE CONTROL INTERNO": "O.I.C.",
    "CONTRALORIA GENERAL DEL ESTADO": "C.G.E.",
    "BAJA CALIFORNIA SUR": "B.C.S.",
    "SAN LUIS POTOSI": "S.L.P.",
    "ESTADO": "EDO",
    "ADMINISTRACION": "ADMON.",
    "SECRETARIA": "SECRET.A",
    "CONTADOR PUBLICO": "C.P.",
    "CIUDADANO": "C.",
    "CIUDADANA": "C.",
    "ABOGADO": "ABG.",
    "ABOGADA": "ABG.",
    "ACTUARIO": "ACT.",
    "ACTUARIA": "ACT.",
    "DOCTORA": "DRA.",
    "DOCTOR": "DR.",
    "GOBERNADORA": "GOB.",
    "GOBERNADOR": "GOB.",
    "INGENIERA": "ING.",
    "INGENIERO": "ING.",
    "LICENCIADA": "LIC.",
    "LICENCIADO": "LIC.",
    "MAESTRA": "MTRA.",
    "MAESTRO": "MTRO.",
    "PROFESORA": "PROFA.",
    "PROFESOR": "PROF.",
    "SEÑORA": "SRA.",
    "SEÑOR": "SR.",
}



def clean_base_text(text: str, *, drop_slash: bool = False, drop_parens: bool= False):
    value = str(text or "").upper().translate(_VOWEL_ACCENTS).replace("?", "Ñ")
    if drop_parens:
        value = value.replace("(", "").replace(")", "")
    if drop_slash:
        value = value.replace("/", "")
    for char, replacement in _SPECIAL_CHARS.items():
        value = value.replace(char, replacement)
    return collapse(value)


def collapse(text: str) -> str:
    text = re.sub(r"\.{2,}", ".", text)
    return re.sub(r"\s+", " ", text).strip()


_PHONE_JUNK = ("TELEFONO", "NUMERO", "NUM", "NOM", "TEL", "NO")

TEL_PATTERN = re.compile(
    r"(?<!\w)(?:"
    + "|".join(re.escape(word) for word in sorted(_PHONE_JUNK, key=len, reverse=True))
    + r")\.?(?!\w)"
)

def normalize_phone(text: str) -> str:
    text_clean = clean_base_text(text)
    text_clean = TEL_PATTERN.sub("", text_clean)
    return collapse(text_clean)


def _apply_terms(text: str, mapping: dict[str, str]) -> str:
    if not text or not mapping:
        return text
    
    words = sorted(
        mapping,
        key=len,
        reverse=True
    )

    regex = r"(?<!\w)(?:{})(?!\w)".format(
        "|".join(
            re.escape(word) for word in words
        )
    )

    pattern = re.compile(regex)

    return collapse(
        pattern.sub(
            lambda match: mapping[match.group(0)],
            text
        )
    )


def normalize_address(text: str) -> str:
    text = text.strip().upper()
    text_clean = clean_base_text(text)
    return _apply_terms(text_clean, STREET_ABBREVIATIONS)

def normalize_state(text: str) -> str:
    text = text.strip().upper()
    return clean_base_text(text, drop_slash=True, drop_parens=True)

def normalize_organization(text: str) -> str:
    text_clean = clean_base_text(text=text.strip().upper())
    return _apply_terms(text_clean, ORG_ABBREVIATIONS)

def normalize_job_role(text: str) -> str:
    text_clean = clean_base_text(text.strip().upper())
    return _apply_terms(text_clean, JOB_ROLE_ABBREVIATIONS)

def normalize_name_receiver_shipment(text: str):
    text_clean = clean_base_text(text, drop_slash=False, drop_parens=True)
    return _apply_terms(text_clean, _SHIPMENT_NAME_RECEIVER)

def normalize_email(value: str) -> str:
    return value.strip().lower()

def normalize_campos_shipments(text: str) -> str:
    return str(text or "").upper().translate(_VOWEL_ACCENTS).replace("?", "Ñ")




