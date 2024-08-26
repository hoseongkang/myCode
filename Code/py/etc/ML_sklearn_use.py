import joblib

text_clf = joblib.load('classify_address.pkl')

new_data = ["709동 404호"]

predicted_labels = text_clf.predict(new_data)

predicted_probabilities = text_clf.predict_proba(new_data)

for data, label, probs in zip(new_data, predicted_labels, predicted_probabilities):
    max_prob = max(probs)
    print(f"주소: {data}, 분류: {label}, 일치률: {max_prob}")


# text_clf = joblib.load('classify_address.pkl')
# new_data = ["한양수자인성남마크뷰 304-1501"]
# predicted_probabilities = text_clf.predict_proba(new_data)
# class_names = text_clf.classes_
# for data, probs in zip(new_data, predicted_probabilities):
#     print(f"주소: {data}")
#     for class_name, prob in zip(class_names, probs):
#         print(f"{class_name} 일치율: {prob*100:.2f}%")
