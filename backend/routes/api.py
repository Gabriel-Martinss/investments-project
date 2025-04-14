from flask import Blueprint, request, jsonify
from modules.calculator import simulate_investment, inverse_simulation
from modules.rates import get_current_rates, get_investment_rates
from modules.taxes import get_investment_tax_info, calculate_income_tax

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API online'}), 200

@api_bp.route('/rates/current', methods=['GET'])
def get_rates():
    '''Retorna as taxas de referência atuais'''
    try:
        rates = get_current_rates()
        return jsonify(rates), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/rates/investments', methods=['GET'])
def get_investments():
    '''Retorna as taxas para diferentes investimentos'''
    try:
        investments = get_investment_rates()
        return jsonify(investments), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/simulate/direct', methods=['POST'])
def direct_simulation():
    '''
    Simula quanto o usuário vai ganhar investindo um valor inicial
    
    Parâmetros esperados no JSON:
    - principal: valor inicial
    - monthly_contribution: aporte mensal (opcional)
    - term_months: prazo em meses
    - investment_types: lista de tipos de investimento para simular
    '''
    try:
        data = request.json
        
        # Validação básica
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        principal = float(data.get('principal', 0))
        monthly_contribution = float(data.get('monthly_contribution', 0))
        term_months = int(data.get('term_months', 12))
        investment_types = data.get('investment_types', [])
        
        # Se nenhum tipo de investimento especificado, use todos
        if not investment_types:
            investment_rates = get_investment_rates()
            investment_types = list(investment_rates.keys())
        
        results = {}
        
        # Simular para cada tipo de investimento
        for inv_type in investment_types:
            investment_info = get_investment_rates().get(inv_type)
            
            if not investment_info:
                continue
                
            tax_info = get_investment_tax_info(inv_type)
            tax_exempt = tax_info.get('tax_exempt', False)
            tax_rate = None if not tax_exempt else 0
            
            simulation = simulate_investment(
                principal=principal,
                monthly_contribution=monthly_contribution,
                monthly_rate=investment_info['monthly_rate'],
                term_months=term_months,
                tax_rate=tax_rate,
                tax_exempt=tax_exempt
            )
            
            results[inv_type] = {
                'investment_info': investment_info,
                'tax_info': tax_info,
                'simulation': simulation
            }
            
        return jsonify({
            'input': {
                'principal': principal,
                'monthly_contribution': monthly_contribution,
                'term_months': term_months
            },
            'results': results
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/simulate/inverse', methods=['POST'])
def inverse_simulation_route():
    '''
    Simula quanto o usuário precisa investir para obter uma renda mensal desejada
    
    Parâmetros esperados no JSON:
    - desired_monthly_income: renda mensal desejada 
    - term_months: prazo em meses para acumular o capital
    - monthly_contribution: aporte mensal (opcional)
    - investment_types: lista de tipos de investimento para simular
    '''
    try:
        data = request.json
        
        # Validação básica
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
            
        desired_monthly_income = float(data.get('desired_monthly_income', 0))
        monthly_contribution = float(data.get('monthly_contribution', 0))
        term_months = int(data.get('term_months', 12))
        investment_types = data.get('investment_types', [])
        
        # Se nenhum tipo de investimento especificado, use todos
        if not investment_types:
            investment_rates = get_investment_rates()
            investment_types = list(investment_rates.keys())
        
        results = {}
        
        # Simular para cada tipo de investimento
        for inv_type in investment_types:
            investment_info = get_investment_rates().get(inv_type)
            
            if not investment_info:
                continue
                
            tax_info = get_investment_tax_info(inv_type)
            tax_exempt = tax_info.get('tax_exempt', False)
            tax_rate = None if not tax_exempt else 0
            
            simulation = inverse_simulation(
                desired_monthly_income=desired_monthly_income,
                monthly_contribution=monthly_contribution,
                monthly_rate=investment_info['monthly_rate'],
                term_months=term_months,
                tax_rate=tax_rate,
                tax_exempt=tax_exempt
            )
            
            results[inv_type] = {
                'investment_info': investment_info,
                'tax_info': tax_info,
                'simulation': simulation
            }
            
        return jsonify({
            'input': {
                'desired_monthly_income': desired_monthly_income,
                'monthly_contribution': monthly_contribution,
                'term_months': term_months
            },
            'results': results
        }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500