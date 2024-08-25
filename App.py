from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ethics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define a model for the decisions table
class Decision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(256), nullable=False)
    decision = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Decision {self.id} - {self.command}>"

# Create the database and the tables
with app.app_context():
    db.create_all()

# Basic ethical decision-making function
def ethical_decision(command):
    if "access_private_data" in command:
        return {"decision": "allowed", "reason": "ethical principles"}
    return {"decision": "allow", "reason": "with ethical principles"}

# API endpoint to process the command
@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command')

    # Make an ethical decision
    decision_data = ethical_decision(command)
    decision = decision_data['decision']
    reason = decision_data['reason']

    # Save the decision to the database
    new_decision = Decision(command=command, decision=decision, reason=reason)
    db.session.add(new_decision)
    db.session.commit()

    # Return the decision
    return jsonify(decision_data)

# API endpoint to fetch all decisions
@app.route('/decisions', methods=['GET'])
def get_decisions():
    decisions = Decision.query.all()
    results = [
        {
            "id": decision.id,
            "command": decision.command,
            "decision": decision.decision,
            "reason": decision.reason,
            "timestamp": decision.timestamp
        } for decision in decisions
    ]

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
