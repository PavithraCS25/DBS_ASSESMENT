from flask import Flask, jsonify, request
from flasgger import Swagger
from dao import DAO
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
dao = DAO()

@app.route('/v1/music/predictions/<file_id>/', methods=['GET'])
def predictions(file_id):
    """Example endpoint returning a list of predictions
    ---
    parameters:
      - name: file_id
        in: path
        type: string
        #enum: ['all', '2435', '3545']
        required: true
        default: all
    definitions:
      File_id:
        type: object
        properties:
          file_id:
            type: array
            items:
              $ref: '#/definitions/file_id'
      file_id:
        type: json
    responses:
      200:
        description: A list of prediction (may be filtered by file_id)
        schema:
          $ref: '#/definitions/file_id'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    predictions = dao.prediction_all(file_id)
    result = predictions
    print(result)
    print("test - " + str(result))
    return result

@app.route('/v1/music/predictions/genres/', methods=['GET'])
def genres():
    """Example endpoint returning a list of genres
    ---
    definitions:
      Genres:
        type: object
        properties:
          genres:
            type: array
            items:
              $ref: '#/definitions/genres'
      genres:
        type: json
    responses:
      200:
        description: A list of genres
        schema:
          $ref: '#/definitions/genres'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    genres = dao.get_all_genres()
    result = genres
    print("test - " + str(result))
    return result

@app.route('/v1/music/predictions/tiles/<genre>/', methods=['GET'])
def genre_title(genre):
    """Example endpoint returning a list of titles
    ---
    parameters:
      - name: genre
        in: path
        type: string
        #enum: ['all', 'pop', 'folk']
        required: true
        default: all
    definitions:
      genre_title:
        type: object
        properties:
          file_id:
            type: array
            items:
              $ref: '#/definitions/genre_title'
      genre:
        type: json
    responses:
      200:
        description: A list of titles (may be filtered by genre)
        schema:
          $ref: '#/definitions/genre_title'
        examples:
          rgb: ['red', 'green', 'blue']
    """

    titles = dao.get_all_titles(genre)
    result = titles
    print("test - " + str(result))
    return result


@app.route('/v1/music/fetchauditfile/', methods=['GET'])
def fetch_audit_files():
    """Example endpoint returning a list of fetchauditfile
    ---

    definitions:
      auditfile:
        type: object
        properties:
          track_id:
            type: array
            items:
              $ref: '#/definitions/auditfile'
      track_id:
        type: json
    responses:
      200:
        description: A list of test filename with file ids for audit purpose
        schema:
          $ref: '#/definitions/auditfile'
        examples:
          rgb: ['red', 'green', 'blue']
    """

    auditfiles = dao.get_audit_files()
    result = auditfiles
    print("test - " + str(result))
    return result


@app.route('/v1/music/predictions/', methods=['POST'])
def upsert_Prediction():
    """
    This API let's you test music classification
    Call this api passing your test file and get the music classification results.

    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        required: true
        in: formData
        type: file
    definitions:
      predict_responses:
        type: string
    responses:
      500:
        description: ERROR Failed!
      200:
        description: INFO Success!
        schema:
          $ref: '#/definitions/predict_responses'
    """

    file = request.files['file']
    dao.get_dao(file.filename, file)
    response = jsonify({"status": "success"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

app.run(debug=True, port=8000)
