"""Vérification mécanique des citations : un passage cité existe-t-il mot pour mot ?"""
import re
import unicodedata

_APOSTROPHES = str.maketrans({"’": "'", "‘": "'", "ʼ": "'"})


def normalize(text: str) -> str:
    """Neutralise ce qui ne change pas le sens : espaces, apostrophes, forme Unicode.

    La casse, les accents, la ponctuation et les chiffres sont conservés :
    une citation doit rester exacte.
    """
    text = unicodedata.normalize("NFC", text).translate(_APOSTROPHES)
    return re.sub(r"\s+", " ", text.replace(" ", " ").replace(" ", " ")).strip()


def contains_quote(source: str, quote: str) -> bool:
    """Vrai si ``quote`` figure mot pour mot dans ``source``. Une citation vide est fausse."""
    needle = normalize(quote)
    return bool(needle) and needle in normalize(source)
