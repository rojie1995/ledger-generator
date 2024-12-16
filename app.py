from flask import Flask, render_template, request, jsonify, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Ensure the static/Images directory exists
os.makedirs(os.path.join('static', 'Images'), exist_ok=True)

# Serve static files from the Images directory
@app.route('/static/Images/<path:filename>')
def serve_image(filename):
    return send_from_directory('Images', filename)

@app.route('/')
def index():
    return render_template('index.html')

class IncomeGenerator:
    MIN_DAILY = 1300
    MAX_DAILY = 4500
    
    @staticmethod
    def generate_daily_incomes(total_days, target_total):
        min_daily = IncomeGenerator.MIN_DAILY
        max_daily = IncomeGenerator.MAX_DAILY
        
        # Calculate average daily income
        average = target_total / total_days
        
        if average < min_daily or average > max_daily:
            return None
            
        daily_incomes = []
        remaining_total = target_total
        remaining_days = total_days
        used_numbers = set()
        
        # Generate random numbers that sum to target_total
        for day in range(total_days - 1):
            # Calculate safe min and max for this day
            min_value = max(min_daily, remaining_total - (max_daily * (remaining_days - 1)))
            max_value = min(max_daily, remaining_total - (min_daily * (remaining_days - 1)))
            
            if min_value > max_value:
                return None
            
            # Try to find a unique number
            attempts = 0
            while attempts < 100:
                income = random.randint(int(min_value), int(max_value))
                if income not in used_numbers:
                    break
                attempts += 1
            
            if attempts == 100:
                return None
                
            used_numbers.add(income)
            daily_incomes.append(income)
            remaining_total -= income
            remaining_days -= 1
        
        # Add the last day
        if min_daily <= remaining_total <= max_daily and remaining_total not in used_numbers:
            daily_incomes.append(remaining_total)
            return daily_incomes
        return None

    @staticmethod
    def calculate_limits(days):
        min_total = days * IncomeGenerator.MIN_DAILY
        max_total = days * IncomeGenerator.MAX_DAILY
        return min_total, max_total

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        month = int(data['month'])
        total_days = int(data['days'])
        target_total = int(data['total'])
        
        if month < 1 or month > 12:
            return jsonify({'error': 'Please select a valid month'}), 400
        
        if total_days <= 0:
            return jsonify({'error': 'Please enter a positive number of days'}), 400
            
        if target_total <= 0:
            return jsonify({'error': 'Please enter a positive total income'}), 400

        # Calculate valid range for the given days
        min_total, max_total = IncomeGenerator.calculate_limits(total_days)
        
        # Check if target_total is within valid range
        if target_total < min_total or target_total > max_total:
            return jsonify({
                'error': f'For {total_days} days, total income must be between:\n' +
                        f'Minimum: ₱{min_total:,} ({total_days} × ₱{IncomeGenerator.MIN_DAILY:,})\n' +
                        f'Maximum: ₱{max_total:,} ({total_days} × ₱{IncomeGenerator.MAX_DAILY:,})\n\n' +
                        f'Your input: ₱{target_total:,}\n\n' +
                        f'Suggestion: Try a total between ₱{min_total:,} and ₱{max_total:,}'
            }), 400

        # Generate daily incomes
        daily_incomes = IncomeGenerator.generate_daily_incomes(total_days, target_total)
        
        if daily_incomes is None:
            suggested_total = (total_days * (IncomeGenerator.MIN_DAILY + IncomeGenerator.MAX_DAILY)) // 2
            return jsonify({
                'error': f'Having trouble distributing ₱{target_total:,} across {total_days} days.\n\n' +
                        f'Suggestions:\n' +
                        f'1. Try a total closer to ₱{suggested_total:,}\n' +
                        f'2. Or try a different number of days\n' +
                        f'3. Each day must be between ₱{IncomeGenerator.MIN_DAILY:,} and ₱{IncomeGenerator.MAX_DAILY:,}'
            }), 400

        # Format the result
        result = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'month': month,
            'total_days': total_days,
            'target_total': target_total,
            'daily_incomes': [{'day': i+1, 'income': income} for i, income in enumerate(daily_incomes)],
            'actual_total': sum(daily_incomes)
        }
        
        return jsonify(result)

    except ValueError:
        return jsonify({'error': 'Please enter valid numbers'}), 400

if __name__ == '__main__':
    # Use environment variable for port if available (for production)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
