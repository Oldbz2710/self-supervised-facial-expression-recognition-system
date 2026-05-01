import base64
from PIL import Image
from io import BytesIO
from flask import Flask, request
import numpy as np
from torchvision import datasets, transforms, models
import torch
import torch.nn as nn
import cv2

transforms = transforms.Compose([transforms.ToTensor(),transforms.Resize((224, 224)),transforms.Normalize([0.485], [0.229])])
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
def predict_img(modelName,mode,path):
    import os
    print("start prediction")
    if modelName == 'custom_efficientnet':
        model_path = r"./models/customEfficientModel_FETD.pth"

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = CustomEfficientNet().to(device)
        if mode == 'single predict':
            # 拆分base64编码，仅保留context部分
            head, context = path.split(",")
            # print(context)
            img = base64.b64decode(context)
            img_arr = np.fromstring(img, np.uint8)
            image = cv2.imdecode(img_arr, cv2.COLOR_RGB2BGR)
            # print('image shape length',len(image.shape))
            if (len(image.shape) == 2):
                # 保持channel数量与模型训练时输入一致（3通道）
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            img_tensor = transforms(image)
            print('img_tensor', img_tensor.shape)
            model_path = r"./models/customEfficientModel.pth"
        print(model_path)
        model.load_state_dict(torch.load(model_path, map_location=device))
        # print("model has been selected: customEfficient")

        if img is None:
            print('No image found')
        else:
            model.eval()
            img_tensor = img_tensor.to(device)
            img_tensor = img_tensor.unsqueeze(0)
            output = model(img_tensor)
            _, predicted = torch.max(output.data, 1)
            print(predicted,predicted.item())
            classList=["愤怒","厌恶","恐惧","高兴","平和","悲伤","惊讶"]
            return classList[predicted.item()]
def predict_img_list(modelName,mode,path):
    import os
    print("start prediction list")
    if modelName == 'custom_efficientnet':

        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model = CustomEfficientNet().to(device)
        if mode == 'folder':
            # 拆分base64编码，仅保留context部分
            replyList=[]
            for i in range(len(path)):
                img_src = path[i]
                head, context = img_src.split(",")
                # print(context)
                img = base64.b64decode(context)
                img_arr = np.fromstring(img, np.uint8)
                image = cv2.imdecode(img_arr, cv2.COLOR_RGB2BGR)
                model_path = r"./models/customEfficientModel_FETD.pth"
                # print('image shape length',len(image.shape))
                if (len(image.shape) == 2):
                    # 保持channel数量与模型训练时输入一致（3通道）
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                    img_tensor = transforms(image)
                    print('img_tensor', img_tensor.shape)
                    model_path = r"./models/customEfficientModel.pth"
                model.load_state_dict(torch.load(model_path, map_location=device))
                # print("model has been selected: customEfficient")

                model.eval()
                img_tensor = img_tensor.to(device)
                img_tensor = img_tensor.unsqueeze(0)
                output = model(img_tensor)
                _, predicted = torch.max(output.data, 1)
                print(predicted,predicted.item())
                classList=["愤怒","厌恶","恐惧","高兴","平和","悲伤","惊讶"]
                replyList.append(classList[predicted.item()])
            return replyList
app = Flask(__name__)

#模型预测
@app.route('/predict',methods=['POST'])
def prediction():
    if request.method == 'POST':
        list = request.get_json()
        prediction = predict_img(list['modelName'],list['mode'],list['path'])
        return str(prediction)
@app.route('/predictGroup',methods=['POST'])
def predictionGroup():
    if request.method == 'POST':
        list = request.get_json()
        predictionList = predict_img_list(list['modelName'],list['mode'],list['path'])
        return predictionList
if __name__ == '__main__':
    app.run()