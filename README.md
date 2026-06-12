# CA-Clothing-Recommender Final Year Project
Uses Base model ResNet-50 and transfer learning to utlize feature extraction

Techniques:
A pre-trained ResNet-50 model was used to extract visual embeddings from the
DeepFashion Attribute Prediction dataset. A curated reference subset of 227 images
was manually annotated using three context dimensions: gender, weather, and
clothing context.

The app:
During recommendation, the user selects a context combination with 3 dimensions namely Gender ( Male/Female), 
Weather (Hot/Mild/Cold), Context (Casual, Street, Smart Casual, Formal, Gym), and
the system filters the reference subset to identify suitable query images. The selected
reference embeddings are then compared against the full embedding database using
cosine similarity ranking, and the top-K visually similar items are returned.

Users can also like images and further explore visually similar items.


This approach reduces the need for extensive user interaction history while still
allowing recommendations to be decided by user based on situational context.



Screenshots:

<img width="1918" height="960" alt="Screenshot 2026-06-12 142823" src="https://github.com/user-attachments/assets/6bacba4d-568b-4fad-80f5-64f288923da6" />

<img width="1918" height="915" alt="image" src="https://github.com/user-attachments/assets/70ed553a-13d1-4820-8389-f432ba64f5e3" />



Instructions to run the app:

##NOTE:: To download: The deepfashion attribute prediction dataset,Please navigate to:-

https://drive.google.com/file/d/0B7EVK8r0v71pa2EyNEJ0dE9zbU0/view?usp=drive_link&resourcekey=0-CPiKS-AiE8IDonk54WJ5_w

And download and extract this into the project repository, without this the images will not get displayed.


###Step 1: modify file path variables according to their location on your machine:####


Navigate to recommender.py and update Line 16 :

#Note for user: Root folder where the img/ is located, update accordingly to where the folder is stored on your machine
IMAGE_ROOT = r"C:\Users\Wanna\Desktop\Fashion FYP\img"

Next, Still in recommender.py Navigate to and update line 21 accordingly:

#Note for user: change the following directory path according to location of embeddings/ within project folder on your machine.
EMBEDDINGS_DIR = r"C:\Users\Wanna\Desktop\Fashion FYP\embeddings"

Lastly, Still in recommender.py, Navigate to and update Line 85 as follows

#Note 3: Please update the following path as well to where the file is stored on your machine.
CURATED_PATH = r"C:\Users\Wanna\Desktop\Fashion FYP\notebooks\curated_annotations.csv"



####Step 2: Running the application####


###Open IDE terminal/ powershell####
Make sure terminal points to project directory 


run command: 
cd notebooks

Next, Run the following command

streamlit run app.py

Application will be running on http://localhost:8501/ 


