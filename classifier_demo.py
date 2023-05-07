from project import fail_classifier_training

predicted, confidence = fail_classifier_training.classifyImage()
print(predicted)
print(confidence)