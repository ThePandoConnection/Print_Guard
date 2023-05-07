from project import fail_classifier_training

predicted, confidence = fail_classifier_training.classifyImage('demo')
print(predicted)
print(confidence)