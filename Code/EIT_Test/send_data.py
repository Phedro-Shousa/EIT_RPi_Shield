import subprocess

def save_to_txt(amp, phase, filename="/home/pedro/Desktop/log.txt"):
    with open(filename, 'w') as f:
        f.write("Amplitude Data:\n")
        for a in amp:
            f.write(f"{a}\n")
        
        f.write("\nPhase Data:\n")
        for p in phase:
            f.write(f"{p}\n")
    print(f"Data saved to {filename}")


def transfer_file(filename):
    # SSH details
    user = "Pedro Sousa"  # Replace with your laptop's username
    ip = "132.187.210.53"  # Replace with your laptop's IP address

    # Correct the file path on Windows laptop with double backslashes and quotes
    destination_path = r"C:\\Users\\Pedro Sousa\\Desktop\\TOMOPLEX\\Redesign\\code\\log.txt"

    # Use scp to transfer the file to the laptop
    command = f"scp {filename} \"{user}@{ip}:{destination_path}\""
    
    # Execute the scp command to transfer the file
    subprocess.run(command, shell=True)