import hashlib

def hash_partition_entry(partition_entry):
    """
    Hashes the MBR partition entry using both SHA-256 and SHA-512.

    :param partition_entry: The partition entry in bytes.
    :return: A tuple containing the SHA-256 and SHA-512 hashes.
    """
    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256(partition_entry).hexdigest()
    
    # Compute SHA-512 hash
    sha512_hash = hashlib.sha512(partition_entry).hexdigest()

    return sha256_hash, sha512_hash

if __name__ == "__main__":
    # Input the MBR partition entry as a hex string (big-endian from the hex editor)
    partition_hex = input("Enter the MBR partition entry (hex, big-endian as seen in hex editor): ").strip()

    # Ensure the input length is valid for partition entries (32 hex characters for 16 bytes)
    if len(partition_hex) % 2 != 0 or len(partition_hex) != 32:
        print("Error: The MBR partition entry should be a 32-character hex string (16 bytes).")
        exit()

    try:
        # Convert the hex string directly to bytes (no endian conversion)
        partition_entry = bytes.fromhex(partition_hex)
    
    except ValueError:
        print("Error: Invalid hex string. Please ensure it's a valid hex.")
        exit()

    # Hash the partition entry using both SHA-256 and SHA-512
    sha256_hash, sha512_hash = hash_partition_entry(partition_entry)

    # Display the hash results
    print(f"SHA-256: {sha256_hash}")
    print(f"SHA-512: {sha512_hash}")
