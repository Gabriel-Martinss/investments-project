import React from 'react';

function Footer() {
  return (
    <footer className="bg-light py-4 mt-4">
      <div className="container">
        <div className="row">
          <div className="col text-center">
            <p className="mb-0">© {new Date().getFullYear()} Simulador de Investimentos</p>
            <p className="text-muted small mb-0">
              Este simulador é apenas uma ferramenta educacional. Consulte um profissional financeiro antes de tomar decisões.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;