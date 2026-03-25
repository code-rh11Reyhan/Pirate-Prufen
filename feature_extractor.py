import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os

class VideoFeatureExtractor:
    def __init__(self):
        
        try:
            self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        except AttributeError:
            
            self.model = models.resnet50(pretrained=True)
        
        
        self.model = nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()
        
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def extract_frame_features(self, frame):
        """Extract feature vector from a single PIL Image"""
        try:
            img = self.transform(frame).unsqueeze(0).to(self.device)
            with torch.no_grad():
                features = self.model(img)
            return features.cpu().numpy().flatten()
        except Exception as e:
            print(f"Error extracting frame features: {e}")
            return None

    def process_video(self, video_path, sample_rate=10):
        """
        Extracts features from frames sampled at 'sample_rate' intervals.
        Returns a numpy array of feature vectors.
        """
        if not os.path.exists(video_path):
            return np.array([])
            
        cap = cv2.VideoCapture(video_path)
        features = []
        frame_count = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            
            if frame_count % sample_rate == 0:
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(frame_rgb)
                feat = self.extract_frame_features(pil_img)
                if feat is not None:
                    features.append(feat)
            
            frame_count += 1
        
        cap.release()
        
        if len(features) == 0:
            return np.array([])
            
        return np.array(features)