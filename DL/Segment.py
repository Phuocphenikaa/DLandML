import torch
import torch.nn as nn
import torchvision.transforms as transforms

class DoubleConv(nn.Module):
    def __init__(self,in_features,out_features):
        super(DoubleConv,self).__init__()
        self.conv_layer = nn.Sequential(
            nn.Conv2d(in_features,out_features,3,1,1,bias = False),
            nn.BatchNorm2d(out_features),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_features,out_features,3,1,1,bias=False),
            nn.BatchNorm2d(out_features),
            nn.ReLU(inplace=True)
        )
    def forward(self,x):
        x = self.conv_layer(x)
        return  x
class Unet(nn.Module):
    def __init__(self,in_channels = 1,out_channels = 1,size_image = (572,572)):

        super(Unet,self).__init__()


        features = [64,128,256,512]

        self.downsample = nn.ModuleList()
        self.upsample = nn.ModuleList()

        for feature in features:
            self.downsample.append(DoubleConv(in_channels,feature))
            self.downsample.append(nn.MaxPool2d(2,2))
            in_channels = feature

        self.bottom_layer = DoubleConv(in_channels,1024)

        in_channels = 1024

        for feature in reversed(features):
            self.upsample.append(nn.ConvTranspose2d(in_channels,feature,2,2,bias=False))
            self.upsample.append(DoubleConv(feature*2,feature))
            in_channels = feature

        self.end_layer = nn.Conv2d(in_channels,out_channels,1,1,0)
    def forward(self,x):

        res = [] # skip conections

        for i in range(0,len(self.downsample),2):
            x = self.downsample[i](x)
            res.append(x)
            x = self.downsample[i+1](x)

        x = self.bottom_layer(x)

        res = res[::-1] #reverse res

        for i in range(0,len(self.upsample),2):

            x = self.upsample[i](x)
            x = torch.concat((res[i//2],x),dim = 1) #concatconetions
            x = self.upsample[i+1](x)

        x = self.end_layer(x)

        return x

model = Unet()
x = torch.rand((3,1,512,512))
print(model(x).shape)

