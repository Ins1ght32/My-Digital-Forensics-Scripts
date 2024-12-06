def hex_to_decimal_and_binary(hex_string):
    # Convert hex string to bytes (ensure it's valid by stripping leading/trailing spaces)
    hex_string = hex_string.strip()

    # Convert the hex string to bytes (big-endian input)
    byte_data = bytes.fromhex(hex_string)

    # Reverse bytes to handle as little-endian
    little_endian_bytes = byte_data[::-1]

    # Convert little-endian bytes to decimal (base 10)
    decimal_value = int.from_bytes(little_endian_bytes, byteorder='big')

    # Convert little-endian bytes to binary
    binary_value = bin(decimal_value)[2:]  # Remove '0b' prefix

    return decimal_value, binary_value


# Example usage
hex_input = input("Enter a big-endian hex string: ")  # e.g., "4E47"

# Convert and print results after handling it as little-endian
decimal_output, binary_output = hex_to_decimal_and_binary(hex_input)
print(f"Decimal: {decimal_output}")
print(f"Binary: {binary_output}")
