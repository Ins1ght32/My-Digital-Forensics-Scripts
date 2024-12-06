import struct
import binascii

def parse_gpt_partition_entry(entry_bytes, sector_size=512):
    # Ensure the partition entry is 128 bytes long
    if len(entry_bytes) != 128:
        raise ValueError("GPT Partition Entry must be exactly 128 bytes long")

    # 1. Partition Type GUID (16 bytes, little-endian)
    partition_type_guid = entry_bytes[0x00:0x10]
    partition_type_str = format_guid(partition_type_guid)

    # 2. Unique Partition GUID (16 bytes, little-endian)
    unique_partition_guid = entry_bytes[0x10:0x20]
    unique_guid_str = format_guid(unique_partition_guid)

    # 3. Starting LBA (8 bytes, little-endian)
    start_lba = struct.unpack('<Q', entry_bytes[0x20:0x28])[0]

    # 4. Ending LBA (8 bytes, little-endian)
    end_lba = struct.unpack('<Q', entry_bytes[0x28:0x30])[0]

    # 5. Calculate partition size in bytes
    partition_size_bytes = (end_lba - start_lba + 1) * sector_size

    # 6. Attribute flags (8 bytes, little-endian)
    attribute_flags = struct.unpack('<Q', entry_bytes[0x30:0x38])[0]

    # Breakdown attribute flags based on image
    gpt_attributes = attribute_flags & 0x07  # Bits 0-2
    reserved_bits = (attribute_flags >> 3) & 0xFFFFFFFFFFFF  # Bits 3-47 (should be zero)
    type_specific = (attribute_flags >> 48) & 0xFFFF  # Bits 48-63

    # 7. Partition Name (72 bytes, UTF-16LE, null-terminated)
    partition_name_bytes = entry_bytes[0x38:0x80]
    partition_name = partition_name_bytes.decode('utf-16le').rstrip('\x00')

    return {
        "Partition Type GUID": partition_type_str,
        "Unique Partition GUID": unique_guid_str,
        "Starting LBA": start_lba,
        "Ending LBA": end_lba,
        "Partition Size (bytes)": partition_size_bytes,
        "Attribute Flags (Raw)": f"0x{attribute_flags:016x}",
        "GPT Attributes (Bits 0-2)": f"0x{gpt_attributes:03x}",
        "Reserved (Bits 3-47)": f"0x{reserved_bits:012x}",
        "Type-Specific Attributes (Bits 48-63)": f"0x{type_specific:04x}",
        "Partition Name": partition_name
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

# Example usage:
if __name__ == "__main__":
    # Input: raw GPT partition entry (replace this with your actual binary input)
    partition_entry = bytes.fromhex(input("Enter the GPT Partition Entry in hex format (128 bytes): "))
    
    # Optionally accept sector size, default to 512 bytes
    sector_size_input = input("Enter sector size in bytes (default is 512): ")
    if sector_size_input.isdigit():
        sector_size = int(sector_size_input)
    else:
        sector_size = 512

    # Parse the GPT Partition Entry
    parsed_entry = parse_gpt_partition_entry(partition_entry, sector_size)

    # Display the parsed Partition Entry information
    print("\nParsed GPT Partition Entry:")
    for key, value in parsed_entry.items():
        print(f"{key}: {value}")
