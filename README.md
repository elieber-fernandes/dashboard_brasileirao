
# Dashboard Brasileirão 2023

Este projeto coleta dados do Campeonato Brasileiro Série A 2023 usando a API Football API Sports, salva em arquivos CSV e exibe um dashboard interativo com Streamlit.

## Funcionalidades

- Coleta automática de jogos, classificação e artilharia do Brasileirão 2023
- Geração de arquivos CSV para análise
- Dashboard interativo com:
  - Tabela de classificação
  - Top 10 artilheiros
  - Jogos por time e por data
  - Gráficos de pontos, saldo de gols e artilharia
  - Destaque para maior goleada
  - Filtros interativos e download dos dados

## Configuração da chave da API

### 1. Usando um arquivo `.env` (recomendado)

1. Crie um arquivo chamado `.env` na raiz do projeto.
2. Adicione a seguinte linha ao arquivo, substituindo pelo valor da sua chave:
   ```
   API_KEY=sua_chave_aqui
   ```
3. O código já está preparado para carregar automaticamente essa variável.

### 2. Usando variável de ambiente no sistema

No terminal, antes de rodar o script, defina a variável:

- **Windows:**
  ```
  set API_KEY=sua_chave_aqui
  ```
- **Linux/Mac:**
  ```
  export API_KEY=sua_chave_aqui
  ```

Depois, execute normalmente:
```
python main.py
```
ou
```
streamlit run main.py
```

