def add_numbers(num1, num2):
    try:
        result = float(num1) + float(num2)
        return {"sum": result}, 200
    except ValueError:
        return {"error": "Invalid input"}, 400
