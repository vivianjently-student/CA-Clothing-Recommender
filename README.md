# CA-Clothing-Recommender Final Year Project
Uses Base model ResNet-50 and transfer learning to utlize feature extraction
Instructions to run the app:
###Step 1: modify file path variables according to their location on your machine:####

Navigate to recommender.py and update Line 16 :

#Note for user: Root folder where the img/ is located, update accordingly to where the folder is stored on your machine
IMAGE_ROOT = r"C:\Users\Wanna\Desktop\Fashion FYP\img"

Next, Still in recommender.py Navigate to and update line 21 accordingly:

#Note for user: change the following directory path to where you stored the embeddings folder on your machine.
EMBEDDINGS_DIR = r"C:\Users\Wanna\Desktop\Fashion FYP\embeddings"

Lastly, Still in recommender.py, Navigate to and update Line 85 as follows

#Note 3: Please update the following path as well to where the file is stored on your machine.
CURATED_PATH = r"C:\Users\Wanna\Desktop\Fashion FYP\notebooks\curated_annotations.csv"

####Step 2: Running the application####
###Open IDE terminal/ powershell####
Make sure terminal points to project directory 
run command
cd notebooks

Next, Run the following command
streamlit run app.py

Application will be running on http://localhost:8501/ 


