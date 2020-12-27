# pythonexam  
Python Exam image recognition software.  
***
Medlemmer:  
Allan Bo SImonsen - cph-as484@cphbusiness.dk  
Nina Lisakowski - cph-nl163@cphbusiness.dk  
Tobias Anker Boldt-Jørgensen - cph-tb193@cphbusiness.dk  
***
Problemformulering:  
Vi vil udvikle et system der består en flask server hvor man kan uploade billeder af dyr. (data input)  
Vi vil bruge Machine learning til at finde ud af hvilket dyr der er på billedet, som blev uploadet. (Bearbejdning af data)  
Flask serveren præsentere billedet samt et søjlediagram over hvilket dyr der er mest sandsynlighed for at være det rigtige i procent.(data præsentation)  
***
Teknologier :  
Flask server (With Jinja)  
Filhåndtering   
Numpy   
Pandas   
Matplotlib   
MySQL Database with sqlalchemy  
Neural network( Keras, Tensorflow)   
***
Resultatet af vores opgave:  
Vores system består af en forside, hvor man kan uploade et billede, hvorefter vores system benytter vores Transfer Learning model og vores egne manuelt udregnede model. Til at clasificere hvad der er på billedet. Vi har givet vores modeller 10 klasser som de kan skelne i mellem.  
Vores Transfer Learning model som er basseret på VGG16 modellen, har en accuracy på 94%, og vores egen manuelt udregnede model som har en accuracy på 78%.
Når et billede er blevet uploadet og predictet af vores 2 modeller, bliver der lavet en graf for hver af modellerne ud fra resultatet. Resultatet bliver vist på en resultat side som er genereret med en random url. Den gemmes i en database og derfor kan resultatet altid hentes igen. På resultatsiden vises graferne sammen med et fact om det dyr, som hver af modellerne har predictet billedet til at være.  
Siden er deployet [her](http://www.hangovergaming.dk).
***

To get the project running do the following:  
1. Clone the project into a docker container  
2. Setup a vagrant server or an online database with a schema called `imagerecog`  
3. Update the `settings.py` file  
		`DB_URL` is the the connection to your database. insert IP, user and  password to the database. If you use a vagrant database, you can connect to it through docker with "host.docker.internal" as the IP. The port is default 3306, but can be set to anything.  
		`FILE_PATH` is the location of the project inside the docker container, Example:   `/home/jovyan/my_notebooks/imagerecognition/`  
		`URL` is the local URL the project is running in. However the important part is that the url ends with the `/result/`. An example would be: `http://127.0.0.1:5000/result/`   
4. [Download](https://drive.google.com/drive/folders/1LOuNLHcCuxji6dZaxxSxKf1xHwA8NLAX?usp=sharing) the image recognition files in the .zip folder; `All_Models.zip`.  
	To run the flask server:  
	Extract the 4 files into the `imagerecognition/resources`.  
  
    To run the image recognition files directly from CLI:  
	The 2 `TL_model.json` & `TL_weights.h5` files need to be inside the `Model_Training/Transfer_learning/my_resources`.  
	The 2 `manual_model.json` & `manual_weights.h5` files need to be inside the `Model_Training/Manual_model/my_resources`.  
  
	To train the models install the following dataset:  
	https://www.kaggle.com/alessiocorrado99/animals10  
	The dataset needs to be placed in both the `Manual_model/my_resources` & `Transfer_learning/my_resources` folders.  
5. Run the following commands to start the flask server:  
	`docker exec -it -e FLASK_APP="my_notebooks/<FLASK LOKATION på docker container>" notebookserver bash` 
	`FLASK_ENV=development flask run --host=0.0.0.0`
6. When the server is running go to: http://127.0.0.1:5000/populate to create the correct tabels in the database.
7. After that the program can be used at http://127.0.0.1:5000


