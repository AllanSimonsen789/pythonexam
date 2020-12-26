# pythonexam  
Python Exam image recognition software  
  
This is a flask server with imagerecognition.  
  
To get the project running do the following:  
1. clone the project into a docker container  
2. setup a vagrant server or an online database with a schema called "imagerecog"  
3. update the "settings.py" file  
		DB_URL is the the connection to your database. insert IP, user and  password to the database  
		FILE_PATH is the location of the project inside the docker container, Example: "/home/jovyan/my_notebooks/imagerecognition/"  
		URL is the local URL the project is running in... default is port5000  
4. [Download](https://drive.google.com/drive/folders/1LOuNLHcCuxji6dZaxxSxKf1xHwA8NLAX?usp=sharing) the image recognition files; "TL_model.json", "TL_weights.h5", "manual_model.json" & "manual_weights.h5".  
		To run the flask server:  
		The 4 files need to be placed inside the "imagerecognition/resources".  
  
		To run the image recognition files directly from CLI:  
		The 2 "TL" files need to be inside the "Model_Training/Transfer_learning/my_resources".  
		The 2 "manual" files need to be inside the "Model_Training/Manual_model/my_resources".  
  
		To train the models install the following dataset:  
		https://www.kaggle.com/alessiocorrado99/animals10  
		The dataset needs to be placed in both the "Manual_model/my_resources" & "Transfer_learning/my_resources" folders.  
4. Kør følgende kommandoer for at starte flask serveren: 
	docker exec -it -e FLASK_APP="my_notebooks/<FLASK LOKATION på docker container>" notebookserver bash 
	FLASK_ENV=development flask run --host=0.0.0.0
5. Når serveren kører gå til: http://127.0.0.1:5000/populate for at oprette de korrekte tabeller. 
6. herefter kan programmet bruges ved at gå til http://127.0.0.1:5000

[Github Large File Storage - For weights.h5 & model.json](https://git-lfs.github.com/)

