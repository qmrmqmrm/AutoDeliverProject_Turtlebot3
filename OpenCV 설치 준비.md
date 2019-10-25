# OpenCV 설치 준비



## 1. 시스템 dependency 설치

```bash
sudo apt update && sudo apt upgrade
sudo apt purge libopencv*
# 컴파일/빌드 관련 패키지
sudo apt install build-essential cmake cmake-qt-gui unzip pkg-config
# openGL
sudo apt install libgl1-mesa-dev mesa-utils libgtkglext1-dev
# 이미지 파일 관련
sudo apt install libjpeg-dev libtiff5-dev libpng-dev
# 비디오 관련
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libavresample-dev
sudo apt install libxine2-dev libv4l-dev v4l-utils
sudo apt install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
# 카메라 관련
sudo apt install libdc1394-22-dev libgphoto2-dev libopenni2-dev
# 코덱
sudo apt install libxvidcore-dev libx264-dev x264
# GUI
sudo apt install libgtk-3-dev
# 최적화
sudo apt install libatlas-base-dev libopenblas-dev libeigen3-dev gfortran libtbb2 libtbb-dev
# python
sudo apt install python3-dev python3-numpy
```



## 2. OpenCV 다운로드

시스템 dependency 설치하면서 여기서 최신버전 'Sources' 다운로드

<https://opencv.org/releases/> 



## 3. Qt 설치

여기서 최신 버전 다운로드 `qt-opensource-linux-x64-<version>.run` 받기  

<https://download.qt.io/archive/qt/>  

다음 명령어를 실행하면 설치 창이 뜨고 기본 값으로 계속 진행하면 된다.

```
> cd ~/Downloads
> chmod a+x <설치파일명>
> sudo ./<설치파일명>
```

