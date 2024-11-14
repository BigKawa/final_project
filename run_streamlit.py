import os


# Check directory
current_directory = os.getcwd()
print("DIRECTORY:", current_directory)

# Windows path
windows_path = "C:\\Users\\Nutzer\\GitHub\\Ironhack\\Groupwork\\final_project"
mac_path = "/Users/linh/Documents/GitHub/GroupWork/Final_Project/final_project"


os.chdir("/Users/linh/Documents/GitHub/GroupWork/Final_Project/final_project")
# Replace 'your_script.py' with the actual name of your Streamlit file
os.system("streamlit run simple_app.py")
