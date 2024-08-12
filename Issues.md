## Development Issues
### 1. Yolo.v8n Model Integration
#### Description: 
Activation of Yolo.v8n model caused a significant spike in the following:
1. RAM
2. Memory
3. GPU 
4. CPU

The following screenshots effectively demonstrate the spikes before-after integration.

### 2. FFMPEG Integration
#### Description:
There is a recorded spike in the following when using ffmpeg framework:
1. Video Recording Length (maximum): 20s
2. Video Playback Speed (1.25x)
3. RAM
4. Memory
5. GPU
6. CPU


### 3. Server Timeout Issue
#### Description
At repeated reload's the Server sometimes timeout and does not respond. 
The server is currently hosted at http://127.0.0.1:8000/