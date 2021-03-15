# Speed estimation algorithm using virtual detection lines(VDLs)

This algorithm is the result of the NIA traffic safety AI data construction project and is an algorithm developed by Korea Electronics Techonology Institute (KETI).

## Algorithm description

### What is the VDL?

The VDL is an imaginary line used for estimating the vehicle's speed, and calculates the vehicle's speed by using the time the vehicle has passed two lines. 
In the situation shown in the figure below, the vehicle speed estimation can be obtained in the following manner.

![속도 계산 식](images/math.JPG)

![VDL 속도 추정 설명](images/VDL_explaination.png)

### Speed estimation algorithm

During this project, various attempts were made on the vehicle speed estimation method. You can check it in [Speed Estimation Algorithm Performance Analysis Report](https://github.com/swhan0329/VDL_speed_estimation/blob/master/%EC%86%8D%EB%8F%84%20%EC%B6%94%EC%A0%95%20%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-v1.0.pdf).
But this report is written by Korean.

### Whole Algorithm Flow Chart

The code provided in this repository cannot be executed with only the .py file itself. In order to estimate the speed, object detection and tracking must be performed in advance. 
As shown in the figure below, when an input image comes in, it receives one frame at a time and preprocessing, object detection, and object tracking.
After going through the process, the speed of each object is finally estimated using the Bboxes and track classes, which are the result of object tracking. 
For more information, refer to [Manual of the Speed Estimation Algorithm using VDL method](https://github.com/swhan0329/VDL_speed_estimation/blob/master/VDL%ED%99%9C%EC%9A%A9%20%EC%86%8D%EB%8F%84%EC%B6%94%EC%A0%95%20%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98%20%EB%A7%A4%EB%89%B4%EC%96%BC-v1.1.pdf).
But this report is also written by Korean.

![속도 추정 알고리즘 전체 모델 사진](images/whole_flow_chart.png)

## How to use this algorithm

### Reference code

For the baseline code of object detection and tracking, refer to this [GitHub][link]. Environment also set in the same way as this link.

[link]: https://github.com/yehengchen/Object-Detection-and-Tracking/tree/master/OneStage/yolo/deep_sort_yolov4

### How to use the "calc_speed.py" file

1. Do git clone YOLOv4 + DeepSORT GitHub used as baseline model for detecting and tracking objects.

```bash
git clone https://github.com/yehengchen/Object-Detection-and-Tracking/tree/master/OneStage/yolo/deep_sort_yolov4
```

2. Change the track.py file in the deep_sort folder to track.py in this repository.

3. Import the calcSpeed function by entering the following at the top of the main.py file.

```python
from calc_speed import calcSpeed
```

4. After obtaining the output from the object tracking module using the object detection result, use the output to use the speed estimation function as shown in the following syntax.

```python
track = calcSpeed(track, luLine, ldLine, ruLine, rdLine, bbox, frame_idx)
```

## Result of this algorithm

[![Video Label](http://img.youtube.com/vi/URZX3wHVAZc/0.jpg)](https://youtu.be/URZX3wHVAZc?t=0s)
