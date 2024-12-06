def parse_mbr_partition_entry(hex_string):
    # Convert the hex string to bytes
    partition_entry = bytes.fromhex(hex_string)

    # Byte 0: Boot indicator
    boot_indicator = partition_entry[0]
    boot_status = "Active (bootable)" if boot_indicator == 0x80 else "Inactive (non-bootable)"

    # Byte 1-3: Starting CHS address (not commonly used anymore)
    starting_chs = partition_entry[1:4].hex()

    # Byte 4: Partition type
    partition_type_code = partition_entry[4]
    partition_type = get_partition_type(partition_type_code)

    # Byte 5-7: Ending CHS address (not commonly used anymore)
    ending_chs = partition_entry[5:8].hex()

    # Byte 8-11: Starting LBA (little-endian, so reverse)
    starting_lba = int.from_bytes(partition_entry[8:12], byteorder='little')

    # Byte 12-15: Total sectors in partition (little-endian, so reverse)
    total_sectors = int.from_bytes(partition_entry[12:16], byteorder='little')

    # Output the parsed information
    return {
        "boot_status": boot_status,
        "starting_chs": starting_chs,
        "partition_type": partition_type,
        "ending_chs": ending_chs,
        "starting_lba": starting_lba,
        "total_sectors": total_sectors
    }

def get_partition_type(partition_type_code):
    # Mapping of partition type codes based on your image
    partition_types = {
        0x00: "Empty",
        0x01: "FAT12",
        0x02: "XENIX root",
        0x03: "XENIX usr",
        0x04: "FAT16 <32M",
        0x05: "Extended",
        0x06: "FAT16",
        0x07: "HPFS/NTFS/exFAT",
        0x08: "AIX",
        0x09: "AIX bootable",
        0x0A: "OS/2 Boot Manager",
        0x0B: "W95 FAT32",
        0x0C: "W95 FAT32 (LBA)",
        0x0E: "W95 FAT16 (LBA)",
        0x0F: "W95 Extended (LBA)",
        0x10: "OPUS",
        0x11: "Hidden FAT12",
        0x12: "Compaq diagnostics",
        0x14: "Hidden FAT16 <32M",
        0x16: "Hidden FAT16",
        0x17: "Hidden HPFS/NTFS",
        0x18: "AST SmartSleep",
        0x1B: "Hidden W95 FAT32",
        0x1C: "Hidden W95 FAT32 (LBA)",
        0x1E: "Hidden W95 FAT16 (LBA)",
        0x24: "NEC DOS",
        0x27: "Hidden NTFS WinRE",
        0x39: "Plan 9",
        0x3C: "PartitionMagic",
        0x40: "Venix 80286",
        0x41: "PPC PReP Boot",
        0x42: "SFS",
        0x4D: "QNX4.x",
        0x4E: "QNX4.x 2nd part",
        0x4F: "QNX4.x 3rd part",
        0x50: "OnTrack DM",
        0x51: "OnTrack DM6 Aux1",
        0x52: "CP/M",
        0x53: "OnTrack DM6 Aux3",
        0x54: "OnTrackDM6",
        0x55: "EZ-Drive",
        0x56: "Golden Bow",
        0x5C: "Priam Edisk",
        0x61: "SpeedStor",
        0x63: "GNU HURD or SysV",
        0x64: "Novell Netware 286",
        0x65: "Novell Netware 386",
        0x70: "DiskSecure Multi-Boot",
        0x75: "PC/IX",
        0x80: "Old Minix",
        0x81: "Minix / old Linux",
        0x82: "Linux swap / Solaris",
        0x83: "Linux",
        0x84: "OS/2 hidden C: drive",
        0x85: "Linux extended",
        0x86: "NTFS volume set",
        0x87: "NTFS volume set",
        0x88: "Linux plaintext",
        0x8E: "Linux LVM",
        0xA0: "IBM Thinkpad hibernation",
        0xA5: "FreeBSD",
        0xA6: "OpenBSD",
        0xA7: "NeXTSTEP",
        0xA8: "Darwin UFS",
        0xA9: "NetBSD",
        0xAB: "Darwin boot",
        0xAF: "HFS / HFS+",
        0xB7: "BSDI fs",
        0xB8: "BSDI swap",
        0xBB: "Boot Wizard hidden",
        0xBC: "Acronis FAT32 LBA",
        0xBE: "Solaris boot",
        0xBF: "Solaris",
        0xC1: "DRDOS/sec (FAT-12)",
        0xC4: "DRDOS/sec (FAT-16 <32M)",
        0xC6: "DRDOS/sec (FAT-16)",
        0xC7: "Syrinx",
        0xDA: "Non-FS data",
        0xDB: "CP/M / CTOS /...",
        0xDE: "Dell Utility",
        0xDF: "BootIt",
        0xE1: "DOS access",
        0xE3: "DOS R/O",
        0xE4: "SpeedStor",
        0xEB: "BeOS fs",
        0xEE: "GPT",
        0xEF: "EFI (FAT-12/16/32)",
        0xF0: "Linux/PA-RISC boot",
        0xF1: "SpeedStor",
        0xF4: "SpeedStor",
        0xFB: "VMware VMFS",
        0xFC: "VMware VMKCORE",
        0xFD: "Linux raid auto",
        0xFE: "LANstep",
        0xFF: "BBT",
    }
    return partition_types.get(partition_type_code, f"Unknown (0x{partition_type_code:02x})")

# Example usage
print("First MBR Partition Entry is at offset 0x01be to 0x01cd")
hex_input = input("Enter a 16-byte hex string (MBR partition entry): ")  # Example: "8000830008000000ee360800"
parsed_entry = parse_mbr_partition_entry(hex_input)

# Display the parsed information
for key, value in parsed_entry.items():
    print(f"{key}: {value}")
