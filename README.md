# NIRdehazing

Code for paper "Near-Infrared Fusion for Photorealistic Image Dehazing".

Presented at Electornic Imaging Conference 2018, Burlingame CA, on Januar 31 2018.

Authors:

- Frederke Dümbgen
- [Majed El Helou](https://majedelhelou.github.io/)
- Natalija Gucevska
- Sabine Süsstrunk

Last updated: 31.01.2018

## Requirements

Requires installation of OpenCV 3+. Can recommend [this](https://milq.github.io/install-opencv-ubuntu-debian/) guide for installing OpenCV 3+ for python on Ubuntu. 

Other libraries required (numpy, matplotlib) are listed in requirements.txt. Install by running:
```
pip install -r requirements.txt

```

## How to use

The pipeline for dehazing using photorealistic fusion can be found in pipeline.ipynb. 
Note that you need to run run_wls.py beforehand, creating the multiresolution 
decomposition of the image. Since this is a costly operation, it has to be done only once per image,
all detail and average images are stored for later use.  

## Contribute

Please report any bugs via this repository, and create pull requests if you wish to contribute. 

