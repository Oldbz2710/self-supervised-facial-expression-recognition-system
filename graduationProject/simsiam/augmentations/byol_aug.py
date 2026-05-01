import torchvision.transforms
from torchvision import transforms
from PIL import Image,ImageOps
from .gaussian_blur import GaussianBlur
torchvision.transforms.GaussianBlur = GaussianBlur

imagenet_norm = [[0.485, 0.456, 0.406],[0.229, 0.224, 0.225]]
class BYOL_transform:
    def __init__(self, image_size,normalize=imagenet_norm):
        self.transfrom1 = transforms.Compose([
            transforms.RandomResizedCrop(image_size,scale=(0.08,1.0),ratio=(0.75,4/3),interpolation=Image.BICUBIC),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomApply([transforms.ColorJitter(0.4,0.4,0.2,0.1)],p=0.8),
            transforms.RandomGrayscale(p=0.2),
            transforms.ToTensor(),
            transforms.Normalize(*normalize)
        ])
        self.transfrom2 = transforms.Compose([
            transforms.RandomResizedCrop(image_size, scale=(0.08, 1.0), ratio=(0.75, 4/3),
                                         interpolation=Image.BICUBIC),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomApply([transforms.ColorJitter(0.4, 0.4, 0.2, 0.1)], p=0.8),
            transforms.RandomGrayscale(p=0.2),
            transforms.RandomApply([transforms.GaussianBlur(kernel_size=image_size//20*2+1,sigma=(0.1,2.0))], p=0.1),
            transforms.ToTensor(),
            transforms.Normalize(*normalize)
        ])
    def __call__(self,img):
        img1=self.transfrom1(img)
        img2=self.transfrom2(img)
        return img1,img2

class Transform_single:
    def __init__(self,image_size,train,normalize=imagenet_norm):
        self.denormalize = Denormalize(*imagenet_norm)
        if train == True:
            self.transfrom = transforms.Compose([
                transforms.RandomResizedCrop(image_size, scale=(0.08, 1.0), ratio=(0.75, 4/3),
                                             interpolation=Image.BICUBIC),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize(*normalize)
            ])
        else:
            self.transfrom = transforms.Compose([
                transforms.Resize(int(image_size*(8/7)),interpolation=Image.BICUBIC),
                transforms.CenterCrop(image_size),
                transforms.ToTensor(),
                transforms.Normalize(*normalize)
            ])
    def __call__(self,img):
        return self.transfrom(img)