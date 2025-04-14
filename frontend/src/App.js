import React, { useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import SimulationForm from "./components/SimulationForm";
import ResultCards from "./components/ResultCards";
import ResultChart from "./components/ResultChart";
import ResultTable from "./components/ResultTable";
import useSimulator from "./hooks/useSimulator";

function App() {
  const [activeTab, setActiveTab] = useState("direct"); // 'direct' ou 'inverse'
  const { loading, results, error, runDirectSimulation, runInverseSimulation } =
    useSimulator();

  const handleSubmit = (formData) => {
    if (activeTab === "direct") {
      runDirectSimulation(formData);
    } else {
      runInverseSimulation(formData);
    }
  };

  return (
    <div className="app">
      <Header />

      <main className="container py-4">
        <div className="row">
          <div className="col-lg-4 mb-4">
            <div className="card shadow-sm">
              <div className="card-body">
                <ul className="nav nav-tabs mb-3">
                  <li className="nav-item">
                    <button
                      className={`nav-link ${
                        activeTab === "direct" ? "active" : ""
                      }`}
                      onClick={() => setActiveTab("direct")}
                    >
                      Quanto vou ganhar?
                    </button>
                  </li>
                  <li className="nav-item">
                    <button
                      className={`nav-link ${
                        activeTab === "inverse" ? "active" : ""
                      }`}
                      onClick={() => setActiveTab("inverse")}
                    >
                      Quanto preciso investir?
                    </button>
                  </li>
                </ul>

                <SimulationForm formType={activeTab} onSubmit={handleSubmit} />
              </div>
            </div>
          </div>

          <div className="col-lg-8">
            {error && <div className="alert alert-danger">{error}</div>}

            {loading && (
              <div className="d-flex justify-content-center my-5">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Carregando...</span>
                </div>
              </div>
            )}

            {!loading && results && (
              <>
                <ResultCards results={results} formType={activeTab} />

                <div className="card shadow-sm mb-4">
                  <div className="card-body">
                    <h5 className="card-title">Comparativo de Rentabilidade</h5>
                    <ResultChart results={results} />
                  </div>
                </div>

                <div className="card shadow-sm">
                  <div className="card-body">
                    <h5 className="card-title">Detalhes da Simulação</h5>
                    <ResultTable results={results} formType={activeTab} />
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;
