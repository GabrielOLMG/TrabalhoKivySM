import numpy as np

def perguntas(arquivo = 'inputs\Input_Trivia.txt'):
    f = open(arquivo,encoding='utf-8')
    #6 linhas por perguinta
    linhas = list(f)
    linhas = [linha[:-1] for linha in linhas]
    perguntas = np.array_split(linhas,len(linhas)//6)
    return perguntas

def mimica(arquivo = 'inputs\mimica.txt'):
    f = open(arquivo,encoding='utf-8')
    linhas = list(f)
    linhas = [linha[:-1] for linha in linhas]
    return linhas

if __name__ == "__main__":
    mimica()