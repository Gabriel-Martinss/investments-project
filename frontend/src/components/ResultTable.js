import React, { useState } from "react";

function ResultTable({ results, formType }) {
  const [selectedInvestment, setSelectedInvestment] = useState(null);

  if (!results || !results.results) {
    return null;
  }

  const { results: simulationResults } = results;
  const investmentTypes = Object.keys(simulationResults);

  // Se nenhum investimento estiver selecionado, seleciona o primeiro
  if (!selectedInvestment && investmentTypes.length > 0) {
    setSelectedInvestment(investmentTypes[0]);
  }

  if (!selectedInvestment) {
    return null;
  }

  const selectedData = simulationResults[selectedInvestment];
  const { evolution } = selectedData.simulation;

  const formatCurrency = (value) => {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(value);
  };

  return (
    <div>
      <div className="mb-3">
        <label className="form-label">
          Selecione o investimento para ver detalhes:
        </label>
        <select
          className="form-select"
          value={selectedInvestment}
          onChange={(e) => setSelectedInvestment(e.target.value)}
        >
          {investmentTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-hover table-sm">
          <thead>
            <tr>
              <th>Mês</th>
              <th>Data</th>
              <th>Saldo Acumulado</th>
              <th>Rendimento</th>
              <th>Aporte</th>
            </tr>
          </thead>
          <tbody>
            {evolution.map((month) => (
              <tr key={month.month}>
                <td>{month.month}</td>
                <td>
                  {month.month_name}/{month.year}
                </td>
                <td>{formatCurrency(month.accumulated)}</td>
                <td>{formatCurrency(month.interest)}</td>
                <td>
                  {month.month === 1
                    ? formatCurrency(results.input.principal)
                    : formatCurrency(month.contribution)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ResultTable;
