import struct

def hex_to_ascii(hex_data):
    # Converts a hexadecimal string to its ASCII equivalent
    ascii_str = bytearray.fromhex(hex_data).decode(errors='ignore')
    return ascii_str

def parse_fat32_directory_entry(entry_bytes):
    # 1. Short filename (8.3 format) - 11 bytes
    short_filename = entry_bytes[0:11].decode('ascii', errors='ignore').strip()
    
    # 2. File attributes - 1 byte
    file_attributes = entry_bytes[11]
    
    # 3. Reserved space - 10 bytes (not important for now)
    reserved = entry_bytes[12:22]
    
    # 4. Creation time, access time, and modification time (each 2 bytes)
    creation_time = struct.unpack('<H', entry_bytes[14:16])[0]  # 0x0E - 0x0F
    access_date = struct.unpack('<H', entry_bytes[18:20])[0]  # 0x12 - 0x13
    modification_time = struct.unpack('<H', entry_bytes[22:24])[0]  # 0x16 - 0x17
    
    # 5. Starting cluster - 2 bytes (high word) + 2 bytes (low word)
    starting_cluster_high = struct.unpack('<H', entry_bytes[20:22])[0]  # 0x14 - 0x15
    starting_cluster_low = struct.unpack('<H', entry_bytes[26:28])[0]  # 0x1A - 0x1B
    starting_cluster = (starting_cluster_high << 16) | starting_cluster_low
    
    # 6. File size - 4 bytes
    file_size = struct.unpack('<I', entry_bytes[28:32])[0]
    
    return {
        "Short Filename": short_filename,
        "File Attributes": file_attributes,
        "Creation Time": creation_time,
        "Access Date": access_date,
        "Modification Time": modification_time,
        "Starting Cluster": starting_cluster,
        "File Size": file_size
    }

def parse_fat32_directory(hex_chunk):
    # Clean up input by removing spaces and newlines
    hex_chunk = hex_chunk.replace(" ", "").replace("\n", "")
    
    entries = []
    # Split the chunk into 32-byte segments
    for i in range(0, len(hex_chunk), 64):  # Each directory entry is 32 bytes (64 hex characters)
        entry_hex = hex_chunk[i:i+64]
        if len(entry_hex) == 64:
            entry_bytes = bytes.fromhex(entry_hex)
            entry = parse_fat32_directory_entry(entry_bytes)
            entries.append(entry)
    
    return entries

def get_user_input():
    print("Please paste the hex chunk of the FAT32 directory structure (multiple lines if needed):")
    hex_chunk = input("Paste hex chunk: ").strip()
    return hex_chunk

# Main function
if __name__ == "__main__":
    # Get hex chunk from the user
    hex_chunk = get_user_input()
    
    # Parse the FAT32 directory entries
    parsed_entries = parse_fat32_directory(hex_chunk)
    
    # Display the parsed entries
    for i, entry in enumerate(parsed_entries):
        print(f"\nDirectory Entry {i + 1}:")
        for key, value in entry.items():
            print(f"  {key}: {value}")
        print("-" * 40)