## 1. Script Python para configuração dos geradores

```python
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

```

```json
[
  {
    "Categoria": "Painel Solar",
    "Id": 1001,
    "Potencia em W": 500,
    "Produto": "Painel Solar 500 W Marca A"
  },
  {
    "Categoria": "Painel Solar",
    "Id": 1002,
    "Potencia em W": 500,
    "Produto": "Painel Solar 500 W Marca B"
  },
  {
    "Categoria": "Painel Solar",
    "Id": 1003,
    "Potencia em W": 500,
    "Produto": "Painel Solar 500 W Marca C"
  },
  {
    "Categoria": "Controlador de carga",
    "Id": 2001,
    "Potencia em W": 500,
    "Produto": "Controlador de Carga 30A Marca E"
  },
  {
    "Categoria": "Controlador de carga",
    "Id": 2002,
    "Potencia em W": 750,
    "Produto": "Controlador de Carga 50A Marca E"
  },
  {
    "Categoria": "Controlador de carga",
    "Id": 2003,
    "Potencia em W": 1000,
    "Produto": "Controlador de Carga 40A Marca D"
  },
  {
    "Categoria": "Inversor",
    "Id": 3001,
    "Potencia em W": 500,
    "Produto": "Inversor 500W Marca D"
  },
  {
    "Categoria": "Inversor",
    "Id": 3002,
    "Potencia em W": 1000,
    "Produto": "Inversor 1000W Marca D"
  }
]

```



# Assunto: Geradores solares configurados - Semana de 28/02/2025

Olá Equipe de Marketing,

Segue o relatório semanal de configuração de geradores solares.

Foram configurados 6 geradores de energia solar esta semana.

Os detalhes completos de cada gerador estão disponíveis no arquivo CSV anexo a este e-mail.

Atenciosamente,
Equipe de Engenharia
Neosolar


```csv
ID Gerador,Potência do Gerador (em W),ID Produto,Nome do Produto,Quantidade Item
32054,500,1001,Painel Solar 500 W Marca A,1
32054,500,3001,Inversor 500W Marca D,1
32054,500,2001,Controlador de Carga 30A Marca E,1
18726,500,1002,Painel Solar 500 W Marca B,1
18726,500,3001,Inversor 500W Marca D,1
18726,500,2001,Controlador de Carga 30A Marca E,1
45391,500,1003,Painel Solar 500 W Marca C,1
45391,500,3001,Inversor 500W Marca D,1
45391,500,2001,Controlador de Carga 30A Marca E,1
61247,1000,1001,Painel Solar 500 W Marca A,2
61247,1000,3002,Inversor 1000W Marca D,1
61247,1000,2003,Controlador de Carga 40A Marca D,1
73502,1000,1002,Painel Solar 500 W Marca B,2
73502,1000,3002,Inversor 1000W Marca D,1
73502,1000,2003,Controlador de Carga 40A Marca D,1
24813,1000,1003,Painel Solar 500 W Marca C,2
24813,1000,3002,Inversor 1000W Marca D,1
24813,1000,2003,Controlador de Carga 40A Marca D,1

```



# Documentação - Configurador de Geradores Solares

## Visão Geral

Este projeto implementa um script para automatizar o processo de criação de geradores solares baseados em componentes disponíveis no estoque da Neosolar. O script segue as regras de compatibilidade entre os componentes (painéis solares, inversores e controladores de carga) conforme especificado nas instruções.

## Requisitos

O script foi desenvolvido utilizando Python 3.7+ e requer as seguintes bibliotecas:
- pandas: para manipulação dos dados e exportação para CSV
- json: para leitura do arquivo de produtos
- random: para geração de IDs aleatórios para os geradores
- datetime: para obter a data atual ao gerar o e-mail

## Estrutura do Projeto

```
configurador_geradores/
│
├── configurador_geradores.py  # Script principal
├── produtos.json              # Dados dos produtos em estoque
├── geradores_configurados.csv # Saída: Tabela de geradores configurados
└── email_marketing.txt        # Saída: E-mail para o time de marketing
```

## Lógica de Funcionamento

O script segue a seguinte lógica:

1. **Carregamento dos dados**: Os produtos disponíveis são carregados do arquivo JSON.

2. **Configuração dos geradores**: Os geradores são configurados seguindo as regras:
   - Cada gerador é composto por painel solar, inversor e controlador de carga
   - Os painéis solares devem ser da mesma marca e potência
   - A potência somada dos painéis deve ser igual à potência do inversor e do controlador

3. **Algoritmo de combinação**:
   - O script percorre os inversores disponíveis
   - Para cada inversor, busca controladores de carga com a mesma potência
   - Para cada combinação inversor/controlador, verifica quais painéis são compatíveis
   - Se a potência do painel for divisível pela potência do inversor, calcula quantos painéis são necessários
   - Gera um ID único para cada gerador criado

4. **Exportação dos resultados**:
   - Os geradores configurados são exportados para um arquivo CSV
   - Um e-mail para o time de marketing é gerado com o número de geradores criados

## Funções Principais

### `carregar_produtos(caminho_arquivo="produtos.json")`
Carrega os dados dos produtos a partir do arquivo JSON especificado.

### `configurar_geradores(produtos)`
Cria as combinações possíveis de geradores com base nos produtos disponíveis, seguindo as regras de compatibilidade.

### `exportar_para_csv(geradores, nome_arquivo="geradores_configurados.csv")`
Exporta a lista de geradores configurados para um arquivo CSV.

### `gerar_email(geradores)`
Gera o conteúdo do e-mail a ser enviado para o time de marketing, incluindo o número de geradores configurados.

### `exportar_email_para_pdf(email, nome_arquivo="email_marketing.txt")`
Exporta o conteúdo do e-mail para um arquivo (formato TXT neste exemplo).

### `main()`
Função principal que orquestra o fluxo de execução do script.

## Limitações

- O script atual não faz consultas a APIs ou bancos de dados; ele lê os dados de um arquivo JSON local.
- Não inclui validação avançada de dados de entrada.
- Exporta o e-mail como um arquivo de texto simples em vez de PDF.

## Extensões Possíveis

- Implementar leitura dos produtos diretamente de uma API ou banco de dados
- Adicionar um sistema de logging para rastreamento de erros e atividades
- Implementar envio automático de e-mail
- Criar uma interface web para visualização e gerenciamento dos geradores
- Adicionar autenticação e autorização para acesso ao sistema

## Execução

Para executar o script, navegue até o diretório do projeto e execute:

```bash
python configurador_geradores.py
```

O script irá gerar dois arquivos:
1. `geradores_configurados.csv`: Contendo os detalhes de todos os geradores configurados
2. `email_marketing.txt`: Contendo o e-mail a ser enviado para o time de marketing

## Manutenção

Para adicionar novos produtos ou alterar as regras de compatibilidade:

1. **Adicionar novos produtos**: Edite o arquivo `produtos.json` adicionando novos objetos seguindo a mesma estrutura.

2. **Alterar regras de compatibilidade**: Modifique a função `configurar_geradores()` no script principal.

## Contato

Em caso de dúvidas ou necessidade de manutenção, entre em contato com a equipe de engenharia da Neosolar.


## Explicação da Solução

Desenvolvi uma solução completa para automatizar a configuração de geradores solares a partir dos componentes disponíveis no estoque. Vamos entender o que cada arquivo representa:

1. **Script Python (configurador_geradores.py)**: 
   - Este é o coração da solução que automatiza todo o processo
   - Lê os dados de produtos em estoque
   - Gera as combinações possíveis de geradores seguindo as regras de compatibilidade
   - Exporta os resultados para CSV e gera o e-mail para o time de marketing

2. **Arquivo de Produtos (produtos.json)**:
   - Contém os dados dos produtos disponíveis em estoque
   - Estruturado conforme o Anexo A fornecido

3. **Tabela de Geradores (geradores_configurados.csv)**:
   - Arquivo CSV contendo todos os geradores configurados
   - Formatado conforme o exemplo do Anexo C

4. **E-mail para Marketing (email_marketing.txt)**:
   - Conteúdo do e-mail a ser enviado para o time de marketing
   - Inclui o número de geradores configurados na semana

5. **Documentação do Desenvolvimento**:
   - Explica o funcionamento da solução
   - Fornece instruções para manutenção do código
   - Detalha a lógica e as possíveis extensões

### Detalhes da Implementação

O script segue uma lógica clara para configurar os geradores:

1. Carrega os produtos do arquivo JSON
2. Agrupa os produtos por categoria (painéis, inversores, controladores)
3. Para cada inversor, busca controladores compatíveis (mesma potência)
4. Para cada combinação inversor/controlador, verifica quais painéis podem ser usados
5. Calcula a quantidade necessária de painéis para atingir a potência desejada
6. Gera um ID único para cada gerador e adiciona os componentes
7. Exporta os resultados para CSV e gera o e-mail

Com esta solução, a Neosolar terá um processo automatizado e eficiente para configurar seus geradores solares semanalmente, reduzindo erros manuais e economizando tempo da equipe de engenharia.
