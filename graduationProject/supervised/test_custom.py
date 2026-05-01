import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from torchvision import datasets, transforms, models
from torch.utils.data import Dataset, DataLoader, random_split
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# data_path = '../dataset/FERPlus'
# train_dir = os.path.join(data_path,'train')
# test_dir = os.path.join(data_path,'test')

transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomAffine(degrees=5),
    transforms.ToTensor(),
    transforms.Normalize([0.485], [0.229])
])

#数据集导入
# def load_data(directory):
#     return datasets.ImageFolder(root=directory, transform=tranform)
# train_dataset = load_data(train_dir)
# test_dataset = load_data(test_dir)
dataset = datasets.ImageFolder(root='../dataset/FETD/train', transform=transform)
train_dataset,test_dataset = train_test_split(dataset,test_size=0.2,random_state=42)
train_size = int(0.8*len(train_dataset))
val_size = len(train_dataset)-train_size
train_subset, val_subset = random_split(train_dataset, [train_size, val_size])
train_loader = DataLoader(train_subset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=True)
train_size = int(0.8*len(train_dataset))
val_size = len(train_dataset)-train_size

#模型加载
class CustomEfficientNet(nn.Module):
    def __init__(self):
        super(CustomEfficientNet, self).__init__()
        self.model = models.efficientnet_b0(pretrained=True)
        num_ftrs = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(num_ftrs, 7)
        self.dropout = nn.Dropout(p=0.5)
        self.batch_norm = nn.BatchNorm1d(num_features=7)
    def forward(self, x):
        x = self.model(x)
        x = self.dropout(x)
        return self.batch_norm(x)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = CustomEfficientNet().to(device)
model.load_state_dict(torch.load("../models/customEfficientModel_FETD.pth"))

#模型测试
def test_model(model, test_loader):
    model.eval()  # Set model to evaluation mode

    all_labels = []
    all_predictions = []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            all_labels.extend(labels.cpu().numpy())
            all_predictions.extend(predicted.cpu().numpy())

    return np.array(all_labels), np.array(all_predictions)

true_labels, predictions = test_model(model, test_loader)

#绘制混淆矩阵
def plot_confusion_matrix(true_labels, predictions):
    cm = confusion_matrix(true_labels, predictions)

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names,
                yticklabels=class_names)

    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()
    plt.savefig('Custom Efficient FETD Confusion Matrix.png')


# Define class names corresponding to emotions
class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Plot the confusion matrix after testing the model
plot_confusion_matrix(true_labels, predictions)

# Print classification report for detailed performance metrics
print(classification_report(true_labels, predictions))