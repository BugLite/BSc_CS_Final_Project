## Development Issues

### Idle CPU
![Idle-CPU](/Support%20Docs/Development%20Documents/Problem%20Logs/System%20CPU%20Idle%20.png)

### Idle Memory
![Idle-Memory](/Support%20Docs/Development%20Documents/Problem%20Logs/System%20Memory%20Idle.png)

### 1. Yolo.v8n Model Integration
#### Description: 
Activation of Yolo.v8n model caused a significant spike in the following:
1. Memory
2. GPU 
3. CPU

The following screenshots effectively demonstrate the spikes before-after integration.
#### > Yolo.v8n CPU
![Yolov-CPU](/Support%20Docs/Development%20Documents/Problem%20Logs/Yolov8n%20CPU.png)

#### > Yolo.v8n GPU 
![Yolov-GPU](/Support%20Docs/Development%20Documents/Problem%20Logs/Yolov8n%20GPU.png)

### 2. ffmpeg Integration
#### Description:
There is a recorded spike in the following when using ffmpeg framework:
* Video Recording Length (maximum): 20s
* Video Playback Speed (1.25x)
3. Memory
4. GPU
5. CPU

#### > ffmpeg CPU
![ffmpeg-CPU](/Support%20Docs/Development%20Documents/Problem%20Logs/ffmpeg%20CPU.png)

#### > ffmpeg Memory 
![ffmpeg-Memory](/Support%20Docs/Development%20Documents/Problem%20Logs/ffmpeg%20Memory.png)

### 2. OpenCv Built-in Video Writer Integration
#### Description:
#### > cv2.VideoWriter CPU
![opencv-CPU](/Support%20Docs/Development%20Documents/Problem%20Logs/OpenCV-video%20CPU.png)

#### > ffmpeg Memory 
![opencv-Memory](/Support%20Docs/Development%20Documents/Problem%20Logs/OpenCV-video%20Memory.png)

This is computationally less expensive compared to ffmpeg.

### 3. Server Timeout Issue
#### Description
At repeated reload's the Server sometimes timeout and does not respond. 
The server is currently hosted at http://127.0.0.1:8000/