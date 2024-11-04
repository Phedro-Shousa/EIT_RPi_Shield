import subprocess

def save_to_txt(amp, phase, max_value, min_value, peak_peak_current, avg_current, filename="/home/pedro/Desktop/log.txt"):
    with open(filename, 'w') as f:
        # Print current values at the top with tabs for Excel-friendly formatting
        f.write(f"Max Current:\t{(max_value / 200):.2f} mA\t{max_value:.2f}\n")
        f.write(f"Min Current:\t{(min_value / 200):.2f} mA\t{min_value:.2f}\n")
        f.write(f"Peak-Peak Current:\t{(peak_peak_current / 200):.2f} mA\t{peak_peak_current:.2f}\n")
        f.write(f"Average Current:\t{(avg_current / 200):.2f} mA\t{avg_current:.2f}\n\n")

        # Write the header for amplitude and phase with tabs
        f.write(f"{'Amplitude':<15}\t{'Phase':<15}\n")
        f.write(f"{'-' * 15}\t{'-' * 15}\n")  # Separator line
        
        # Write amplitude and phase values in aligned columns with tabs
        for a, p in zip(amp, phase):
            f.write(f"{a:<15.2f}\t{p:<15.2f}\n")
    
    print(f"Data saved to {filename} \n")



def transfer_file(filename="/home/pedro/Desktop/log.txt"):
    # SSH details
    user = "Pedro Sousa"  # Replace with your laptop's username
    ip = "132.187.210.53"  # Replace with your laptop's IP address

    # Correct the file path on Windows laptop with double backslashes and quotes
    destination_path = r"C:\\Users\\Pedro Sousa\\Desktop\\TOMOPLEX\\Redesign\\Rasp_Code\\log.txt"

    # Use scp to transfer the file to the laptop
    command = f"scp {filename} \"{user}@{ip}:{destination_path}\""
    
    # Execute the scp command to transfer the file
    subprocess.run(command, shell=True)