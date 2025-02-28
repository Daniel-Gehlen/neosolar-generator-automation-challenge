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
