import json
import pandas as pd
import random
from datetime import datetime

# Função para carregar os dados dos produtos
def carregar_produtos(caminho_arquivo="produtos.json"):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            produtos = json.load(arquivo)
        return produtos
    except Exception as e:
        print(f"Erro ao carregar produtos: {e}")
        return None

# Função para gerar ID único para o gerador
def gerar_id_gerador():
    return random.randint(10000, 99999)

# Função para configurar geradores baseados nos produtos disponíveis
def configurar_geradores(produtos):
    # Separar produtos por categoria
    paineis = [p for p in produtos if p["Categoria"] == "Painel Solar"]
    inversores = [p for p in produtos if p["Categoria"] == "Inversor"]
    controladores = [p for p in produtos if p["Categoria"] == "Controlador de carga"]
    
    geradores = []
    ids_geradores_usados = set()
    
    # Para cada potência de inversor disponível
    for inversor in inversores:
        potencia_inversor = inversor["Potencia em W"]
        
        # Encontrar controladores compatíveis com a potência do inversor
        controladores_compativeis = [c for c in controladores if c["Potencia em W"] == potencia_inversor]
        
        if not controladores_compativeis:
            continue
            
        # Para cada controlador compatível
        for controlador in controladores_compativeis:
            # Para cada modelo de painel solar disponível
            for painel in paineis:
                potencia_painel = painel["Potencia em W"]
                
                # Se a potência do painel for menor que a do inversor, verificar quantos painéis são necessários
                if potencia_painel <= potencia_inversor and potencia_inversor % potencia_painel == 0:
                    qtd_paineis = potencia_inversor // potencia_painel
                    
                    # Gerar ID único para o gerador
                    id_gerador = gerar_id_gerador()
                    while id_gerador in ids_geradores_usados:
                        id_gerador = gerar_id_gerador()
                    ids_geradores_usados.add(id_gerador)
                    
                    # Adicionar componentes ao gerador
                    gerador = []
                    
                    # Adicionar painéis
                    gerador.append({
                        "ID Gerador": id_gerador,
                        "Potência do Gerador (em W)": potencia_inversor,
                        "ID Produto": painel["Id"],
                        "Nome do Produto": painel["Produto"],
                        "Quantidade Item": qtd_paineis
                    })
                    
                    # Adicionar inversor
                    gerador.append({
                        "ID Gerador": id_gerador,
                        "Potência do Gerador (em W)": potencia_inversor,
                        "ID Produto": inversor["Id"],
                        "Nome do Produto": inversor["Produto"],
                        "Quantidade Item": 1
                    })
                    
                    # Adicionar controlador
                    gerador.append({
                        "ID Gerador": id_gerador,
                        "Potência do Gerador (em W)": potencia_inversor,
                        "ID Produto": controlador["Id"],
                        "Nome do Produto": controlador["Produto"],
                        "Quantidade Item": 1
                    })
                    
                    geradores.extend(gerador)
    
    return geradores

# Função para exportar os geradores para CSV
def exportar_para_csv(geradores, nome_arquivo="geradores_configurados.csv"):
    try:
        df = pd.DataFrame(geradores)
        df.to_csv(nome_arquivo, index=False)
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao exportar para CSV: {e}")
        return None

# Função para gerar conteúdo do e-mail
def gerar_email(geradores):
    # Contar número de geradores únicos
    ids_unicos = set([g["ID Gerador"] for g in geradores])
    num_geradores = len(ids_unicos)
    
    # Obter data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Montar conteúdo do e-mail
    assunto = f"Geradores solares configurados - Semana de {data_atual}"
    
    corpo = f"""
Olá Equipe de Marketing,

Segue o relatório semanal de configuração de geradores solares.

Foram configurados {num_geradores} geradores de energia solar esta semana.

Os detalhes completos de cada gerador estão disponíveis no arquivo CSV anexo a este e-mail.

Atenciosamente,
Equipe de Engenharia
Neosolar
"""
    
    return {"assunto": assunto, "corpo": corpo}

# Função para exportar o e-mail para um arquivo PDF
def exportar_email_para_pdf(email, nome_arquivo="email_marketing.txt"):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f"Assunto: {email['assunto']}\n\n")
            arquivo.write(email['corpo'])
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao exportar e-mail: {e}")
        return None

# Função principal
def main():
    # Carregar produtos do arquivo JSON
    produtos = carregar_produtos()
    
    if not produtos:
        print("Não foi possível carregar os produtos. Verifique o arquivo de produtos.")
        return
    
    # Configurar geradores
    print("Configurando geradores...")
    geradores = configurar_geradores(produtos)
    
    if not geradores:
        print("Não foi possível configurar nenhum gerador com os produtos disponíveis.")
        return
    
    # Exportar geradores para CSV
    print("Exportando geradores para CSV...")
    arquivo_csv = exportar_para_csv(geradores)
    
    if not arquivo_csv:
        print("Erro ao exportar geradores para CSV.")
        return
    
    # Gerar e-mail
    print("Gerando e-mail para equipe de marketing...")
    email = gerar_email(geradores)
    
    # Exportar e-mail para PDF (simulado com TXT neste exemplo)
    arquivo_email = exportar_email_para_pdf(email)
    
    if not arquivo_email:
        print("Erro ao exportar e-mail.")
        return
    
    print(f"Processo concluído com sucesso!")
    print(f"Foram configurados {len(set([g['ID Gerador'] for g in geradores]))} geradores.")
    print(f"Arquivo CSV gerado: {arquivo_csv}")
    print(f"Arquivo de e-mail gerado: {arquivo_email}")

# Executar o programa principal
if __name__ == "__main__":
    main()
