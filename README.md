# FarmTech Solutions - Aplicação Web (Django)

Aplicação web em Django que reúne, em um único lugar, o que antes estava
separado em três arquivos:

- `Projeto_1_FarmTechSolutions` (Python/terminal) → virou o CRUD de culturas
  (Entrada, Saída, Atualização e Deleção de Dados), agora com banco de dados
  (SQLite) em vez de CSV.
- `Estatistica_Farm_Tech.R` → virou a página **/estatisticas/**, calculando
  média e desvio padrão de área e ruas com a biblioteca `statistics` do Python.
- `Clima_API.R` → virou a página **/clima/**, que consulta a API pública
  Open-Meteo via AJAX (JavaScript) e mostra o resultado sem recarregar a página.

## Como rodar

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate     (Windows)
   source venv/bin/activate  (Linux/Mac)
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Crie as tabelas do banco de dados:
   ```
   python manage.py migrate
   ```

4. Rode o servidor:
   ```
   python manage.py runserver
   ```

5. Acesse no navegador: http://127.0.0.1:8000/

## Estrutura

```
farmtech_web/
├── manage.py
├── requirements.txt
├── farmtech_web/        (configurações do projeto)
└── culturas/             (app principal)
    ├── models.py         (modelo Cultura)
    ├── views.py           (CRUD + estatísticas + clima)
    ├── urls.py
    ├── templates/culturas/
    └── static/culturas/{css,js}
```
