def validate_option_type(option_type):
    return option_type.lower() in ['call', 'put']

def convert_percent_to_decimal(val):
    return val / 100.0 if val > 1 else val

def convert_days_to_years(days):
    return days / 365.0
