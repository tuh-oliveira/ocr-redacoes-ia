from difflib import SequenceMatcher

def calcular_similaridade(a, b):
    return round(SequenceMatcher(None, a, b).ratio() * 100, 2)