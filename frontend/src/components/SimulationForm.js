import React, { useState, useEffect } from 'react';
import api from '../services/api';

function SimulationForm({ formType, onSubmit }) {
  const [investments, setInvestments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    // Formulário direto
    principal: 10000,
    monthly_contribution: 500,
    term_months: 12,
    
    // Formulário inverso
    desired_monthly_income: 2000,
    
    // Comum
    investment_types: []
  });

  useEffect(() => {
    const fetchInvestments = async () => {
      try {
        const response = await api.getInvestmentRates();
        setInvestments(Object.values(response.data));
        
        // Seleciona os 4 primeiros investimentos por padrão
        const defaultSelected = Object.keys(response.data).slice(0, 4);
        setFormData(prev => ({
          ...prev,
          investment_types: defaultSelected
        }));
        
        setLoading(false);
      } catch (error) {
        console.error('Erro ao buscar investimentos:', error);
        setLoading(false);
      }
    };
    
    fetchInvestments();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      // Para checkboxes de tipos de investimento
      if (checked) {
        setFormData(prev => ({
          ...prev,
          investment_types: [...prev.investment_types, name]
        }));
      } else {
        setFormData(prev => ({
          ...prev,
          investment_types: prev.investment_types.filter(type => type !== name)
        }));
      }
    } else {
      // Para inputs numéricos
      setFormData(prev => ({
        ...prev,
        [name]: type === 'number' ? parseFloat(value) : value
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (loading) {
    return <div>Carregando opções de investimento...</div>;
  }

  return (
    <form onSubmit={handleSubmit}>
      {formType === 'direct' ? (
        // Formulário direto: "Quanto vou ganhar?"
        <>
          <div className="mb-3">
            <label htmlFor="principal" className="form-label">Valor Inicial (R$)</label>
            <input
              type="number"
              className="form-control"
              id="principal"
              name="principal"
              min="0"
              step="100"
              value={formData.principal}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="mb-3">
            <label htmlFor="monthly_contribution" className="form-label">Aporte Mensal (R$)</label>
            <input
              type="number"
              className="form-control"
              id="monthly_contribution"
              name="monthly_contribution"
              min="0"
              step="50"
              value={formData.monthly_contribution}
              onChange={handleChange}
            />
          </div>
        </>
      ) : (
        // Formulário inverso: "Quanto preciso investir?"
        <div className="mb-3">
          <label htmlFor="desired_monthly_income" className="form-label">Renda Mensal Desejada (R$)</label>
          <input
            type="number"
            className="form-control"
            id="desired_monthly_income"
            name="desired_monthly_income"
            min="100"
            step="100"
            value={formData.desired_monthly_income}
            onChange={handleChange}
            required
          />
        </div>
      )}
      
      {/* Campos comuns a ambos formulários */}
      <div className="mb-3">
        <label htmlFor="term_months" className="form-label">Prazo de Investimento</label>
        <select
          className="form-select"
          id="term_months"
          name="term_months"
          value={formData.term_months}
          onChange={handleChange}
          required
        >
          <option value="6">6 meses</option>
          <option value="12">1 ano</option>
          <option value="24">2 anos</option>
          <option value="36">3 anos</option>
          <option value="60">5 anos</option>
          <option value="120">10 anos</option>
          <option value="240">20 anos</option>
        </select>
      </div>
      
      <div className="mb-4">
        <label className="form-label d-block">Tipos de Investimento</label>
        <div className="row">
          {investments.map((investment) => (
            <div className="col-6 mb-2" key={investment.name}>
              <div className="form-check">
                <input
                  className="form-check-input"
                  type="checkbox"
                  name={investment.name}
                  id={`check-${investment.name}`}
                  checked={formData.investment_types.includes(investment.name)}
                  onChange={handleChange}
                />
                <label className="form-check-label" htmlFor={`check-${investment.name}`}>
                  {investment.name}
                </label>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <button type="submit" className="btn btn-primary w-100">
        {formType === 'direct' ? 'Calcular Rendimentos' : 'Calcular Investimento Necessário'}
      </button>
    </form>
  );
}

export default SimulationForm;