import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  doi,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Registrar componentes do Chart.js
ChartJS.register(
  CategoryScale, 
  LinearScale, 
  PointElement, 
  LineElement, 
  Title, 
  Tooltip, 
  Legend
);

function ResultChart({ results }) {
  if (!results || !results.results) {
    return null;
  }
  
  const { results: simulationResults } = results;
  
  // Criar dados para o gráfico
  const investmentTypes = Object.keys(simulationResults);
  
  // Cores para as linhas do gráfico (até 7 investimentos)
  const colors = [
    'rgb(75, 192, 192)',
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(255, 205, 86)',
    'rgb(201, 203, 207)'
  ];
  
  // Obter o máximo número de meses entre todas as simulações
  const maxMonths = Math.max(
    ...Object.values(simulationResults).map(
      data => data.simulation.evolution.length
    )
  );
  
  // Criar labels para os meses (ex: Mês 1, Mês 2, etc.)
  const labels = Array.from({ length: maxMonths }, (_, i) => `Mês ${i + 1}`);
  
  // Criar datasets para cada tipo de investimento
  const datasets = investmentTypes.map((type, index) => {
    const evolution = simulationResults[type].simulation.evolution;
    
    return {
      label: type,
      data: evolution.map(month => month.accumulated),
      borderColor: colors[index % colors.length],
      backgroundColor: colors[index % colors.length] + '20', // cor com transparência
      tension: 0.1
    };
  });
  
  const chartData = {
    labels,
    datasets
  };
  
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Evolução do Patrimônio ao Longo do Tempo'
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const value = context.raw;
            return `${context.dataset.label}: ${new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL'
            }).format(value)}`;
          }
        }
      }
    },
    scales: {
      y: {
        ticks: {
          callback: function(value) {
            return new Intl.NumberFormat('pt-BR', {
              style: 'currency',
              currency: 'BRL',
              maximumFractionDigits: 0
            }).format(value);
          }
        }
      }
    }
  };

  return (
    <div className="chart-container" style={{ height: '400px' }}>
      <Line data={chartData} options={chartOptions} />
    </div>
  );
}

export default ResultChart;