from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Path to the directory where files will be stored
PERSISTENT_STORAGE_PATH = '/home/ghost/app/persistent_storage'

if not os.path.exists(PERSISTENT_STORAGE_PATH):
    os.makedirs(PERSISTENT_STORAGE_PATH)

def calculate_product_sum(filename, product):
    filepath = os.path.join(PERSISTENT_STORAGE_PATH, filename)
    if not os.path.exists(filepath):
        return None, "File not found."

    try:
        total_sum = 0
        with open(filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['product'] == product:
                    total_sum += int(row[' amount '])
        return total_sum, None
    except Exception as e:
        return None, f"Input file not in CSV format: {str(e)}"

@app.route('/calculate-sum', methods=['POST'])
def calculate_sum():
    try:
        request_data = request.get_json()
        filename = request_data.get('file')
        product = request_data.get('product')
        
        if not filename or not product:
            return jsonify({"file": filename, "error": "Invalid JSON input."}), 400
        
        total_sum, error = calculate_product_sum(filename, product)
        
        if error:
            return jsonify({"file": filename, "error": error}), 500
        
        return jsonify({"file": filename, "sum": total_sum}), 200
    
    except Exception as e:
        return jsonify({"file": None, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)

