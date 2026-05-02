#Self-Supervised Facial Expression Recognition System
##Overview

This project focuses on improving performance under limited labeled data by applying self-supervised learning techniques.
The system allows users to upload images for prediction and visualize model results through an interactive web interface.

##Features
Image-based facial expression prediction
Visualization of prediction results
Comparison of different training strategies
Modular frontend-backend architecture
##Tech Stack
Frontend: Vue2, Element-UI, ECharts
Backend: Flask server
Machine Learning: PyTorch
Model & Method

The project explores self-supervised learning to address data scarcity in facial expression recognition.
Key approaches include:
CNN-based baseline model
Contrastive learning (MoCo-style framework)
Data augmentation techniques
Learning rate scheduling
These methods aim to improve representation learning and model robustness.

##System Architecture
Frontend (Vue) → Backend API (Flask) → Model Inference (PyTorch)

##Repository Structure
frontend/                              # Web interface (Vue)
graduationProject/"modelName"          # Training and inference code
graduationProject/flask_app.py         # server
present_demo/                                  # Screenshots and results

##How to Run
Backend
flask run

##Frontend
cd frontend
npm install
npm run serve

##Note on Model Weights
Model weights are not included due to GitHub file size limitations.
Please train the model provided by the original paper.
the training command is in graduationProject/execute command.txt

##demo
/present_demo/2-1systemtest2.png
/present_demo/3-2model_test.mp4
