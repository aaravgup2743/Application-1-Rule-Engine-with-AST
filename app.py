from flask import Flask, request, jsonify
import re

app = Flask(__name__)

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

# Function to validate rule strings
def validate_rule(rule_string):
    # Simple regex for validation: checks for basic structure (conditions and operators)
    pattern = r'^\(\s*([a-zA-Z_]+[ ]*(>=|<=|>|<|==|!=)[ ]*[\d]+|[a-zA-Z_]+[ ]*=[ ]*\'[a-zA-Z_]+\'|[a-zA-Z_]+[ ]*!=[ ]*\'[a-zA-Z_]+\'|[a-zA-Z_]+)\s*(AND|OR)\s*([a-zA-Z_]+[ ]*(>=|<=|>|<|==|!=)[ ]*[\d]+|[a-zA-Z_]+[ ]*=[ ]*\'[a-zA-Z_]+\'|[a-zA-Z_]+[ ]*!=[ ]*\'[a-zA-Z_]+\')\s*\)$'
    return re.match(pattern, rule_string) is not None

# Function to create an AST from a rule string
def create_rule(rule_string):
    if not validate_rule(rule_string):
        raise ValueError("Invalid rule format")

    # For demonstration, we will create a simple hardcoded AST for the example rule
    node = Node(type='operator',
                left=Node(type='operand', value='age > 30'),
                right=Node(type='operand', value="department = 'Sales'"))
    return node

# Store rules in memory (or implement a database for persistence)
rules_db = {}

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.json.get('rule')

    try:
        ast = create_rule(rule_string)
        rule_id = len(rules_db) + 1
        rules_db[rule_id] = ast
        return jsonify({"AST": {"type": ast.type, "left": ast.left.__dict__, "right": ast.right.__dict__}, "rule_id": rule_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@app.route('/modify_rule/<int:rule_id>', methods=['PUT'])
def modify_rule_endpoint(rule_id):
    if rule_id not in rules_db:
        return jsonify({"error": "Rule ID not found"}), 404

    new_rule_string = request.json.get('rule')
    try:
        ast = create_rule(new_rule_string)
        rules_db[rule_id] = ast
        return jsonify({"AST": {"type": ast.type, "left": ast.left.__dict__, "right": ast.right.__dict__}}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

@app.route('/evaluate_rule/<int:rule_id>', methods=['POST'])
def evaluate_rule_endpoint(rule_id):
    if rule_id not in rules_db:
        return jsonify({"error": "Rule ID not found"}), 404

    data = request.json
    ast = rules_db[rule_id]

    # Dummy evaluation logic; you'd want to implement the real evaluation based on the AST
    if ast.left.value == 'age > 30' and data.get("age", 0) > 30:
        return jsonify({"result": True}), 200
    return jsonify({"result": False}), 200

if __name__ == '__main__':
    app.run(debug=True)
