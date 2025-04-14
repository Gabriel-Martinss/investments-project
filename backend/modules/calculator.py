import numpy as np
from modules.taxes import calculate_income_tax
from datetime import datetime, timedelta
import calendar

def get_days_in_month(year, month):
    '''Retorna o número de dias em um mês específico'''
    return calendar.monthrange(year, month)[1]

def calculate_monthly_income(principal, monthly_rate, term_months):
    '''Calcula a renda mensal que pode ser gerada por um principal'''
    # Retorna apenas os juros sem amortizar o principal
    return principal * monthly_rate

def calculate_required_principal(desired_income, monthly_rate):
    '''Calcula o principal necessário para gerar uma renda desejada'''
    if monthly_rate <= 0:
        return float('inf')  # Evitar divisão por zero
    return desired_income / monthly_rate

def calculate_compound_interest(principal, monthly_rate, term_months, monthly_contribution=0):
    '''
    Calcula juros compostos com aportes mensais
    
    Args:
        principal: valor inicial
        monthly_rate: taxa mensal (ex: 0.01 para 1%)
        term_months: prazo em meses
        monthly_contribution: aporte mensal
    
    Returns:
        dict com resultados da simulação
    '''
    result = []
    accumulated = principal
    total_invested = principal
    
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    for month_index in range(term_months):
        # Incrementa o mês
        month += 1
        if month > 12:
            month = 1
            year += 1
            
        # Calcula os juros do mês
        interest = accumulated * monthly_rate
        
        # Adiciona o aporte mensal (ocorre após o cálculo de juros)
        accumulated += interest + monthly_contribution
        
        # Atualiza total investido
        if month_index > 0:  # Não considera o principal como aporte
            total_invested += monthly_contribution
        
        # Armazena resultado mensal
        result.append({
            'month': month_index + 1,
            'year': year,
            'month_name': calendar.month_name[month],
            'accumulated': accumulated,
            'interest': interest,
            'contribution': monthly_contribution if month_index > 0 else principal,
            'total_invested': total_invested
        })
    
    return result

def simulate_investment(principal, monthly_contribution, monthly_rate, term_months, tax_rate=None, tax_exempt=False):
    '''
    Simula um investimento completo
    
    Args:
        principal: valor inicial
        monthly_contribution: aporte mensal
        monthly_rate: taxa mensal de juros
        term_months: prazo em meses
        tax_rate: alíquota de IR (0 a 1) ou None para cálculo automático
        tax_exempt: True se o investimento é isento de IR
        
    Returns:
        dict com resultados detalhados da simulação
    '''
    evolution = calculate_compound_interest(principal, monthly_rate, term_months, monthly_contribution)
    
    final_amount = evolution[-1]['accumulated']
    total_invested = evolution[-1]['total_invested']
    gross_profit = final_amount - total_invested
    
    # Cálculo do IR
    if tax_exempt:
        tax_amount = 0
    else:
        if tax_rate is None:
            tax_rate = calculate_income_tax(term_months)
        tax_amount = gross_profit * tax_rate
    
    net_profit = gross_profit - tax_amount
    net_amount = final_amount - tax_amount
    
    # Renda mensal estimada (considerando a mesma taxa de juros)
    monthly_income = calculate_monthly_income(final_amount, monthly_rate)
    monthly_income_after_tax = monthly_income * (1 - (0 if tax_exempt else tax_rate))
    
    # Rendimento percentual
    percentage_return = (net_amount / total_invested - 1) * 100 if total_invested > 0 else 0
    
    return {
        'initial_principal': principal,
        'monthly_contribution': monthly_contribution,
        'term_months': term_months,
        'final_gross_amount': final_amount,
        'total_invested': total_invested,
        'gross_profit': gross_profit,
        'tax_rate': 0 if tax_exempt else tax_rate,
        'tax_amount': tax_amount,
        'net_profit': net_profit,
        'net_amount': net_amount,
        'monthly_gross_income': monthly_income,
        'monthly_net_income': monthly_income_after_tax,
        'percentage_return': percentage_return,
        'annual_return_rate': (1 + monthly_rate) ** 12 - 1,
        'evolution': evolution
    }

def inverse_simulation(desired_monthly_income, monthly_rate, term_months, monthly_contribution=0, tax_rate=None, tax_exempt=False):
    '''
    Calcula o principal necessário para gerar uma renda desejada
    
    Args:
        desired_monthly_income: renda mensal desejada líquida
        monthly_rate: taxa mensal de juros
        term_months: prazo para acumular o valor
        monthly_contribution: aporte mensal
        tax_rate: alíquota de IR (0 a 1)
        tax_exempt: True se o investimento é isento de IR
        
    Returns:
        dict com resultados detalhados da simulação
    '''
    # Se for isento de IR, a renda bruta necessária é igual à desejada
    # Caso contrário, precisamos de uma renda bruta maior para compensar o IR
    if tax_exempt:
        required_gross_income = desired_monthly_income
    else:
        if tax_rate is None:
            tax_rate = calculate_income_tax(term_months)
        # Fórmula: renda_líquida = renda_bruta * (1 - taxa_ir)
        # Portanto: renda_bruta = renda_líquida / (1 - taxa_ir)
        required_gross_income = desired_monthly_income / (1 - tax_rate)
    
    # Principal necessário para gerar a renda bruta
    required_principal = calculate_required_principal(required_gross_income, monthly_rate)
    
    # Agora precisamos calcular quanto precisamos investir agora + aportes mensais
    # para chegar ao principal necessário
    if monthly_contribution <= 0:
        # Se não houver aportes mensais, o principal inicial é o mesmo que o requerido
        initial_principal = required_principal
    else:
        # Caso contrário, precisamos calcular quanto deve ser o principal inicial
        # para que, com os aportes mensais, chegue ao principal necessário
        
        # Fator de juros para valor futuro de uma série de pagamentos
        fv_factor = ((1 + monthly_rate) ** term_months - 1) / monthly_rate
        
        # Quanto do principal necessário será coberto pelos aportes mensais
        contribution_portion = monthly_contribution * fv_factor
        
        # O restante precisa vir do principal inicial
        initial_principal = required_principal / ((1 + monthly_rate) ** term_months) if term_months > 0 else required_principal
        
        # Se os aportes forem suficientes, o principal inicial pode ser zero
        initial_principal = max(0, initial_principal)
    
    # Simula o investimento para obter detalhes completos
    return {
        'desired_monthly_income': desired_monthly_income,
        'required_gross_income': required_gross_income,
        'required_principal': required_principal,
        'initial_principal': initial_principal,
        'monthly_contribution': monthly_contribution,
        'simulation': simulate_investment(initial_principal, monthly_contribution, monthly_rate, term_months, tax_rate, tax_exempt)
    }