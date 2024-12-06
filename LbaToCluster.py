def lba_to_cluster(lba, sector_size=512, cluster_size=4096, cluster_start=2):
    # Calculate how many sectors are in each cluster
    sectors_per_cluster = cluster_size // sector_size
    
    # Calculate the cluster number (LBA divided by sectors per cluster)
    cluster_number = (lba // sectors_per_cluster) + cluster_start

    return cluster_number

# Accept user input for the LBA value
lba_input = int(input("Enter the LBA value: "))  # This will prompt the user for the LBA value

# Call the conversion function
cluster_number = lba_to_cluster(lba_input)

# Output the result
print(f"The cluster number for LBA {lba_input} is: {cluster_number}")
