def calculate_income_tax(term_months):
    '''
    Calcula a alíquota de imposto de renda baseada na tabela regressiva para investimentos de renda fixa
    
    Args:
        term_months: prazo do investimento em meses
    
    Returns:
        float: alíquota de IR (de 0 a 1)
    '''
    # Tabela regressiva de IR para renda fixa
    if term_months <= 6:
        return 0.225    # 22.5% para aplicações até 180 dias
    elif term_months <= 12:
        return 0.20     # 20% para aplicações de 181 a 360 dias
    elif term_months <= 24:
        return 0.175    # 17.5% para aplicações de 361 a 720 dias
    else:
        return 0.15     # 15% para aplicações acima de 720 dias

def get_investment_tax_info(investment_type):
    '''
    Retorna informações sobre impostos para diferentes tipos de investimento
    
    Args:
        investment_type: string com o tipo de investimento (CDB, LCI, etc)
        
    Returns:
        dict: informações sobre impostos para o tipo de investimento
    '''
    tax_exempt_investments = ['LCI', 'LCA', 'Poupança']
    
    return {
        'tax_exempt': investment_type in tax_exempt_investments,
        'has_iof': investment_type not in ['Poupança'] + tax_exempt_investments,
        'description': 'Isento de IR' if investment_type in tax_exempt_investments else 'Sujeito à tabela regressiva de IR'
    }