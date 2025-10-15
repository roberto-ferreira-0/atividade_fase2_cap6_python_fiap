import json
import pandas as pd

def obter_resposta_sim_nao(pergunta):
    respostas_validas = ['s','n']
    while True:
        resposta = input(pergunta + 's/n ').lower()
        if resposta in respostas_validas:
            return resposta == 's'
        else:
            print("resposta inválida")

def obter_numero_positivo(pergunta):
    while True:
        try:
            numero = int(input(pergunta))
            if numero > 0:
                return numero
            else:
                print('Digite um número positivo')
        except ValueError:
            print('Por favor, digite um número válido')

def classificar_dados():
    dados = {}

    dados['tipo_producao'] = input('Qual a cultura predominante em sua propriedade? ')
    dados['uso_fertilizante'] = input(f'Qual o fertilizante mais usado em sua plantação de {dados["tipo_producao"]}? ')
    dados['numero_hectares'] = obter_numero_positivo(f'Quantos hectares sua produção de {dados["tipo_producao"]} possui? ')
    dados['calagem_recente'] = obter_resposta_sim_nao(f'Você realizou a calagem e sua produção de {dados["tipo_producao"]} nos últimos 12 meses? ')
    dados['mudanca_uso_terra'] = obter_resposta_sim_nao('Houve mudança do uso da terra em sua propriedade nos últimos 12 meses? ')
    dados['presenca_biodigestao'] = obter_resposta_sim_nao('Sua propriedade possui sistema de biodigestão dos resíduos? ')
    dados['ILPF'] = obter_resposta_sim_nao('Sua propriedade possui sistema de Integração Lavoura-Pecuária-Floresta? ')

    print()
    print('='*100)
    print()

    return dados

def calcular_pontuacao(dados):
    pontos = 0
    resultado = []

    if dados['tipo_producao']:
        pontos = pontos + 1
        resultado.append(f'Plantações de {dados["tipo_producao"]} são responsáveis pela emissão de inúmeras toneladas de CO2e')
    if dados['uso_fertilizante']:
        pontos = pontos + 1
        resultado.append(f'Usar {dados["uso_fertilizante"]} em excesso pode ser prejudicial ao meio-ambiente')
    if dados['numero_hectares']:
        pontos = pontos + 1
        resultado.append(f'{dados["numero_hectares"]} hectares de {dados["tipo_producao"]} podem gerar grandes impactos ambientais')
    if dados['calagem_recente']:
        pontos = pontos + 1
        resultado.append('A calagem, quando feita sem as devidas precauções, pode emitir grandes quantidades de CO2e, além de poder alterar a microbiota do solo')
    if dados['mudanca_uso_terra']:
        pontos = pontos + 1
        resultado.append(f'Segundo dados do SEEG, a mudança no uso da terra é a principal causa de emissão de gases de efeito estufa, requerindo cuidado redobrado')
    if dados['presenca_biodigestao']:
        pontos = pontos - 1
        resultado.append('Sistemas de biodigestão, além de diminuir a emissão de metano, produz o biogás e biofertilizante (digestato), que auxiliam na administração sustentável de propriedades rurais')
    if dados['ILPF']:
        pontos = pontos - 1
        resultado.append('A Integração Lavoura-Pecuária-Floresta promove, entre outros efeitos positivos, aumento da produtividade e captura de carbono')

    return pontos, resultado

def classificar_risco(pontos):
    if pontos <= 1:
        return 'RISCO BAIXO','Excelente! Sua propriedade adota práticas amigáveis ao meio-ambiente'
    if pontos == 2:
        return 'RISCO MÉDIO','Impacto moderado. Algumas medidas são necessárias para melhorar ainda mais a sustentabilidade de sua propriedade'
    if pontos == 3:
        return 'RISCO ALTO','Elevado impacto ambiental. Adote práticas mais sustentáveis em sua propriedade'
    if pontos >= 4:
        return 'RISCO EXTREMO','Situação crítica. Por favor, promova mudanças drásticas em suas operações'

def salvar_json(dados, pontos, risco, recomendacao):
    dados_completos = {
        'dados_propriedade': dados,
        'pontos': pontos,
        'risco': risco,
        'recomendacao': recomendacao
    }

    dados_completos_json = json.dumps(dados_completos)

    with open('registro.json', 'w+') as arquivo:
        arquivo.write(dados_completos_json)
    print('\nDados salvos com sucesso em registro.json')

def salvar_txt(dados, pontos, risco, recomendacao, resultado):
    with open('relatorio.txt', 'w+') as arquivo:
        arquivo.write('='*100 + '\n')
        arquivo.write('RELATÓRIO DE IMPACTO AMBIENTAL - Re.N.I.A.P.A.\n')
        arquivo.write('='*100 + '\n\n')

        arquivo.write(f'Cultura: {dados["tipo_producao"]}\n')
        arquivo.write(f'Fertilizante: {dados["uso_fertilizante"]}\n')
        arquivo.write(f'Hectares: {dados["numero_hectares"]}\n')
        arquivo.write(f'Calagem recente: {"Sim" if dados["calagem_recente"] else "Não"}\n')
        arquivo.write(f'Mudança uso da terra: {"Sim" if dados["mudanca_uso_terra"] else "Não"}\n')
        arquivo.write(f'Sistema de biodigestão: {"Sim" if dados["presenca_biodigestao"] else "Não"}\n')
        arquivo.write(f'ILPF (Integração Lavoura-Pecuária-Floresta): {"Sim" if dados["ILPF"] else "Não"}\n\n')

        arquivo.write(f'PONTUAÇÃO: {pontos}\n')
        arquivo.write(f'RISCO: {risco}\n')
        arquivo.write(f'RECOMENDAÇÃO: {recomendacao}\n\n')

        arquivo.write('OBSERVAÇÕES:\n')
        for obs in resultado:
            arquivo.write(f'- {obs}\n')

    print('Relatório salvo em relatorio.txt')

def ler_json():
    with open('registro.json', 'r+') as arquivo:
        dados = json.load(arquivo)
    return dados

def ler_txt():
    with open('relatorio.txt', 'r+') as arquivo:
        linhas = arquivo.readlines()

    print('\n--- CONTEÚDO DO RELATÓRIO ---')
    for linha in linhas:
        print(linha.strip())

def resumo_classificacao(dados):
    print(f'Cultura: {dados["tipo_producao"]}')
    print(f'Fertilizante: {dados["uso_fertilizante"]}')
    print(f'Número de hectares: {dados["numero_hectares"]}')
    print(f'Calagem recente: {"Sim" if dados["calagem_recente"] else "Não"}')
    print(f'Houve mudança no uso da terra? {"Sim" if dados["mudanca_uso_terra"] else "Não"}')
    print(f'Há sistemas de biodigestão? {"Sim" if dados["presenca_biodigestao"] else "Não"}')
    print(f'Há Integração Lavoura-Pecuária-Floresta? {"Sim" if dados["ILPF"] else "Não"}')

    pontos, resultado = calcular_pontuacao(dados)
    risco, recomendacao = classificar_risco(pontos)

    print(f'\nPontos: {pontos}')
    print(f'Risco: {risco}')
    print(f'Recomendação: {recomendacao}')

    return pontos, risco, recomendacao, resultado

def main():
    while True:
        print('\n' + '='*100)
        print('Bem-vind@ ao Re.N.I.A.P.A. (Registro Nacional de Impacto Ambiental em Propriedade Agrícola)')
        print('='*100)
        print('1. Nova análise')
        print('2. Ler dados salvos (JSON)')
        print('3. Ver relatório (TXT)')
        print('4. Sair')
        print('='*100)

        opcao = input('\nEscolha uma opção: ')

        match opcao:

          case '1':
              dados = classificar_dados()
              pontos, risco, recomendacao, resultado = resumo_classificacao(dados)

              salvar_json(dados, pontos, risco, recomendacao)
              salvar_txt(dados, pontos, risco, recomendacao, resultado)

          case '2':
              try:
                  dados_lidos = ler_json()
                  print('\n--- DADOS DO JSON ---')
                  print(f"Cultura: {dados_lidos['dados_propriedade']['tipo_producao']}")
                  print(f"Pontos: {dados_lidos['pontos']}")
                  print(f"Risco: {dados_lidos['risco']}")
                  print(f"Recomendação: {dados_lidos['recomendacao']}")
              except:
                  print('\nErro ao ler arquivo. Faça uma análise primeiro.')

          case '3':
              try:
                  ler_txt()
              except:
                  print('\nErro ao ler arquivo. Faça uma análise primeiro.')

          case '4':
              print('\nObrigado por usar o Re.N.I.A.P.A.!')
              break

          case _:
              print('\nOpção inválida!')

if __name__ == "__main__":
    main()
