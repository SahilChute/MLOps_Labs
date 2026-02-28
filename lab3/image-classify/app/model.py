import torch
from torchvision import models, transforms
from PIL import Image
import urllib.request
import json

# Load ImageNet labels
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
with urllib.request.urlopen(LABELS_URL) as f:
    LABELS = json.load(f)

# Load pre-trained ResNet50
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.eval()

# Standard ImageNet transforms
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict(image: Image.Image, top_k: int = 5) -> list[dict]:
    tensor = transform(image).unsqueeze(0)  # Add batch dim
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.nn.functional.softmax(outputs[0], dim=0)
    
    top = torch.topk(probs, top_k)
    return [
        {"label": LABELS[idx], "confidence": round(score.item(), 4)}
        for score, idx in zip(top.values, top.indices)
    ]