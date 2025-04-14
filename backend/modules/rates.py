def get_current_rates():
    '''
    Retorna as taxas de referência atuais (CDI, SELIC, Poupança)
    Em um cenário real, estas taxas seriam obtidas de uma API externa ou banco de dados
    
    Returns:
        dict: taxas de referência atuais
    '''
    # Valores fictícios para demonstração
    annual_cdi = 0.1175  # 11.75% ao ano
    annual_selic = 0.1175  # 11.75% ao ano
    annual_poupanca = 0.0817  # 8.17% ao ano (70% da Selic quando esta é maior que 8.5% ao ano)
    
    # Conversão para taxas mensais aproximadas 
    # Taxa mensal = (1 + taxa anual)^(1/12) - 1
    monthly_cdi = (1 + annual_cdi) ** (1/12) - 1
    monthly_selic = (1 + annual_selic) ** (1/12) - 1
    monthly_poupanca = (1 + annual_poupanca) ** (1/12) - 1
    
    return {
        'cdi': {
            'annual': annual_cdi,
            'monthly': monthly_cdi,
            'annual_percentage': annual_cdi * 100,
            'monthly_percentage': monthly_cdi * 100
        },
        'selic': {
            'annual': annual_selic,
            'monthly': monthly_selic,
            'annual_percentage': annual_selic * 100,
            'monthly_percentage': monthly_selic * 100
        },
        'poupanca': {
            'annual': annual_poupanca,
            'monthly': monthly_poupanca,
            'annual_percentage': annual_poupanca * 100,
            'monthly_percentage': monthly_poupanca * 100
        }
    }

def get_investment_rates():
    '''
    Retorna as taxas de referência para diferentes tipos de investimentos
    
    Returns:
        dict: tipos de investimento e suas taxas
    '''
    current_rates = get_current_rates()
    
    return {
        'Poupança': {
            'name': 'Poupança',
            'annual_rate': current_rates['poupanca']['annual'],
            'monthly_rate': current_rates['poupanca']['monthly'],
            'reference': 'Rendimento fixo da poupança',
            'percentage_of_reference': 100,
            'tax_exempt': True,
            'liquidity': 'Alta (D+0 após aniversário)',
            'risk': 'Muito baixo'
        },
        'CDB 100% CDI': {
            'name': 'CDB 100% CDI',
            'annual_rate': current_rates['cdi']['annual'],
            'monthly_rate': current_rates['cdi']['monthly'],
            'reference': 'CDI',
            'percentage_of_reference': 100,
            'tax_exempt': False,
            'liquidity': 'Média (conforme contrato)',
            'risk': 'Baixo'
        },
        'CDB 110% CDI': {
            'name': 'CDB 110% CDI',
            'annual_rate': current_rates['cdi']['annual'] * 1.10,
            'monthly_rate': ((1 + current_rates['cdi']['annual'] * 1.10) ** (1/12)) - 1,
            'reference': 'CDI',
            'percentage_of_reference': 110,
            'tax_exempt': False,
            'liquidity': 'Média (conforme contrato)',
            'risk': 'Baixo'
        },
        'LCI 95% CDI': {
            'name': 'LCI 95% CDI',
            'annual_rate': current_rates['cdi']['annual'] * 0.95,
            'monthly_rate': ((1 + current_rates['cdi']['annual'] * 0.95) ** (1/12)) - 1,
            'reference': 'CDI',
            'percentage_of_reference': 95,
            'tax_exempt': True,
            'liquidity': 'Baixa (carência mínima)',
            'risk': 'Baixo'
        },
        'LCA 98% CDI': {
            'name': 'LCA 98% CDI',
            'annual_rate': current_rates['cdi']['annual'] * 0.98,
            'monthly_rate': ((1 + current_rates['cdi']['annual'] * 0.98) ** (1/12)) - 1,
            'reference': 'CDI',
            'percentage_of_reference': 98,
            'tax_exempt': True,
            'liquidity': 'Baixa (carência mínima)',
            'risk': 'Baixo'
        },
        'Tesouro SELIC': {
            'name': 'Tesouro SELIC',
            'annual_rate': current_rates['selic']['annual'],
            'monthly_rate': current_rates['selic']['monthly'],
            'reference': 'SELIC',
            'percentage_of_reference': 100,
            'tax_exempt': False,
            'liquidity': 'Alta (D+1 com deságio)',
            'risk': 'Muito baixo'
        },
        'Tesouro Prefixado': {
            'name': 'Tesouro Prefixado',
            'annual_rate': 0.1025,  # Exemplo: 10.25% ao ano
            'monthly_rate': (1 + 0.1025) ** (1/12) - 1,
            'reference': 'Taxa prefixada',
            'percentage_of_reference': 100,
            'tax_exempt': False,
            'liquidity': 'Alta (D+1 com deságio)',
            'risk': 'Baixo'
        },
        'Tesouro IPCA+': {
            'name': 'Tesouro IPCA+',
            'annual_rate': 0.06,  # Exemplo: IPCA + 6% ao ano
            'monthly_rate': (1 + 0.06) ** (1/12) - 1,  # Apenas o juro real, sem inflação
            'reference': 'IPCA + taxa real',
            'percentage_of_reference': 100,
            'tax_exempt': False,
            'liquidity': 'Alta (D+1 com deságio)',
            'risk': 'Baixo',
            'obs': 'Taxa real sem considerar inflação'
        }
    }