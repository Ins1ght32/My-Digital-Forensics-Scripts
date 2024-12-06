def hex_to_bytes(hex_string):
    """
    Converts a hex string to bytes.
    """
    # Ensure the hex string length is even
    if len(hex_string) % 2 != 0:
        raise ValueError("Hex string must have an even length.")
    
    # Convert hex string to bytes
    byte_data = bytes.fromhex(hex_string)
    return byte_data

def convert_bytes_to_decimal(byte_data):
    """
    Converts the first few bytes of the file to a decimal number (which represents the LBA or sector count).
    """
    # Convert the byte data to a hexadecimal string
    hex_string = byte_data.hex()

    # Convert hex string to decimal
    decimal_value = int(hex_string, 16)
    return decimal_value

if __name__ == "__main__":
    # Input hex string from user
    hex_string = input("Enter the hex string: ").strip()

    # Convert hex to bytes
    try:
        byte_data = hex_to_bytes(hex_string)
    except ValueError as e:
        print(f"Error: {e}")
        exit()

    # Input sector size from user or use default
    sector_size_input = input("Enter sector size (default is 512): ").strip()
    if sector_size_input:
        try:
            sector_size = int(sector_size_input)
        except ValueError:
            print("Invalid sector size. Using default value of 512.")
            sector_size = 512
    else:
        sector_size = 512

    # Convert the first few bytes to a decimal number representing the LBA
    decimal_lba = convert_bytes_to_decimal(byte_data)

    # Calculate the total size in bytes by multiplying sector size by the LBA (sector count)
    total_size_bytes = decimal_lba * sector_size

    # Display the hex and decimal values (LBA)
    print(f"Hexadecimal LBA: {byte_data.hex()}")
    print(f"Decimal LBA (Means Sector Number OR Sector Count - Dependent on Usage): {decimal_lba}")
    
    # Display the total size in bytes
    print(f"Total size in bytes (Only useful if above is sector count): {total_size_bytes}")
