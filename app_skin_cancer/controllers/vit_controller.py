# import packages
import torch
from torch import nn
from transformers import ViTImageProcessor
from torchvision.transforms import (Compose, 
                                    Normalize,
                                    Resize, 
                                    ToTensor)
import torch.nn.functional as F
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
import logging 

from transformers import ViTForImageClassification

# import classifier
from controllers.dnn_classifier import CustomClassifier

# get settings
from controllers.config import settings, id2label, label2id

# write loggers
logger = logging.getLogger(__name__)


#                   --- class of ViTModel ---
class ViTModel(torch.nn.Module):
    def __init__(self, num_labels=7):
        super(ViTModel, self).__init__()
        self.vit = ViTForImageClassification.from_pretrained(settings["list_models"]["vit-L/32"],
                                                              num_labels=len(settings["class_names"]),
                                                              id2label=id2label,
                                                              label2id=label2id,
                                                              ignore_mismatched_sizes = True)
        custom_classifier = CustomClassifier(in_features = 1024,
                                             hidden_features = [512, 256, 64],
                                             out_features = num_labels)
        self.vit.classifier = custom_classifier
        
    def forward(self, pixel_values):
        outputs = self.vit(pixel_values=pixel_values)
        return outputs.logits

    def total_parameters(self):
      return sum(p.numel() for p in self.parameters())


#               --- class of inference engine ---
class ViTInferenceEngine:
    def __init__(self):
        logger.info("Start to load model...")
            
        # load preprocessor
        self.processor = ViTImageProcessor.from_pretrained(
            settings["list_models"]["vit-L/32"]
        )
        self.image_mean = self.processor.image_mean
        self.image_std = self.processor.image_std
        self.image_size = self.processor.size["height"]

        # load vector of class names and indexes
        self.class_names = settings["class_names"]
        
        # load model
        logger.info("Loading model...")
        self.model = ViTModel()

    # function to preprocessing input
    def preprocess_image(self, img_path):
        logger.info("Preprocessing step...")
        # make normalization operation
        normalize = Normalize(mean = self.image_mean,
                              std = self.image_std)
        # create test transformation
        test_transforms = Compose([
            Resize((self.image_size, self.image_size)),
            ToTensor(),
            normalize
        ])
        # load image
        img = Image.open(img_path)

        # convert to tensor of pixels
        img_pixel = test_transforms(img.convert("RGB"))
        img_pixel = img_pixel.unsqueeze(0)

        return img_pixel

    # function to rename keys in state dicts
    def rename_keys(self, state_dict, old_prefix, new_prefix):
        new_state_dict = {}
        for key, value in state_dict.items():
            if key.startswith(old_prefix):
                new_key = new_prefix + key[len(old_prefix):]
                new_state_dict[new_key] = value
            else:
                new_state_dict[key] = value
        return new_state_dict

    # function to build architecture
    def load_model(self):        
        # load parameters
        model_params = torch.load("controllers/ai_inference/vitL_p32_v13_isic027.pt",
                                  map_location = torch.device('cpu'))

        # remove parallelization
        if isinstance(model_params, nn.DataParallel):
            model_params = model_params.module

        # reconfiguration of dictionary's layers
        new_model_params = self.rename_keys(
            state_dict = model_params,
            old_prefix = 'module.',
            new_prefix = ''
        )

        self.model.load_state_dict(new_model_params)

    # function to make prediction
    def predict(self, img_path):
        # preprocess image
        logger.info("Preprocessing input...")
        image = self.preprocess_image(img_path)
        # load weights and biases of model
        self.load_model()
        # put model in evaluation mode
        self.model.eval()

        logger.info("Generating prediction...")
        # get predictions
        output = self.model.forward(image)
        # take probabilities
        probs = F.softmax(output, dim = 1)
        # squeeze tensor
        probs = probs.flatten()
        # convert to numpy array
        probs = probs.detach().numpy()
        # get class-prediction
        class_pred = np.argmax(probs)
        # get label-prediction
        label_pred = settings["class_names"][class_pred]
        
        return class_pred, label_pred, probs.tolist()
    
    # function to plot probability distribution
    def plot_probs(self, labels, probs):    
        logger.info("Plotting results...")
        # index of classes
        class_idx = np.arange(len(labels))
        plt.barh(class_idx, probs, color = 'skyblue')
        plt.xlabel('Probabilities')
        plt.ylabel('Skin Cancer')
        plt.title('Classification ranking')
        plt.yticks(class_idx, labels)

        # Annotate each bar with the percentage value
        for i, v in enumerate(probs):
            plt.text(v + 0.01, i, f'{v*100:.2f}%', color='black', va='center')
            
        plt.show()

# object of ViTInferenceEngine
vit_inference = ViTInferenceEngine()
