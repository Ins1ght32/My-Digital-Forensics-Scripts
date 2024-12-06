def calculate_offset(lba, sector_size=512):
    """Calculate the byte offset for a given LBA and sector size."""
    return lba * sector_size

def hex_to_byte_offset(hex_value):
    """Convert a hex value to a decimal byte offset."""
    try:
        return int(hex_value, 16)  # Convert from hex to decimal
    except ValueError:
        print("Invalid hexadecimal input.")
        return None

def main():
    # Ask the user to input the LBA number
    try:
        lba = int(input("Enter the LBA number: "))
        # Ask the user to input the sector size (optional, default is 512 bytes)
        sector_size = input("Enter the sector size in bytes (default is 512): ")

        # Use default sector size (512 bytes) if the user doesn't provide one
        if sector_size == '':
            sector_size = 512
        else:
            sector_size = int(sector_size)

        # Calculate the byte offset for the first LBA
        offset = calculate_offset(lba, sector_size)

        # Print the result
        print(f"Byte offset for LBA {lba} with sector size {sector_size} bytes is: {offset} bytes (or 0x{offset:X} in hex)")


        print(f"-----Calculate byte space from earlier defined start and to be defined end-----")
        # Now prompt the user to enter another address (in decimal or hex)
        second_address = input("Enter address of where data ends: 0x")

        # Handle hex input
        second_offset = hex_to_byte_offset(second_address)  # Remove the '0x' prefix

        # Calculate the difference in bytes and hex
        byte_difference = abs(second_offset - offset)
        hex_difference = hex(byte_difference)

        # Print the differences
        #print(f"-----Difference between the addresses-----")
        print(f"Byte difference: {byte_difference} bytes")
        print(f"Hexadecimal difference: {hex_difference}")

    except ValueError:
        print("Invalid input. Please enter a valid LBA number and address.")

if __name__ == "__main__":
    main()
