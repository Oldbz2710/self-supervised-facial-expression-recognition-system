import cv2
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
from PIL import Image,ImageDraw,ImageFont
from sklearn.model_selection import train_test_split
from models import ResNet50Model,ViTBase16
img_size = 64
vit_img_size = 224
# targetx = 64
# targety = 64
epochs = 50
batch_size = 16

# transform = transforms.Compose([transforms.Resize((img_size,img_size)),
#                                 transforms.ToTensor(),
#                                 transforms.RandomHorizontalFlip(),])
transform_train = transforms.Compose([transforms.Resize((vit_img_size, vit_img_size)),
        transforms.RandomHorizontalFlip(p=0.3),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.RandomResizedCrop(vit_img_size),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),])
dataset = datasets.ImageFolder(root='./dataset/FERPlus/train', transform=transform_train)
train_df,test_df = train_test_split(dataset,test_size=0.2,random_state=42)
train_loader = DataLoader(dataset=train_df,batch_size=batch_size,shuffle=True)
test_loader = DataLoader(dataset=test_df,batch_size=batch_size,shuffle=True)


### resnet model
# model = ResNet50Model( num_classes=7)
# loss_func = nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=0.0001,weight_decay=0.01)
#
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# model.to(device)
# loss_func.to(device)
#
# train_loss=[]
# train_accuracy=[]
#
# for epoch in range(epochs):
#     model.train()
#     total_loss = 0
#     total_correct=0
#     total_samples = 0
#     for images, labels in train_loader:
#         images, labels = images.to(device), labels.to(device)
#         optimizer.zero_grad()
#         outputs = model(images)
#         loss = loss_func(outputs, labels)
#         loss.backward()
#         optimizer.step()
#         total_loss += loss.item()
#         _, predicted = outputs.max(1)
#         total_correct = predicted.eq(labels).sum().item()
#         total_samples+=labels.size(0)
#     avg_loss=total_loss/len(train_loader)
#     train_loss.append(avg_loss)
#     avg_accuracy=total_correct/total_samples
#     train_accuracy.append(avg_accuracy)
#
#     print(f'Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}, Accuracy: {avg_accuracy:.4f}')
# torch.save(model.state_dict(),'./models/resnet50.pth')
#
# test_loss = []
# test_accuracy = []
#
# for epoch in range(epochs):
#     model.eval()
#     total_loss = 0
#     total_correct=0
#     total_samples = 0
#     for images, labels in test_loader:
#         images, labels = images.to(device), labels.to(device)
#         outputs = model(images)
#         loss = loss_func(outputs, labels)
#         total_loss += loss.item()
#         _, predicted = outputs.max(1)
#         total_correct = predicted.eq(labels).sum().item()
#         total_samples += labels.size(0)
#     avg_loss = total_loss/len(test_loader)
#     test_loss.append(avg_loss)
#     avg_accuracy=total_correct/total_samples
#     test_accuracy.append(avg_accuracy)
#     print(f'Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}, Accuracy: {avg_accuracy:.4f}')


### vit model
model = ViTBase16(num_classes=7)
print(model)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001,weight_decay=0.01)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)
model.to(device)
criterion.to(device)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)
criterion.to(device)

train_loss = []
train_acc = []
import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
for epoch in range(epochs):
    print("Train Epoch {}/{}".format(epoch+1, epochs))
    epoch_loss = 0
    epoch_acc = 0
    model.train()
    for data, target in train_loader:
        data = data.to(device)
        target = target.to(device)
        optimizer.zero_grad()
        output = model.forward(data)
        loss = criterion(output, target)
        loss.backward()
        acc = (output.argmax(dim=1) == target).float().mean()
        epoch_loss += loss
        epoch_acc += acc
        train_loss.append(epoch_loss/len(train_loader))
        train_acc.append(epoch_acc/len(train_loader))
        optimizer.step()
    print(f'Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss/len(train_loader):.4f}, Accuracy: {epoch_acc/len(train_loader):.4f}')


val_loss = []
val_acc = []
for epoch in range(epochs):
    epoch_loss = 0
    epoch_acc = 0
    model.eval()
    for data, target in test_loader:
        data = data.to(device)
        target = target.to(device)
        with torch.no_grad():
            output = model(data)
            loss = criterion(output, target)
            acc = (output.argmax(dim=1) == target).float().mean()
            epoch_loss += loss
            epoch_acc += acc
            val_loss.append(epoch_loss/len(test_loader))
            val_acc.append(epoch_acc/len(test_loader))
    print(
        f'Epoch {epoch + 1}/{epochs}, Loss: {epoch_loss / len(test_loader):.4f}, Accuracy: {epoch_acc / len(test_loader):.4f}')
