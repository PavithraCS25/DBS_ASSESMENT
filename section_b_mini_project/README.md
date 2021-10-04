# Mini Project - Music Genre Classification

BACKEND:
	- pip3 install -r requirements.txt
	
	- make_predictions.py:
		* Makes predictions for provided test file
	
	- dao.py:
		* loads predictions to SQLite database
		* retrives predictions, distinct genres, and distinct titles per genre from database
		
	- app.py:
		* creates OpenAPI specifications using Swagger

FRONTEND:
 ![alt text](https://github.com/PavithraCS25/dbs_assessment/blob/main/section_b_mini_project/img/Data_Exploration_Jupyter_NB.png)
 
 Click on the jupyter image to load the html of exploration and model building jupyter notebook 
 
 ![alt text](https://github.com/PavithraCS25/dbs_assessment/blob/main/section_b_mini_project/img/Predictions_OP.png)
 
 Load test file and click on "Predict" to fetch the predictions of Logistic Regression and LSTM - NN classifiers
 
 ![alt text](https://github.com/PavithraCS25/dbs_assessment/blob/main/section_b_mini_project/img/testfile_selection.png)
 
 Select value from the drop down to filter predictions of specific test files
 
 ![alt text](https://github.com/PavithraCS25/dbs_assessment/blob/main/section_b_mini_project/img/genre_selection.png)
 
 Select genre from the drop down displaying list of classified genres from the predictions
 
 ![alt text](https://github.com/PavithraCS25/dbs_assessment/blob/main/section_b_mini_project/img/title_listing.png)
 
 Select value from the drop down to filter titles of specific genre
 
 
 
 

 
	
