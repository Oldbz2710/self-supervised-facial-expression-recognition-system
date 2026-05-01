import torch
import torch.nn as nn
import torchvision.models as models
import timm

num_classes = 7
RESNET_MODEL_PATH = './models/resnet.pth'
VIT_MODEL_PATH = './models/vit.pth'
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
class ResNet50Model(nn.Module):
    def __init__(self,num_classes):
        super(ResNet50Model, self).__init__()
        self.resnet50 = models.resnet50(pretrained=True)
        num_ftrs = self.resnet50.fc.in_features
        self.resnet50.fc = nn.Linear(num_ftrs, num_classes)
    def forward(self, x):
        return self.resnet50(x)

class ViTBase16(nn.Module):
    def __init__(self,num_classes,pretrained=False):
        super(ViTBase16, self).__init__()
        self.model = timm.create_model("vit_base_patch16_224", pretrained=False)
        if pretrained:
            self.model.load_state_dict(torch.load(VIT_MODEL_PATH))
        self.model.head == nn.Linear(self.model.head.in_features,num_classes)
    def forward(self,x):
        x = self.model(x)
        return x
