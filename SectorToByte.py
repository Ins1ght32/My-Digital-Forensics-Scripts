def calculate_byte_offset(sector_address, sector_size=512):
    """
    Calculates the byte offset for a given sector starting address.
    
    :param sector_address: The sector starting address (integer).
    :param sector_size: Size of a sector in bytes (default is 512).
    :return: The byte offset.
    """
    byte_offset = sector_address * sector_size
    return byte_offset

if __name__ == "__main__":
    # Input sector starting address from user
    try:
        sector_address = int(input("Enter the sector starting address (decimal): ").strip())
    except ValueError:
        print("Invalid input. Please enter a valid integer for the sector starting address.")
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

    # Calculate the byte offset
    byte_offset = calculate_byte_offset(sector_address, sector_size)

    # Display the byte offset in decimal and hex
    print(f"Byte Offset (Decimal): {byte_offset} bytes")
    print(f"Byte Offset (Hexadecimal): {hex(byte_offset)}")
