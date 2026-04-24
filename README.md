# Group4 - Handset Detection 
Dectect the hand gesture (Left, Right, Up or Down) and turn on the LED using the I/O pins

## Contribution
### Stimson
- 19 Apr
    - Added `Snapshot.py` for data collection
        - NOTES: The folder will be created on the OpenMV device under the folder 'handset_dataset'. Once all the files are created please move it to the 'dataset' folder in the repo. Make sure to use the dataset numbering as discussed in the group.
    - BUG FIX: `Snapshot.py` - updated the horizontal mirror to reflect proper direction.
- 20 Apr
    - Added Data for each class numbering from 21 to 40 set it up as a small quiz to complete over the next couple of days for


### Ryan 
- Have understood and agreed to the project. Github repo is created and is added people.
- Everyone create their own python file and we work on it separately. So we dont overlap also we can pull and see each other work.
- I have added a file for my python file Ryan.py and I have added a print statement to test it.
- I had an issue with the saving the snap so I changed the snapshot code to a different one. If anyone else also facing the issue I have uploaded the code separately. So it doesnt get mixed.
- I have created my data set. I would like you all to check the dataset and let me know if there is any changes or if any improvements.
- The dataset is created under the `handset_dataset` folder. My sample number as discussed starts from 61-80.
- The dataset obtained by Musab from Kaggle was accessed and downloaded for further processing. The dataset was originally organized into multiple classes representing different hand gestures (e.g., index finger, thumb), comprising approximately nine distinct categories. Each class was manually reviewed by inspecting the images within its respective folder to determine the directional gesture it represented, such as forward, backward, left, right, or unknown.

- Following this inspection, images corresponding to each directional category were reorganized accordingly. For instance, all images identified as representing the “forward” gesture were copied into a dedicated forward class folder. This process resulted in an initial distribution of approximately 7,800 images for the forward class, 1,800 images for the right class, and around 9,800 images categorized as unknown.

- To address class imbalance and improve model performance, data augmentation techniques were applied. Since an equal number of samples was required across all classes, and excessive data volume was unnecessary, augmentation was used to generate additional samples. Specifically, images from the right class (e.g., thumb pointing right) were transformed through rotation and other augmentation methods to simulate forward gestures (e.g., upward direction). These augmented images were then incorporated into the forward class. As a result, while the right class initially contained only a single variation, the forward class was enriched with multiple variations (increasing from four to five distinct visual patterns).

- Subsequently, similar augmentation strategies were applied to generate balanced representations for all directional classes, including left, right, forward, and backward. This process yielded approximately 9,600 images per class. Finally, the dataset was randomized, and a subset of 2,500 images from each class was selected and consolidated into a separate folder labeled “augmented data” for model training and evaluation.
- Augmented data can be found here https://www.kaggle.com/datasets/ryanbijujoseph/augmented-hand-data/data

### Parikshit
- 12 APR Cloned the repo
- 20 APR 2026
    - Set up my working branch (parikshit-dataset-41-60).
- 21 Apr 2026
    - Uploaded/updated my dataset images in handset_dataset/ for my allocation 41–60 (Left / Right / Forward / Backward / Unknown) following the agreed naming convention (e.g., left_41.jpg … unknown_60.jpg).
    - Pushed the dataset with 20 images per class.
    - Added collect_photos.py (script I used to capture/collect the images for the dataset).
- Have cloned the repo.

### Musab
- 20-April
    - Pulled Snapshot.py. Run on OpenMV. 
    - Forgot to remove lens cap and "took" photos initially. Was pointed out by roomate
    - Encountered corrupted photos and unable to access files on device flash
    
- 21-April
    - Added file handling to snapshot.py to fix corrupted files. 
    - Updated dataset 80-100 with 4 specified classes.
    - Added Unknown class of variables as discussed on call
    - Suggest using https://www.kaggle.com/datasets/gti-upm/leapgestrecog/data to populate classes for more data variety


### Abhishek
- 18 April 2026
  - Cloned the repo
- 20 April 2026
  - Reviewed Ryan's PR
- 21 April 2026
  - Cleared extra code from  repo and Pushed Dataset to repo



### DATASET NUMBER ALLOCATION
1-20 Abhishek 
21-40 Stimson
41-60 Parikshit 
61-80 Ryan
81-100 Musab (Done)

### DATASET LABEL NAMING CONVENTION
left_01
right_01
forward_01
backward_01
unknown_01
