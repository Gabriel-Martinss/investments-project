import React from 'react';

function Header() {
  return (
    <header className="bg-primary text-white py-4">
      <div className="container">
        <div className="row align-items-center">
          <div className="col">
            <h1 className="mb-0">Simulador de Investimentos</h1>
            <p className="lead mb-0">Compare rentabilidades e planeje seu futuro financeiro</p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;