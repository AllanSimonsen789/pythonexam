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
4. Kør følgende kommandoer for at starte flask serveren: 
	docker exec -it -e FLASK_APP="my_notebooks/<FLASK LOKATION på docker container>" notebookserver bash 
	FLASK_ENV=development flask run --host=0.0.0.0
5. Når serveren kører gå til: http://127.0.0.1:5000/populate for at oprette de korrekte tabeller. 
6. herefter kan programmet bruges ved at gå til http://127.0.0.1:5000

[Github Large File Storage - For weights.h5 & model.json](https://git-lfs.github.com/)

