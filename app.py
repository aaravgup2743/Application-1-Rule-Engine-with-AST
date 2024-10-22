from flask import Flask, request, jsonify

app = Flask(__name__)

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to left Node
        self.right = right  # Reference to right Node
        self.value = value  # Value for operand nodes

    def to_dict(self):
        """Convert the Node to a dictionary for JSON serialization."""
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

def create_rule(rule_string):
    """Create a rule from a rule string and return the AST as a Node."""
    try:
        if not rule_string:
            raise ValueError("Rule string cannot be empty.")

        rule_string = rule_string.strip()

        if " AND " in rule_string:
            left, right = rule_string.split(" AND ", 1)
            return Node("operator", left=create_rule(left), right=create_rule(right), value="AND")
        elif " OR " in rule_string:
            left, right = rule_string.split(" OR ", 1)
            return Node("operator", left=create_rule(left), right=create_rule(right), value="OR")
        else:
            return Node("operand", value=rule_string)

    except Exception as e:
        return {"error": str(e)}

def combine_rules(rules):
    """Combine multiple rules into a single AST."""
    if not rules or not isinstance(rules, list):
        raise ValueError("No rules provided for combination.")

    combined_ast = None
    for rule in rules:
        operator = "AND"  # Default operator

        # Ensure that the rule is processed without extra parentheses
        try:
            # Use create_rule directly on the rule string
            ast = create_rule(rule.strip())  # Strip any extra whitespace

            if combined_ast is None:
                combined_ast = ast
            else:
                combined_ast = Node("operator", left=combined_ast, right=ast, value=operator)
        except Exception as e:
            return {"error": f"Invalid rule format: {str(e)}"}

    return combined_ast



def evaluate_rule(ast, data):
    """Evaluate the rule represented by the AST against the provided data."""
    if ast.type == "operand":
        if ">" in ast.value:
            left, right = ast.value.split(">")
            left_value = data.get(left.strip())
            right_value = int(right.strip())
            return left_value > right_value
        elif "<" in ast.value:
            left, right = ast.value.split("<")
            left_value = data.get(left.strip())
            right_value = int(right.strip())
            return left_value < right_value
        elif "=" in ast.value:
            left, right = ast.value.split("=")
            left_value = data.get(left.strip())
            right_value = right.strip().replace("'", "")
            return left_value == right_value

    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    data = request.get_json()
    rule_string = data.get('rule_string')
    ast = create_rule(rule_string)
    return jsonify({"AST": ast.to_dict()}), 201

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    data = request.get_json()
    rules = data.get('rules', [])
    
    try:
        combined_ast = combine_rules(rules)
        return jsonify({"Combined AST": combined_ast.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Return error if something went wrong

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    data = request.get_json()
    ast_data = data.get('ast')
    input_data = data.get('data')

    # Reconstruct the AST from the received data
    ast = Node(ast_data['type'])
    if 'left' in ast_data:
        ast.left = Node(ast_data['left']['type'], value=ast_data['left'].get('value'))
    if 'right' in ast_data:
        ast.right = Node(ast_data['right']['type'], value=ast_data['right'].get('value'))
    ast.value = ast_data.get('value')

    result = evaluate_rule(ast, input_data)
    return jsonify({"result": result}), 200

if __name__ == '__main__':
    app.run(debug=True)
