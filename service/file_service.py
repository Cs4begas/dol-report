import os
import re
import shutil
import getpass

from numpy import delete

from global_constant import GLOBAL_CONSTANT


def directory_handle() :
    # Create the main folder
    username = getpass.getuser()
    desktop_path = os.path.join('C:\\Users', username, 'Desktop')
    main_folder_name = f"{GLOBAL_CONSTANT.START_TIME.strftime('%Y-%m-%d')}_to_{GLOBAL_CONSTANT.END_TIME.strftime('%Y-%m-%d')}"
    main_folder_path = os.path.join(desktop_path, main_folder_name)

    try:
        os.makedirs(main_folder_path, exist_ok=True) 
    except OSError as e:
        print(f"Error creating main folder: {e}")
        # You might want to exit or handle this error differently based on your requirements

    # Subfolders
    subfolders = ['RDP', 'SSH', 'SMB', 'Telnet']

    # Create all subfolders upfront (optional)
    for subfolder in subfolders:
        try:
            os.makedirs(os.path.join(main_folder_path, subfolder), exist_ok=True)
        except OSError as e:
            print(f"Error creating subfolder '{subfolder}': {e}")

    # Define the pattern to extract protocol and target from filenames
    middle_part_pattern = r"RptReportCKMoo_Port(\w+)_(\w+)\.xlsx$"

    # Get all files in the current directory
    files_in_directory = os.listdir('.')

    for filename in files_in_directory:
        # Extract protocol and target using regular expression
        match = re.search(middle_part_pattern, filename) 
        if match:
            protocol = match.group(1)
            target = match.group(2)

            protocol = protocol.lower() 

            if protocol in [subfolder.lower() for subfolder in subfolders]:
                # Construct the destination path using the original subfolder name (case-sensitive)
                destination_path = os.path.join(main_folder_path, protocol.capitalize(), filename)

                try:
                    shutil.copy2(filename, destination_path)
                    #Delete the original file after moving
                    os.remove(filename)
                    print(f"Moved '{filename}' to '{destination_path}'")
                except (shutil.Error, OSError) as e:
                    print(f"Error moving file '{filename}': {e}")   