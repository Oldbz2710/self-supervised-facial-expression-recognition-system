import os
import torch
import torch.nn as nn
from torchvision import datasets
from torch.utils.data import DataLoader
from tqdm import tqdm
from arguments import get_args
from augmentations import get_aug
from models import get_model,get_backbone
from tools import AverageMeter
from optimizers import get_optimizer,LR_Scheduler

def main(args):
    #load test dataset
    train_dataset = datasets.ImageFolder(root='../dataset/archive/train',
                                         transform=get_aug(train=True,**args.aug_kwargs),)
    test_dataset = datasets.ImageFolder(root='../dataset/archive/test',
                                        transform=get_aug(train=False,train_classifier=False,**args.aug_kwargs))
    train_loader = DataLoader(dataset=train_dataset,shuffle=True,batch_size=args.train.batch_size,**args.dataloader_kwargs)
    test_loader = DataLoader(dataset=test_dataset,shuffle=False,batch_size=args.train.batch_size,**args.dataloader_kwargs)

    model = get_backbone(args.model.backbone)
    classifier = nn.Linear(model.output_dim,out_features=7,bias=True).to(args.device)

    assert args.eval_from is not None
    save_dict = torch.load(args.eval_from,map_location='cpu')
    msg= model.load_state_dict({k[9:]:v for k, v in save_dict['state_dict'].items() if k.startswith('backbone.')},strict=True)
    print(msg)
    model = model.to(args.device)
    model = nn.DataParallel(model)
    classifier = nn.DataParallel(classifier)
    optimizer = get_optimizer(
        args.eval.optimizer.name,
        classifier,
        lr=args.eval.base_lr*args.eval.batch_size/256,
        momentum=args.eval.optimizer.momentum,
        weight_decay=args.eval.optimizer.weight_decay,
    )
    lr_scheduler = LR_Scheduler(
        optimizer,
        args.eval.warmup_epochs,args.eval.warmup_lr*args.eval.batch_size/256,
        args.eval.num_epochs,args.eval.base_lr*args.eval.batch_size/256,args.eval.final_lr*args.eval.batch_size/256,
        len(train_loader)
    )
    loss_meter = AverageMeter(name='Loss')
    acc_meter = AverageMeter(name='Acc')

    global_process = tqdm(range(0,args.eval.num_epochs,desc=f'Evaluating'))
    for epoch in global_process:
        loss_meter.reset()
        model.eval()
        classifier.train()
        local_process = tqdm(train_loader,desc=f'Epoch {epoch}/{args.eval.num_epochs}',disable=True)

        for idx,(images,labels) in enumerate(local_process):
            classifier.zero_grad()
            with torch.no_grad():
                feature = model(images.to(args.device))
            preds = classifier(feature)
            loss = loss_meter(preds,labels.to(args.device))
            loss.backward()
            optimizer.step()
            loss_meter.update(loss.item())
            lr=lr_scheduler.step()
            local_process.set_postfix({'lr':lr,'Loss':loss_meter.val,'loss_avg': loss_meter.avg})
    classifier.eval()
    correct,total = 0,0
    acc_meter.reset()
    for idx,(images,labels) in enumerate(test_loader):
        with torch.no_grad():
            feature = model(images.to(args.device))
            preds = classifier(feature).argmax(dim=1)
            correct = (preds == labels.to(args.device)).sum().item()
            acc_meter.update(correct/preds.shape[0])
    print(f'Acc={acc_meter.avg*100:.2f}')
if __name__ == "__main__":
    main(args=get_args())