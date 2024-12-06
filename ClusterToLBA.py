def cluster_to_lba(cluster_number, first_data_sector, sectors_per_cluster):
    """
    Convert cluster number to LBA (Logical Block Address).
    
    :param cluster_number: The cluster number to convert.
    :param first_data_sector: The first data sector (start of the data region).
    :param sectors_per_cluster: The number of sectors per cluster.
    
    :return: The corresponding LBA.
    """
    if cluster_number < 2:
        raise ValueError("Cluster number should be >= 2 (FAT cluster numbering starts from 2).")
    
    # Apply the formula to convert cluster to LBA
    lba = first_data_sector + (cluster_number - 2) * sectors_per_cluster
    return lba

# Example usage
if __name__ == "__main__":
    # Input parameters
    cluster_number = int(input("Enter the cluster number: "))  # Example: 118
    first_data_sector = int(input("Enter the first data sector: "))  # Example: 2048
    sectors_per_cluster = int(input("Enter the sectors per cluster: "))  # Example: 8

    # Convert cluster to LBA
    lba = cluster_to_lba(cluster_number, first_data_sector, sectors_per_cluster)

    # Output the result
    print(f"Cluster {cluster_number} corresponds to LBA {lba}.")
