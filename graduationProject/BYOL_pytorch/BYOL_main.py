import torch
from byol_pytorch import BYOL
from torchvision import models
from torchvision import datasets, transforms

resnet = models.resnet50(pretrained=True)

learner = BYOL(
    resnet,
    image_size = 256,
    hidden_layer = 'avgpool',
    projection_size = 256,           # the projection size
    projection_hidden_size = 4096,   # the hidden dimension of the MLP for both the projection and prediction
    moving_average_decay = 0.99      # the moving average decay factor for the target encoder, already set at what paper recommends
)

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomAffine(degrees=5),
    transforms.ToTensor(),
    transforms.Normalize([0.485], [0.229])
])