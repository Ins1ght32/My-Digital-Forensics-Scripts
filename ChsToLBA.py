def chs_to_lba(cylinder, head, sector, hpc=255, spt=63):
    """
    Converts CHS (Cylinder, Head, Sector) to LBA (Logical Block Address).

    :param cylinder: The cylinder number (C).
    :param head: The head number (H).
    :param sector: The sector number (S).
    :param hpc: Heads per cylinder (default 255).
    :param spt: Sectors per track (default 63).
    :return: The corresponding LBA (Logical Block Address).
    """
    # Calculate LBA using the formula
    lba = (cylinder * hpc + head) * spt + (sector - 1)
    return lba

if __name__ == "__main__":
    try:
        # Get Cylinder, Head, Sector from the user
        cylinder = int(input("Enter the Cylinder (C) value: ").strip())
        head = int(input("Enter the Head (H) value: ").strip())
        sector = int(input("Enter the Sector (S) value: ").strip())
        
        # Optional: Input Heads per Cylinder (HPC) and Sectors per Track (SPT)
        hpc_input = input("Enter the Heads per Cylinder (HPC) (default is 255): ").strip()
        spt_input = input("Enter the Sectors per Track (SPT) (default is 63): ").strip()

        # Set default or user-defined HPC and SPT
        hpc = int(hpc_input) if hpc_input else 255
        spt = int(spt_input) if spt_input else 63

        # Calculate LBA
        lba = chs_to_lba(cylinder, head, sector, hpc, spt)

        # Display the result
        print(f"The LBA (Logical Block Address) is: {lba}")

    except ValueError:
        print("Invalid input. Please enter valid integer values.")
