import cv2
import numpy as np
from matplotlib import pyplot as plt


def find_matching_points(img1, img2, method='sift', match_method='bf', plot=False):
    '''
    Find matching points in img1 and img2.
    
    '''
    if method == 'orb':
        # Initiate ORB detector
        detector = cv2.ORB_create()
        norm = cv2.NORM_HAMMING
    elif method == 'sift':
        # Initiate SIFT detector
        detector = cv2.xfeatures2d.SIFT_create()   
        #Since SIFT returns a detectorType() of CV32F (=float) 
        #you cannot use any Hamming-distance as matcher. 
        #Hamming-distance works only for binary feature-types like ORB
        norm = cv2.NORM_L2

    # find the keypoints and descriptors
    kp1, des1 = detector.detectAndCompute(img1,None)
    kp2, des2 = detector.detectAndCompute(img2,None)
    print('{},{} keypoints found in img1, img2.'.format(len(kp1), len(kp2)))
    
    #define matcher
    if match_method == 'bf': 
         matcher = cv2.BFMatcher(norm, crossCheck=True)
    elif match_method == 'flann':
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary
        matcher = cv2.FlannBasedMatcher(index_params, search_params)
    
    # Match descriptors.
    matches = matcher.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    print('{} matches found.'.format(len(matches)))
    if (plot):
        # Draw first 10 matches.
        img3 = img1.copy()
        img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], img3, flags=2)
        plt.imshow(img3),plt.show()
        cv2.imwrite('output/matches_' + method + '.jpg',img3)

    # Find homography
    points1 = [kp1[match.queryIdx].pt for match in matches]
    points2 = [kp2[match.trainIdx].pt for match in matches]
    return np.array(points1), np.array(points2)

def registration(img1, img2, method='sift', match_method='bf', plot=False):
    '''
    Align img2 with img1.
    
    '''
    pts1, pts2 = find_matching_points(img2, img1, method, match_method, plot)
    M, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
    img2_aligned = cv2.warpPerspective(img2, M, (img2.shape[1], img2.shape[0]))
    return img2_aligned
