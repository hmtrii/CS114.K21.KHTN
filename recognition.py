pip install --upgrade "watson-developer-cloud>=2.4.1"
pip install simplejson
import json

from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='1ILZkyzgNMH6FTgPJ8WtT6WR4scQj_LNmkHRFsMN78Pj')

with open('/content/image4.png', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        threshold='0.6',
	classifier_ids='default').get_result()
print(json.dumps(classes, indent=2))
