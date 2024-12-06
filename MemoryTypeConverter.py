def convert_size_to_all(value, from_unit):
    """
    Convert a given value in one unit to all other units of data: bytes (B), kilobytes (KB), megabytes (MB), gigabytes (GB), and terabytes (TB).
    
    Parameters:
    - value: The numerical value to convert.
    - from_unit: The unit of the input value ('B', 'KB', 'MB', 'GB', 'TB').
    
    Returns:
    - A dictionary containing the converted values for all units.
    """
    
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
    }
    
    # Ensure the input unit is valid
    if from_unit not in units:
        raise ValueError("Invalid unit. Must be one of 'B', 'KB', 'MB', 'GB', 'TB'")
    
    # Convert the input value to bytes first
    value_in_bytes = value * units[from_unit]
    
    # Convert from bytes to all other units
    converted_values = {unit: value_in_bytes / units[unit] for unit in units}
    
    return converted_values

# Prompt user for input
try:
    input_value = float(input("Enter the value to convert: "))
    from_unit = input("Enter the unit you are converting from (B, KB, MB, GB, TB): ").upper()

    # Perform the conversion to all units
    conversions = convert_size_to_all(input_value, from_unit)

    # Display the results
    print(f"{input_value} {from_unit} is equivalent to:")
    for unit, converted_value in conversions.items():
        print(f"{converted_value:.2f} {unit}")

except ValueError as e:
    print(f"Error: {e}")
