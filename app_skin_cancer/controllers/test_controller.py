from vit_controller import vit_inference
from config import settings

# generate the model
model = vit_inference

# make the prediction
img_path = "controllers/images/ISIC_9999251.JPG"
class_pred, label_pred, probs = model.predict(img_path)

# print predictions
print(f"predicted class: {label_pred}")
print(f"probability: {probs[class_pred]:.4f}")
print(f"list of probs: {probs}")

# generate probability distribution
model.plot_probs(settings["class_names"], probs)
