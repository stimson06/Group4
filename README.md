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


### Parikshit
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


1-20 Abhishek 
21-40 Stimson
41-60 Parikshit 
61-80 Ryan
81-100 Musab (Done)

left_01
right_01
forward_01
backward_01
