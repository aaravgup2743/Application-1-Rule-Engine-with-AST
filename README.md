Project - 1
                                                                                     #Application-1-Rule-Engine-with-AST
#Overview
This project implements a simple Rule Engine using Flask, designed to create, combine, and evaluate rules represented as Abstract Syntax Trees (ASTs). It allows for the creation of conditional rules and supports both AND and OR operations.

#Features
1.Create Rules: Define rules as strings which are parsed into ASTs.
2.Combine Rules: Combine multiple rules into a single AST using the default AND operator.
3.Evaluate Rules: Evaluate the combined or individual rules against provided data.
4.Error Handling: Comprehensive error messages for invalid inputs or rule formats.

#Endpoints
1. Create Rule
Endpoint: /create_rule
Method: POST
Request Body:(select raw)
json
Copy code
{
    "rule_string": "age > 30 AND department = 'Sales'"
}
Response:
json
Copy code
{
    "AST": {
        "left": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "age > 30"
        },
        "right": {
            "left": null,
            "right": null,
            "type": "operand",
            "value": "department = 'Sales'"
        },
        "type": "operator",
        "value": "AND"
    }
}


2. Combine Rules
Endpoint: /combine_rules
Method: POST
Request Body:(select raw)
json
Copy code
{
    "rules": [
        "age > 30 AND department = 'Sales'",
        "age < 25 AND department = 'Marketing'"
    ]
}
Response:
json
Copy code
{
    "Combined AST": {
        "left": {
            "left": {
                "left": null,
                "right": null,
                "type": "operand",
                "value": "age > 30"
            },
            "right": {
                "left": null,
                "right": null,
                "type": "operand",
                "value": "department = 'Sales'"
            },
            "type": "operator",
            "value": "AND"
        },
        "right": {
            "left": {
                "left": null,
                "right": null,
                "type": "operand",
                "value": "age < 25"
            },
            "right": {
                "left": null,
                "right": null,
                "type": "operand",
                "value": "department = 'Marketing'"
            },
            "type": "operator",
            "value": "AND"
        },
        "type": "operator",
        "value": "AND"
    }
}


3. Evaluate Rule
Endpoint: /evaluate_rule
Method: POST
Request Body:(select raw)
json
Copy code
{
    "ast": {
        "type": "operator",
        "left": {
            "type": "operand",
            "value": "age > 30"
        },
        "right": {
            "type": "operand",
            "value": "department = 'Sales'"
        },
        "value": "AND"
    },
    "data": {
        "age": 35,
        "department": "Sales"
    }
}
Response:
json
Copy code
{
    "result": true
}


#How to Use
Install Required Packages: Ensure that Python is installed on your system. Then, install the required libraries by running:

bash
Copy code
pip install Flask
Run the Application: Execute the Flask application by running the following command:

bash
Copy code
python app.py
The server will start at http://127.0.0.1:5000/.

#Test Using Postman:

Install Postman.
Use the following steps to test the API:
1.Create Rule: Choose POST and enter http://127.0.0.1:5000/create_rule. Use a JSON body with the rule string you want to convert into an AST.
2.Combine Rules: Choose POST and enter http://127.0.0.1:5000/combine_rules. Provide a list of rules in the JSON body.
3.Evaluate Rule: Choose POST and enter http://127.0.0.1:5000/evaluate_rule. Provide the AST and the data you want to evaluate against.


#Bonus Considerations
1.Security:
Uses POST requests to avoid exposing sensitive data in URLs.
Input validation to prevent malicious payloads from causing unintended behavior.

2.Performance:
Designed with simplicity in mind, focusing on quick rule evaluation.
Efficient processing of rule combinations by directly parsing strings and minimizing overhead.



