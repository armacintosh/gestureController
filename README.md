# gestureController

Adaptive gesture-based game controller for people with unique neuromuscular profiles. Provides in-game calibration and classification setup using Myo Armband. Interact with games by custom gestures and keypress mapping.

Main files from which others are called:
-	Base                                > PlayMyoDashy.m
-	Base_withThreshold and Classifier   > A_GestCal_Home.m

# Notes: 
-	Scripts are in development. They are not expected to run out of the box and have not been optimized. 
-	Both folder stream and process raw data from Myo and convert them to gestures and custom mapped keypress actions. Base_withThreshold and Classifier additionally includes extended calibration for 3 gestures, custom threshold detection and profiling, and classification model building.
-	The game that this controller was built for cannot be included here. However, key pass functions are generic and configurable. They can be linked with other games.
-	Matlab scripts currently available 
-	Python scripts to come.

# Citation:
If you use any of the resources provided on this page in any of your publications, we ask you to cite the following work.

MacIntosh A, Vignais N, Desailly E, Biddiss E, Vigneron V. (2019). A classification and calibration procedure for gesture specific home-based therapy exercise in youth with Cerebral Palsy. in prep to IEEE Transactions on Neural Systems and Rehabilitation Engineering, September 2019.

MacIntosh A, Vignais N, Vigneron V, Fay L, Musielak A, Desailly E, Biddiss E. (2019). The design and evaluation of biofeedback in motor therapy gaming. Submitted to Assistive Technology, July 2019.

This repository uses other tools including (full references embedded):
1.	MyoMex - https://github.com/mark-toma/MyoMex
2.	Bayesian Filtering - https://github.com/Ircam-RnD/bayesfilter
3.	EMG Features adapted from: 
  - EMG Feature Extraction Toolbox - https://nl.mathworks.com/matlabcentral/fileexchange/71514-emg-feature-extraction-toolbox
  - CircStat - https://github.com/circstat/circstat-matlab
  - SMAV MADN -https://bidal.sfsu.edu/~kazokada/research/okada_embc17_myoFeature.pdf
4.	Scrollplot - https://nl.mathworks.com/matlabcentral/fileexchange/14984-scrollplot-scrollable-x-y-axes
5.	Peakseek - https://nl.mathworks.com/matlabcentral/fileexchange/26581-peakseek
