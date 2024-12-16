from flask import Flask, render_template, request, jsonify, send_from_directory
import random
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        month = int(data.get('month', 1))
        total_days = int(data.get('days', 30))
        target_total = float(data.get('total', 0))
        
        if month < 1 or month > 12:
            return jsonify({'error': 'Please select a valid month'}), 400
        if total_days < 1 or total_days > 31:
            return jsonify({'error': 'Days must be between 1 and 31'}), 400
        if target_total <= 0:
            return jsonify({'error': 'Total must be greater than 0'}), 400

        daily_incomes = []
        remaining_total = target_total
        remaining_days = total_days

        for day in range(1, total_days + 1):
            if day == total_days:
                # Last day gets the remaining amount
                amount = round(remaining_total, 2)
            else:
                # Generate a random amount between 30-70% of the average remaining amount
                avg_remaining = remaining_total / remaining_days
                min_amount = max(1300, avg_remaining * 0.3)
                max_amount = min(4500, avg_remaining * 1.7)
                amount = round(random.uniform(min_amount, max_amount), 2)
            
            daily_incomes.append({
                'day': day,
                'amount': amount
            })
            remaining_total -= amount
            remaining_days -= 1

        return jsonify({
            'success': True,
            'data': daily_incomes,
            'month': month,
            'total': target_total
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Use environment variables for configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
