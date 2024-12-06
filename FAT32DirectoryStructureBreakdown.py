import struct

def parse_fat32_directory_entry(hex_string):
    # Convert the hex string to bytes
    directory_entry = bytes.fromhex(hex_string)

    # Short filename (offset 0x00-0x07)
    short_filename = directory_entry[0x00:0x08].decode('ascii', errors='ignore').strip()

    # File extension (offset 0x08-0x0a)
    file_extension = directory_entry[0x08:0x0b].decode('ascii', errors='ignore').strip()

    # File attribute mask (offset 0x0b)
    file_attributes = directory_entry[0x0b]
    file_attributes_str = decode_fat32_attributes(file_attributes)

    # Reserved byte (offset 0x0c)
    reserved = directory_entry[0x0c]

    # File creation timestamp (offsets 0x0e-0x0f for time, 0x0d for millisecond, 0x10-0x11 for date)
    creation_time = struct.unpack("<H", directory_entry[0x0e:0x10])[0]
    creation_millisecond = directory_entry[0x0d]
    creation_date = struct.unpack("<H", directory_entry[0x10:0x12])[0]

    # Last access date (offset 0x12-0x13)
    last_access_date = struct.unpack("<H", directory_entry[0x12:0x14])[0]

    # First cluster of entry (offsets 0x14-0x15 for high word, 0x1a-0x1b for low word)
    first_cluster_high = struct.unpack("<H", directory_entry[0x14:0x16])[0]
    first_cluster_low = struct.unpack("<H", directory_entry[0x1a:0x1c])[0]

    # Last write timestamp (offsets 0x16-0x17 for time, 0x18-0x19 for date)
    last_write_time = struct.unpack("<H", directory_entry[0x16:0x18])[0]
    last_write_date = struct.unpack("<H", directory_entry[0x18:0x1a])[0]

    # File size in bytes (offset 0x1c-0x1f)
    file_size = struct.unpack("<I", directory_entry[0x1c:0x20])[0]

    # Decode time and date for creation and last write
    creation_time_str = decode_fat32_time(creation_time)
    creation_date_str = decode_fat32_date(creation_date)
    last_write_time_str = decode_fat32_time(last_write_time)
    last_write_date_str = decode_fat32_date(last_write_date)

    # Return the parsed information in a dictionary
    return {
        "short_filename": short_filename,
        "file_extension": file_extension,
        "file_attributes": file_attributes_str,
        "reserved": reserved,
        "creation_time": creation_time_str,
        "creation_millisecond": creation_millisecond,
        "creation_date": creation_date_str,
        "last_access_date": decode_fat32_date(last_access_date),
        "first_cluster_high": first_cluster_high,
        "first_cluster_low": first_cluster_low,
        "last_write_time": last_write_time_str,
        "last_write_date": last_write_date_str,
        "file_size": file_size
    }

def decode_fat32_attributes(attr_byte):
    # Decode the attribute byte (0x0b) into a readable string
    attributes = []
    if attr_byte & 0x01:  # Bit 0: Read-Only
        attributes.append("ATTR_READ_ONLY")
    if attr_byte & 0x02:  # Bit 1: Hidden
        attributes.append("ATTR_HIDDEN")
    if attr_byte & 0x04:  # Bit 2: System
        attributes.append("ATTR_SYSTEM")
    if attr_byte & 0x08:  # Bit 3: Volume ID
        attributes.append("ATTR_VOLUME_ID")
    if attr_byte & 0x10:  # Bit 4: Directory
        attributes.append("ATTR_DIRECTORY")
    if attr_byte & 0x20:  # Bit 5: Archive
        attributes.append("ATTR_ARCHIVE")
    return ", ".join(attributes)

def decode_fat32_date(date_value):
    # Convert the 16-bit date value to binary (keeping leading zeros if necessary)
    date_binary = f"{date_value:016b}"

    # Extract the fields from the binary string
    day = int(date_binary[-5:], 2)  # Bits 0-4: Day of the month (binary digits 11-15 in a 16-bit date field)
    month = int(date_binary[-9:-5], 2)  # Bits 5-8: Month of the year (binary digits 7-10)
    year = int(date_binary[:-9], 2) + 1980  # Bits 9-15: Year since 1980 (binary digits 0-6)

    # Return the decoded date in the format "YYYY-MM-DD"
    return f"{year:04d}-{month:02d}-{day:02d}"

def decode_fat32_time(time_value):
    # Extract the components from the 16-bit time value
    seconds = (time_value & 0x1F) * 2  # Bits 0-4 (2-second count)
    minutes = (time_value >> 5) & 0x3F  # Bits 5-10 (minutes)
    hours = (time_value >> 11) & 0x1F  # Bits 11-15 (hours)

    # Return the decoded time as a formatted string
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Example usage
hex_input = input("Enter a 32-byte hex string: ")  # You will input the hex string here
parsed_entry = parse_fat32_directory_entry(hex_input)

# Display the parsed FAT32 directory entry
for key, value in parsed_entry.items():
    print(f"{key}: {value}")
