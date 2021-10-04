import numpy as np
import pandas as pd
import pickle
from keras.models import Sequential, load_model
import warnings
warnings.filterwarnings("ignore")
class MakePrediction:
    def load_labels(self):
        labels = pd.read_csv('data/labels.csv')
        return labels

    def preprocess_data(self,test_data):
        test_data.dropna(inplace = True)
        test_data.reset_index(drop=True, inplace=True)
        return test_data

    def get_test_data(self,X_test):
        X_test = self.preprocess_data(X_test)
        return X_test

    def load_models(self):
        # Load the pre-trained models
        LR_model_file = 'model/LR_C10.bin'
        LR_model = pickle.load(open(LR_model_file, 'rb'))
        NN_model_file = 'model/NN_1.bin'
        NN_model = load_model(NN_model_file)
        return LR_model, NN_model

    # Functions gets dataframe as input
    def make_predictions(self, test_data, labels):

        LR_model,NN_model = self.load_models()
        # Predict target genres on test data using LR model
        m_predict_test = LR_model.predict(test_data.iloc[:, 3:157].values)
        print('Successfully predicted LR model')
        # Store predicted classes along with its title name
        LR_test_pred_op = pd.DataFrame(m_predict_test, columns=['LR_classified_genre'])
        LR_test_pred_op['title'] = test_data.title.tolist()
        LR_test_pred_op['track_id'] = test_data.trackID.tolist()
        LR_test_pred_op = LR_test_pred_op[['track_id', 'title', 'LR_classified_genre']]
        # reshape input data for NN model
        X_test = test_data.iloc[:, 3:157].values
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

        # Predict target genres on test data using NN model
        # This model outputs continuous values
        predict_x = NN_model.predict(X_test)
        NN_model_predictions = np.argmax(predict_x, axis=1)
        print('Successfully predicted NN model')

        # Resturcture the prediction values so that it matches the genre class values
        temp_labels = pd.DataFrame(labels['genre'].unique(), columns=['NN_classified_genre'])
        temp_labels = temp_labels.sort_values(by=['NN_classified_genre'], ascending=True)
        temp = pd.DataFrame(NN_model_predictions, columns=['predictions'])
        NN_test_pred_op = pd.merge(temp, temp_labels, right_index=True, left_on='predictions')
        NN_test_pred_op['track_id'] = test_data.trackID.tolist()
        NN_test_pred_op = NN_test_pred_op[['track_id', 'NN_classified_genre']]
        NN_test_pred_op['NN_classified_genre'] = NN_test_pred_op['NN_classified_genre']

        predictions = pd.merge(LR_test_pred_op, NN_test_pred_op, on='track_id', how='inner')

        return predictions

