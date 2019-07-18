# NIRdehazing

Code for the paper "[Near-Infrared Fusion for Photorealistic Image Dehazing](https://infoscience.epfl.ch/record/253201)".

Presented at the Electornic Imaging Conference 2018, Burlingame CA, on January 31 2018.

Authors:

- Frederke Dümbgen *
- [Majed El Helou](https://majedelhelou.github.io/) *
- Natalija Gucevska
- Sabine Süsstrunk

*the first two authors have equal contribution. 

Last updated: 18.07.2019

## Requirements

Requires installation of OpenCV 3+. We can recommend [this](https://milq.github.io/install-opencv-ubuntu-debian/) guide for installing OpenCV 3+ for Python on Ubuntu. 

Other libraries required (NumPy, Matplotlib) are listed in requirements.txt. Install by running:
```
pip install -r requirements.txt

```

## How to use

The pipeline for dehazing using photorealistic fusion can be found in pipeline.ipynb. 
Note that you need to run run_wls.py beforehand, creating the multiresolution 
decomposition of the image. Since this is a costly operation, it has to be done only once per image,
all detail and average images are stored for later use.  

## Datasets

The dataset used in this publication can be found here:  

- https://ivrl.epfl.ch/wp-content/uploads/2018/08/ImagesNIR.zip (12 NIR images)
- https://ivrl.epfl.ch/wp-content/uploads/2018/08/ImagesVIS1.zip (first 6 color images)
- https://ivrl.epfl.ch/wp-content/uploads/2018/08/ImagesVIS2.zip (second 6 color images)


## Contribute

Please report any bugs via this repository, and create pull requests if you wish to contribute. 

## Cite

Please cite the paper as 

```
@article{NIRDehazing,
      title = {Near-Infrared Fusion for Photorealistic Image Dehazing},
      author = {Dümbgen, Frederike and El Helou, Majed and Gucevska, Natalija and Süsstrunk, Sabine},
      journal = {IS&amp;T Electronic Imaging: Proceedings},
      pages = {321-1-321-5(5)},
      year = {2018},
      note = {First two authors have equal contribution},
      doi = {10.2352/ISSN.2470-1173.2018.16.COLOR-321}
}
```
