# Hand Gesture Detection 
Dectect the hand gesture (Left, Right, Up or Down) and turn on the LED using the I/O pins

# Requirements
- ## Software Requirements
    - [OpenMV IDE](https://openmv.io/pages/download?srsltid=AfmBOoqqQOKlNj1aivOZZpxfx6Zg_1ny7cqYO_99kxVEwimPfCVBPElF)
  to run the code

- ## Hardware Requirements
  - [OpenMV RT 1062](https://openmv.io/products/openmv-cam-rt?gad_source=1&gad_campaignid=23516406659&gbraid=0AAAAADOSICryFgLm1M5Oh1GLy3zOFfZN7&gclid=CjwKCAjwtcHPBhADEiwAWo3sJszJLGAS7zwRKzvMOKSZOVvNGGk_ErYrzA7MBv_XrhWebFIZ6uQqfRoCaSwQAvD_BwE)
  - [Esp 32](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp-dev-kits-en-master-esp32.pdf)
  - 4 LED Bulbs
  - Wires
  - Bread board

## Files
- `Snapshot.py`- To collec the photos
- `data_augmentation.ipynb` - Data augmentation performed on Kaggale dataset for our application ([Dataset](https://www.kaggle.com/datasets/ryanbijujoseph/hand-gesture-dataset))
- `gesture_led_wifi.py` - 
- `models/model 1` - Fine tued Pre-trained model using MobileNet V2 using [Edge Impulse](https://www.edgeimpulse.com)
- `models/model 2` - A simple CNN architecture build using Edge Impulse.

## Steps to Recreate
- Connect the OpenMV device to the system
- Copy the `gesture_led_wifi.py`, model 1/model 2, labels.txt file onto the OpenMV device
- Update the IP address of the device the Esp 32 is connected.
- Run the code

## Output
- Image or a short video

## Contribution
### Stimson
- 19 Apr
  - Added `Snapshot.py` for data collection
      - NOTES: The folder will be created on the OpenMV device under the folder 'handset_dataset'. Once all the files are created please move it to the 'dataset' folder in the repo. Make sure to use the dataset numbering as discussed in the group.
    - BUG FIX: `Snapshot.py` - updated the horizontal mirror to reflect proper direction.
- 20 Apr
    - Added Data for each class numbering from 21 to 40

### Custom model Development with Ryan
#### **Model Iteration & Performance**
|Iteration| Timeline | Strategy | Train Acc. | Test Acc. | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1 (Initial)** | 21 to 23 Apr  |Base collected data | 79.5%| 82.2% | Directional classes > 80%; "Unknown" class at 50%  |
| **V2 (Hybrid)** | 24 to 25 Apr |50% Original + 50% Augmented  | 69.0%  | 61.03%  | Attempted to reduce background bias  |
| **V3 (Final)** |26 to 27 Apr|Entire Augmented Dataset  | **96.9%**  | **94.8%**  | Achieved peak performance; noted plane background bias . |


### Ryan 
- 18 - 19 Apr    
    - Have understood and agreed to the project. Github repo is created and is added people.
    - Everyone create their own python file and we work on it separately. So we dont overlap also we can pull and see each other work.
    - I have added a file for my python file Ryan.py and I have added a print statement to test it.
    - I had an issue with the saving the snap so I changed the snapshot code to a different one. If anyone else also facing the issue I have uploaded the code separately. So it doesnt get mixed.
- 20 Apr
    - I have created my data set. I would like you all to check the dataset and let me know if there is any changes or if any improvements.
    - The dataset is created under the `handset_dataset` folder. My sample number as discussed starts from 61-80.
- 23–24 April
  - Dataset downloaded from Kaggle (via Musab). It contained ~9 gesture classes (e.g., thumb, index).
  - Each class was manually inspected and re-labeled into directional categories: **forward, backward, left, right, unknown**.
  -  Images were reorganized into new class folders:
      - Forward: ~7,800 images  
      - Right: ~1,800 images  
      - Unknown: ~9,800 images  
  - To address class imbalance, data augmentation (e.g., rotation) was applied:
  - Right-class images were transformed to simulate other directions (e.g., forward).
  - Forward class diversity increased (4 → 5 variations).
  - Augmentation applied across all directional classes → ~9,600 images per class.
  - Dataset shuffled; **2,500 images per class** selected → stored in `augmented data`.
  - Dataset link: https://www.kaggle.com/datasets/ryanbijujoseph/augmented-hand-data/data  

- 25 April
  - Processed the **unknown** class (previously excluded from balancing).
  - Original unknown dataset: ~9,800 + 100 custom images.
  - Augmented into 3 orientations → ~29,400 images.
  - Randomly selected **2,500 images** and added custom images → final unknown class.
  - All classes (forward, backward, left, right, unknown) balanced.
  - Final dataset: ~2,600 images per class.
  - Old dataset deleted; new dataset uploaded:
    - https://www.kaggle.com/datasets/ryanbijujoseph/hand-gesture-dataset
  - `data_augmentation.ipynb` includes code (last cell) to download and save dataset automatically.
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
