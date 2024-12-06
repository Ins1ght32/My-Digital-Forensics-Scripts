def sector_to_cluster(sector_number, first_data_sector, sectors_per_cluster):
    """
    Convert sector number to cluster number.
    
    :param sector_number: The sector number you want to convert.
    :param first_data_sector: The first sector of the data region (after the reserved sectors).
    :param sectors_per_cluster: Number of sectors per cluster.
    
    :return: Corresponding cluster number.
    """
    if sector_number < first_data_sector:
        raise ValueError("Sector number is before the data region (first data sector).")

    # Calculate the cluster number
    cluster_number = ((sector_number - first_data_sector) // sectors_per_cluster) + 2
    return cluster_number

# Example usage:
if __name__ == "__main__":
    # Input values for calculation
    sector_number = int(input("Enter the sector number: "))
    first_data_sector = int(input("Enter the first data sector: "))
    sectors_per_cluster = int(input("Enter the sectors per cluster: "))
    
    # Calculate the cluster number
    cluster_number = sector_to_cluster(sector_number, first_data_sector, sectors_per_cluster)
    
    # Display the result
    print(f"Sector {sector_number} corresponds to Cluster {cluster_number}.")
