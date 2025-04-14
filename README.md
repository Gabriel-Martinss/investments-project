# Simulador de Investimentos

Este é um aplicativo web completo para simulação de investimentos, desenvolvido com Python/Flask no backend e React no frontend. O sistema permite realizar dois tipos de simulações financeiras:

1. **Fluxo Direto**: Calcular quanto você vai ganhar a partir de um determinado investimento inicial e/ou aportes mensais.
2. **Fluxo Inverso**: Calcular quanto você precisa investir para atingir uma renda mensal desejada.

## Recursos

- Comparação entre diversos produtos financeiros (Poupança, CDB, LCI, LCA, Tesouro Direto, etc.)
- Cálculos precisos considerando juros compostos e tributação (IR)
- Visualização gráfica da evolução do patrimônio
- Interface responsiva para desktop e dispositivos móveis
- Tabelas detalhadas com evolução mês a mês

## Tecnologias Utilizadas

### Backend
- Python 3.9+
- Flask (framework web)
- Flask-CORS (para permitir requisições cross-origin)
- NumPy (para cálculos numéricos)

### Frontend
- React 18
- Chart.js (para visualização de gráficos)
- Bootstrap 5 (para estilos e layout)
- Axios (para requisições HTTP)

## Estrutura do Projeto

```
/investment-simulator/
├── backend/                 # Código Python/Flask
│   ├── app.py               # Ponto de entrada da aplicação Flask
│   ├── config.py            # Configurações da aplicação
│   ├── requirements.txt     # Dependências Python
│   ├── modules/             # Módulos para cálculos e regras de negócio
│   └── routes/              # Rotas da API
├── frontend/                # Código React
│   ├── public/              # Arquivos estáticos
│   ├── src/                 # Código fonte React
│   │   ├── components/      # Componentes React
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # Serviços de API
│   │   └── styles/          # Estilos CSS
│   ├── package.json         # Dependências NPM
│   └── README.md            # Documentação do frontend
└── README.md                # Este arquivo
```

## Instalação e Execução

### Pré-requisitos
- Python 3.9+
- Node.js 14+
- npm ou yarn

### Backend

1. Navegue até a pasta do backend:
   ```
   cd backend
   ```

2. Crie e ative um ambiente virtual:
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Execute o servidor Flask:
   ```
   python app.py
   ```

   O servidor estará rodando em `http://localhost:5000`

### Frontend

1. Em outro terminal, navegue até a pasta do frontend:
   ```
   cd frontend
   ```

2. Instale as dependências:
   ```
   npm install
   # ou
   yarn install
   ```

3. Inicie o servidor de desenvolvimento:
   ```
   npm start
   # ou
   yarn start
   ```

   O frontend estará disponível em `http://localhost:3000`

## Uso da API

O backend expõe os seguintes endpoints:

- `GET /api/rates/current` - Retorna as taxas de referência atuais (CDI, SELIC, etc.)
- `GET /api/rates/investments` - Retorna informações sobre diferentes tipos de investimentos
- `POST /api/simulate/direct` - Realiza uma simulação direta (quanto vai ganhar)
- `POST /api/simulate/inverse` - Realiza uma simulação inversa (quanto precisa investir)

### Exemplos de Requisições

#### Simulação Direta
```json
POST /api/simulate/direct
{
  "principal": 10000,
  "monthly_contribution": 500,
  "term_months": 12,
  "investment_types": ["Poupança", "CDB 100% CDI", "Tesouro SELIC"]
}
```

#### Simulação Inversa
```json
POST /api/simulate/inverse
{
  "desired_monthly_income": 2000,
  "monthly_contribution": 500,
  "term_months": 60,
  "investment_types": ["Poupança", "CDB 100% CDI", "Tesouro SELIC"]
}
```

## Considerações Finais

Este projeto foi desenvolvido para fins educacionais. Os cálculos realizados são aproximações e podem não refletir exatamente todos os custos, taxas e impostos envolvidos em investimentos reais. Sempre consulte um profissional financeiro antes de tomar decisões de investimento.

## Melhorias Futuras

- Adicionar autenticação de usuários
- Permitir salvar simulações para comparações futuras
- Adicionar mais tipos de investimentos (ações, FIIs, etc.)
- Incluir inflação nos cálculos
- Adicionar taxas administrativas de corretoras e bancos
