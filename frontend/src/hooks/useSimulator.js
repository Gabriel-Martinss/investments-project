import { useState } from 'react';
import api from '../services/api';

function useSimulator() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  
  const runDirectSimulation = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.runDirectSimulation(formData);
      setResults(response.data);
    } catch (err) {
      console.error('Erro na simulação direta:', err);
      setError('Ocorreu um erro ao processar a simulação. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };
  
  const runInverseSimulation = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await api.runInverseSimulation(formData);
      setResults(response.data);
    } catch (err) {
      console.error('Erro na simulação inversa:', err);
      setError('Ocorreu um erro ao processar a simulação. Por favor, tente novamente.');
    } finally {
      setLoading(false);
    }
  };
  
  return {
    loading,
    results,
    error,
    runDirectSimulation,
    runInverseSimulation
  };
}

export default useSimulator;

