import torch
from .simsiam import SimSiam
from .backbones import resnet18_cifar_variant2

def get_backbone(backbone, castrate = True):
    backbone = eval(f"{backbone}()")

    if castrate:
        backbone.output_dim = backbone.fc.in_features
        backbone.fc = torch.nn.Identity()
    return backbone

def get_model(model_cfg):
    # 在此处添加模型
    if model_cfg.name == 'simsiam':
        model = SimSiam(get_backbone(model_cfg.backbone))
        if model_cfg.proj_layers is not None:
            model.projector.set_layers(model_cfg.proj_layers)
    else:
        raise NotImplementedError
    return model