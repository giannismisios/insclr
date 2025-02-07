import torch
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm


def extract_batch_feature(model, inputs, scales):
    return torch.from_numpy(_multi_scale(model, inputs, scales))


def  extract_features(dataloader, model, device, scales):
    model.eval()    
    features = []
    with torch.no_grad():
        for batch in tqdm(dataloader):
            inputs = batch["input"]
            inputs2 = batch["input2"]
            # bug in pytorch 1.5?
            # when batch_size=1 in dataloader, inputs' shape is (C, H, W)
            # instead of (1, C, H, W)
            if len(inputs.size()) == 3:
                inputs = torch.unsqueeze(inputs, dim=0)
            
            inputs = inputs.to(device)
            inputs2 = inputs2.to(device)

            features.append(_multi_scale(model, inputs, inputs2, scales))

    features = np.concatenate(features, axis=0)
    return features


def _single_scale(model, inputs, inputs2, scale):
    """
    Args:
        inputs: (B, 3, H, W)
    """
    if abs(scale - 1.0) > 0.001:
        inputs = F.interpolate(inputs, scale_factor=scale, mode="bilinear", align_corners=False)
        inputs2 = F.interpolate(inputs2, scale_factor=scale, mode="bilinear", align_corners=False)
    with torch.no_grad():
        features, *_ = model(inputs)
        features2, *_ = model(inputs2)
        features = torch.cat((features, features2), 1) #concatenate features of the 2 branches
    return features.cpu().numpy()


def _multi_scale(model, inputs, inputs2, scales):
    features = None
    for scale in scales:
        _features = _single_scale(model, inputs, inputs2, scale)
        features = _features if features is None else features + _features
    
    if len(scales) > 1:
        features /= len(scales)
    features /= np.linalg.norm(features, axis=1, keepdims=True)
    return features
