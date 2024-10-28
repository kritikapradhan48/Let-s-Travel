from flask import Flask, jsonify, request
from models import db, User, Transaction

app = Flask(__name__)

@app.route('/wallet/balance/<int:user_id>', methods=['GET'])
def check_balance(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'wallet_balance': user.wallet_balance})
    return jsonify({'error': 'User not found'}), 404

@app.route('/wallet/add_funds', methods=['POST'])
def add_funds():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    user = User.query.get(user_id)
    if user and amount > 0:
        user.wallet_balance += amount
        transaction = Transaction(user_id=user_id, amount=amount, transaction_type='credit')
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Funds added successfully', 'wallet_balance': user.wallet_balance})
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/wallet/use_funds', methods=['POST'])
def use_funds():
    data = request.get_json()
    user_id = data.get('user_id')
    amount = data.get('amount')

    user = User.query.get(user_id)
    if user and amount > 0 and user.wallet_balance >= amount:
        user.wallet_balance -= amount
        transaction = Transaction(user_id=user_id, amount=amount, transaction_type='debit')
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'message': 'Funds deducted successfully', 'wallet_balance': user.wallet_balance})
    return jsonify({'error': 'Insufficient balance or invalid request'}), 400
