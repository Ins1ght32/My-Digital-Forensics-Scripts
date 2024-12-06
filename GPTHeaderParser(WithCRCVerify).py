import binascii
import struct

# CRC32 Verification Function
def calculate_gpt_crc32(header_bytes):
    # Ensure the header is at least 92 bytes long (GPT header size is 92 bytes)
    if len(header_bytes) < 92:
        raise ValueError("GPT header must be at least 92 bytes long")

    # Backup the current CRC32 value from offset 0x10 to 0x13
    original_crc32 = header_bytes[0x10:0x14]

    # Replace the CRC32 field (0x10 to 0x13) with 0x00 for calculation
    header_bytes_zeroed = bytearray(header_bytes)
    header_bytes_zeroed[0x10:0x14] = b'\x00\x00\x00\x00'

    # Calculate the CRC32 checksum on the modified header
    calculated_crc32 = binascii.crc32(header_bytes_zeroed) & 0xFFFFFFFF

    # Convert the original CRC32 (from the header) into a hex value
    original_crc32_value = int.from_bytes(original_crc32, byteorder='little')

    # Return both calculated and original CRC32 for comparison
    return calculated_crc32, original_crc32_value

# GPT Header Parsing Function
def parse_gpt_header(header_bytes):
    # Ensure the header is at least 92 bytes long
    if len(header_bytes) < 92:
        raise ValueError("GPT header must be at least 92 bytes long")

    # 1. Signature (offset 0x00-0x07, 8 bytes)
    signature = header_bytes[0x00:0x08].decode('ascii', errors='ignore').strip()

    # 2. Revision (offset 0x08-0x0b, 4 bytes, little-endian)
    revision = struct.unpack('<I', header_bytes[0x08:0x0c])[0]

    # 3. Header size (offset 0x0c-0x0d, 2 bytes, little-endian)
    header_size = struct.unpack('<H', header_bytes[0x0c:0x0e])[0]

    # 4. CRC32 of the GPT header (offset 0x10-0x13, 4 bytes)
    crc32_header = struct.unpack('<I', header_bytes[0x10:0x14])[0]

    # 5. Current LBA (offset 0x18-0x1f, 8 bytes, little-endian)
    current_lba = struct.unpack('<Q', header_bytes[0x18:0x20])[0]

    # 6. Backup LBA (offset 0x20-0x27, 8 bytes, little-endian)
    backup_lba = struct.unpack('<Q', header_bytes[0x20:0x28])[0]

    # 7. First usable LBA (offset 0x28-0x2f, 8 bytes, little-endian)
    first_usable_lba = struct.unpack('<Q', header_bytes[0x28:0x30])[0]

    # 8. Last usable LBA (offset 0x30-0x37, 8 bytes, little-endian)
    last_usable_lba = struct.unpack('<Q', header_bytes[0x30:0x38])[0]

    # 9. Disk GUID (offset 0x38-0x47, 16 bytes, little-endian)
    disk_guid = header_bytes[0x38:0x48]
    guid_str = format_guid(disk_guid)

    # 10. Starting LBA of the partition entry array (offset 0x48-0x4f, 8 bytes, little-endian)
    partition_entry_lba = struct.unpack('<Q', header_bytes[0x48:0x50])[0]

    # 11. Number of partition entries (offset 0x50-0x53, 4 bytes, little-endian)
    num_partition_entries = struct.unpack('<I', header_bytes[0x50:0x54])[0]

    # 12. Size of each partition entry (offset 0x54-0x57, 4 bytes, little-endian)
    partition_entry_size = struct.unpack('<I', header_bytes[0x54:0x58])[0]

    # 13. CRC32 of the partition entry array (offset 0x58-0x5b, 4 bytes, little-endian)
    crc32_partition_array = struct.unpack('<I', header_bytes[0x58:0x5c])[0]

    return {
        "Signature": signature,
        "Revision": revision,
        "Header Size": header_size,
        "CRC32 Header": crc32_header,
        "Current LBA": current_lba,
        "Backup LBA": backup_lba,
        "First Usable LBA": first_usable_lba,
        "Last Usable LBA": last_usable_lba,
        "Disk GUID": guid_str,
        "Partition Entry LBA": partition_entry_lba,
        "Number of Partition Entries": num_partition_entries,
        "Partition Entry Size": partition_entry_size,
        "CRC32 Partition Array (Little-endian)": f"0x{crc32_partition_array:08x}"
    }

def format_guid(guid_bytes):
    # GPT GUID is stored in little-endian for some parts, so we need to convert the format
    guid_parts = [
        struct.unpack("<I", guid_bytes[0:4])[0],  # First part (4 bytes) is little-endian
        struct.unpack("<H", guid_bytes[4:6])[0],  # Second part (2 bytes) is little-endian
        struct.unpack("<H", guid_bytes[6:8])[0],  # Third part (2 bytes) is little-endian
        binascii.hexlify(guid_bytes[8:10]).decode('ascii'),  # Fourth part (2 bytes) is big-endian
        binascii.hexlify(guid_bytes[10:16]).decode('ascii')  # Fifth part (6 bytes) is big-endian
    ]
    # Format the GUID in the standard form
    return f"{guid_parts[0]:08x}-{guid_parts[1]:04x}-{guid_parts[2]:04x}-{guid_parts[3]}-{guid_parts[4]}"

# Main function to calculate CRC32 and parse GPT header
if __name__ == "__main__":
    # Input: raw GPT header (you can replace this with your actual binary input)
    gpt_header = bytes.fromhex(input("Enter the GPT header in hex format: "))

    # Calculate and compare CRC32 values
    calculated_crc, original_crc = calculate_gpt_crc32(gpt_header)

    # Print results of CRC32 check
    print(f"Original CRC32 (from header): 0x{original_crc:08X}")
    print(f"Calculated CRC32: 0x{calculated_crc:08X}")

    if calculated_crc == original_crc:
        print("CRC32 verification successful!")
    else:
        print("CRC32 verification failed!")

    # Parse the GPT header regardless of CRC32 result
    parsed_header = parse_gpt_header(gpt_header)

    # Display the parsed GPT header information
    print("\nParsed GPT Header Information:")
    for key, value in parsed_header.items():
        print(f"{key}: {value}")
