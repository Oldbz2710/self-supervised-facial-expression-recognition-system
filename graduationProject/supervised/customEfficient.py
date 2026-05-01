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
from tqdm import tqdm
from torch.utils.tensorboard import SummaryWriter

data_path = '../dataset/FERPlus'
train_dir = os.path.join(data_path,'train')
test_dir = os.path.join(data_path,'test')


tranform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomAffine(degrees=5),
    transforms.ToTensor(),
    transforms.Normalize([0.485], [0.229])
])

def load_data(directory):
    return datasets.ImageFolder(root=directory, transform=tranform)
train_dataset = load_data(train_dir)
test_dataset = load_data(test_dir)
train_size = int(0.8*len(train_dataset))
val_size = len(train_dataset)-train_size

train_subset, val_subset = random_split(train_dataset, [train_size, val_size])
train_loader = DataLoader(train_subset, batch_size=128, shuffle=True)
val_loader = DataLoader(val_subset, batch_size=128, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=True)
logger = SummaryWriter(log_dir='../models/log')
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
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, factor=0.5, patience=3, verbose=True)

def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler,num_epochs=70):
    train_losses=[]
    val_losses=[]
    train_accuracies=[]
    val_accuracies=[]
    best_val_accuracy=0.0
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        for images, labels in tqdm(train_loader):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_train += labels.size(0)
            correct_train+=(predicted==labels).sum().item()
        epoch_loss = running_loss/len(train_loader)
        epoch_accuracy = correct_train/total_train*100
        train_losses.append(epoch_loss)
        train_accuracies.append(epoch_accuracy)
        val_loss,val_accuracy = validate_model(model, val_loader)
        val_accuracies.append(val_accuracy)
        val_losses.append(val_loss)
        print(f'Epoch[{epoch+1}/{num_epochs}],'
              f'Train Loss: {epoch_loss:.4f},'
              f'Train Accuracy: {epoch_accuracy:.2f}%,'
              f'Val Loss: {val_loss:.4f},'
              f'Val Accuracy: {val_accuracy:.2f}%')
        logger.add_scalar('train_loss', epoch_loss, epoch+1)
        logger.add_scalar('train_accuracy', epoch_accuracy, epoch+1)
        logger.add_scalar('val_loss', val_loss, epoch+1)
        logger.add_scalar('val_accuracy', val_accuracy, epoch+1)
        scheduler.step(val_loss)
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            torch.save(model.state_dict(), '../models/customEfficientModel.pth')
            print('Model improved, saved to dict')
def validate_model(model, val_loader):
    model.eval()
    running_loss = 0.0
    correct_val=0
    total_val=0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total_val += labels.size(0)
            correct_val+=(predicted == labels).sum().item()
    val_loss = running_loss/len(val_loader)
    val_accuracy = correct_val/total_val*100
    return val_loss, val_accuracy

train_losses,train_accuracies,val_losses,val_accuracies=train_model(model,train_loader,val_loader,criterion,optimizer,scheduler,num_epochs=70)


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


# Test the model on the test dataset and get predictions after training is complete.
true_labels, predictions = test_model(model, test_loader)


def plot_confusion_matrix(true_labels, predictions):
    cm = confusion_matrix(true_labels, predictions)

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names,
                yticklabels=class_names)

    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.show()
    plt.savefig('Custom Efficient Confusion Matrix.png')


# Define class names corresponding to emotions
class_names = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Plot the confusion matrix after testing the model
plot_confusion_matrix(true_labels, predictions)

# Print classification report for detailed performance metrics
print(classification_report(true_labels, predictions))