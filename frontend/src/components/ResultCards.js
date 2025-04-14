import React from 'react';

function ResultCards({ results, formType }) {
  if (!results || !results.results) {
    return null;
  }
  
  const { results: simulationResults } = results;
  const investmentEntries = Object.entries(simulationResults);
  
  // Ordenar resultados do melhor para o pior em termos de retorno percentual
  const sortedResults = investmentEntries.sort((a, b) => {
    if (formType === 'direct') {
      return b[1].simulation.percentage_return - a[1].simulation.percentage_return;
    } else {
      // Para o fluxo inverso, ordena do menor investimento necessário para o maior
      return a[1].simulation.initial_principal - b[1].simulation.initial_principal;
    }
  });

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  return (
    <div className="mb-4">
      <h4 className="mb-3">Resultados da Simulação</h4>
      <div className="row">
        {sortedResults.map(([investmentType, data]) => {
          const { simulation, investment_info, tax_info } = data;
          
          return (
            <div className="col-md-6 col-lg-4 mb-3" key={investmentType}>
              <div className="card h-100 shadow-sm">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{investmentType}</h5>
                </div>
                <div className="card-body">
                  {formType === 'direct' ? (
                    // Resultados para fluxo direto
                    <>
                      <div className="mb-2">
                        <small className="text-muted">Montante Final Bruto</small>
                        <div className="fw-bold fs-5">{formatCurrency(simulation.final_gross_amount)}</div>
                      </div>
                      <div className="mb-2">
                        <small className="text-muted">Rendimento Líquido</small>
                        <div className="fw-bold fs-5 text-success">
                          +{formatCurrency(simulation.net_profit)}
                        </div>
                        <div className="badge bg-success">
                          +{simulation.percentage_return.toFixed(2)}%
                        </div>
                      </div>
                      <div className="mb-2">
                        <small className="text-muted">Renda Mensal Estimada</small>
                        <div className="fw-bold">{formatCurrency(simulation.monthly_net_income)}</div>
                      </div>
                    </>
                  ) : (
                    // Resultados para fluxo inverso
                    <>
                      <div className="mb-2">
                        <small className="text-muted">Investimento Inicial Necessário</small>
                        <div className="fw-bold fs-5">{formatCurrency(simulation.initial_principal)}</div>
                      </div>
                      <div className="mb-2">
                        <small className="text-muted">Principal Total Necessário</small>
                        <div className="fw-bold">{formatCurrency(simulation.required_principal)}</div>
                      </div>
                      <div className="mb-2">
                        <small className="text-muted">Renda Mensal</small>
                        <div className="fw-bold text-success">
                          {formatCurrency(results.input.desired_monthly_income)}
                        </div>
                      </div>
                    </>
                  )}
                  <hr />
                  <div className="small">
                    <div className="mb-1">
                      <span className="text-muted">Taxa:</span> {(investment_info.annual_rate * 100).toFixed(2)}% a.a.
                    </div>
                    <div className="mb-1">
                      <span className="text-muted">IR:</span> {tax_info.tax_exempt ? 'Isento' : `${(simulation.tax_rate * 100).toFixed(1)}%`}
                    </div>
                    <div>
                      <span className="text-muted">Referência:</span> {investment_info.percentage_of_reference}% do {investment_info.reference}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ResultCards;