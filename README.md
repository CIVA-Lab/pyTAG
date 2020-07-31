# pyTAG: Python based Tracking Assisted Ground-truthing

pyTAG is a lightweight tool for generating ground-truth data. pyTAG has only been tested with Python version 3.x, we haven't tested with Python 2.x. The only requirement for that is required for pyTAG is OpenCV. pyTAG supports both OpenCV versions 3.x and 4.x. To install OpenCV use the command below. 

```
pip install opencv-python
```
## About pyTAG
pyTAG has three modes for ground-truth generation: Automatic, Semi-automatic and Full Manual. For fully automatic ground-truth generation pyTAG uses six of the OpenCV's state of the art object tracking algorithms.
* CSRT
* KCF
* TLD
* MIL
* MEDIANFLOW
* BOOSTING

On the other hand, the user can interfere the object tracking process by pausing, move back and forward on frames, change the object tracking methods, reinitialize bounding box, and resume/restart the object tracking algorithm. This is the semi-automatic mode for ground-truth generation.

Another alternative for the semi-automatic ground-truth generation mode is by using linear interpolation. The frame skip size can be modified by the user and a bounding box is drawn after the size of the skip frame.

Finally, there is a fully manual mode for ground-truth generation, where the user draws bounding boxes for each frame.

### Tracking Assisted Ground-truth Generation (Automatic/Semi-Automatic Mode)
The tracking assisted ground-truth generation is uses the ```pyTAG.py``` code and initially starts with CSRT. Inside the source code you need to specify your initial/starting tracker, video source and initial bounding box. To run ```pyTAG```, you simply run the command below.
```
python pyTAG.py
```

### Linear Interpolation-based Ground-truth Generation (Semi-Automatic Mode)
The default skip frame size is 5, which means after each 5 frame the user is required to draw a bounding box. The frame skip size can be modified inside the code. Along with the frame skip size you need to provide the video source inside the code. To run ``` groundtruth_generator_linear_interpolation.py ```, use the command below.
```
python groundtruth_generator_linear_interpolation.py
```
### Fully Manual Ground-truth Generation/Reviwing Module
The Full manual ground-truth generation can be used for multiple purposes. You can use it on an exiting ground-truth data to edit/fix/correct. Another usage of this module allows you to generate ground-truth data by fully manual, by drawing bounding boxes for each frame. To run ``` reviewGT.py ```, use the command below.
```
python reviewGT.py
```

### Tracker Evaluator
The tracker evaluator is for visually comparing 2 ground-truth data and does serve for any other purpose. It is not actually a part of pyTAG.
```
python trackerEvaluator.py
```

### How to use the interactive tracking-based ground truth generation
The user interactions are mapped to only three keys.
* To stop/pause on the current frame press the ```space``` key.
* To move to the **next** frame in stopped/paused state press the ```n``` key.
* To move to the **previous** frame in stopped/paused state press the ```p``` key.
* To reinitialize the bounding box in the stopped/paused state and use the mouse by holding on the ```left-click``` and release the ```left-click``` when you are done.

The state machine that shows the interactions are given in the figure below.

![](figures/editingModuleFSMv3.png | width=100)

If you are using pyTAG, please cite our work as given below.

```
@inproceedings{ufuktepe2020pytag,
  author = "E. Ufuktepe and V. Ramtekkar and K. Gao and N. Al-Shakarji and J. Fraser and H. AliAkbarpour and G. Seetharaman and K. Palaniappan",
  title = " pyTAG: Python-based Interactive Training Data Generation for Visual Tracking Algorithms",
  year = 2020,
  journal = "Proc. SPIE Conf. Geospatial InfoFusion X (Defense + Commercial Sensing)",
  volume = 11398,
  keywords = "ground-truth generation, visual tracking, crowd sourcing, annotation, deep learning",
  doi = "10.1117/12.2561718",
  url = "https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11398/113980D/pyTAG--python-based-interactive-training-data-generation-for-visual/10.1117/12.2561718.full?SSO=1"
}
```
