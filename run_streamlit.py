import os
import platform

# Check current directory
current_directory = os.getcwd()
print("Current Directory:", current_directory)

# Define paths for Windows and macOS
windows_path = "C:\\Users\\Nutzer\\GitHub\\Ironhack\\Groupwork\\final_project"
mac_path = "/Users/linh/Documents/GitHub/GroupWork/Final_Project/final_project"

# Select path based on OS
target_path = windows_path if platform.system() == "Windows" else mac_path

try:
    # Change directory to the target path
    os.chdir(target_path)
    print("Changed directory to:", target_path)

    # Run the Streamlit app
    os.system("streamlit run simple_app.py")
except Exception as e:
    print("An error occurred:", e)
