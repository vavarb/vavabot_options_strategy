# VavaBot Options Strategy
a bot for Deribit exchange 
![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

## Author
|Vavarb</sub>](https://github.com/vavarb) | 

Contact email:
```
vavarb@yahoo.com
```

## About the Project
This is a bot what send options strategies orders. It was developed in python and designed to be executed only on the Deribit Exchange.
  https://www.deribit.com/

<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/ad2b1f500d2846dc9af0796e32d63adc2ee30824/img/img1.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img2.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img3.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img4.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img5.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img6.PNG'>
<img src = 'https://github.com/vavarb/vavabot_options_spread/blob/9340cb76558bdc7f3faae18390a04143c248f71d/img/img7.PNG'>

## Getting Started
- This project was devoloped:
  - OS: Windows 10.
  - IDE: PyCharm 2021.3.1 (Community Edition).
  - Language: Python 3.10
- If you want .exe version, you can download it from the link below. If you prefer to obtain a local copy of the 
repository, please do the following further below.
```
https://drive.google.com/file/d/1lPUbGObDrG4pKOZ6WxGNDabjb31n326g/view?usp=sharing
```
Windows FireWall need disabled for .exe if there is a Deribit conection or SSL Certificate error.

### Prerequisites
- Install packages:
   - websocket-client
   - Websocket
   - Threading
   - Matplotlib
   - PyQt5, QtCore, QtGui, QtWidgets
- Windows FireWall need disabled for PyCaharm if there is a conection or SSL Certificate error.

### Installation :arrow_forward:
  1. Clone the repo:
```
git clone https://github.com/vavarb/vavabot_options_spread
```
  2. Run vavabot_options_spread.py file

#### Linux
- If you use Linux Ubuntu 22.04 and the following error appears:

qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, xcb.

- You can try:
  1. OPEN TERMINAL: <CTRL + ALT + T>
  2. From https://howtoinstall.co/pt/xcb

  ```
  sudo apt-get update
  ```

  ```
  sudo apt-get install xcb
  ```

  3. From https://www.techtudo.com.br/noticias/2011/04/aprenda-ativar-o-login-de-acesso-conta-root-no-ubuntu.ghtml

  ```
  sudo passwd root
  ```

  Type your user password.

  Type new root password

  Confirm new root password

  4. DISBLED WAYLAND. 

  From https://stackoverflow.com/questions/69828508/warning-ignoring-xdg-session-type-wayland-on-gnome-use-qt-qpa-platform-wayland#:~:text=The%20same%20Warning%3A%20Ignoring%20XDG_SESSION_TYPE,figure%20to%20a%20pdf%20file.
  
  ```
  su root
  ```

  ```
  cd //
  ```

  ```
  cd etc
  ```

  ```
  cd gdm3
  ```

  ```
  gedit custom.conf
  ```

  Uncommenting: ```WaylandEnable=false```

  Save and close.

  ```
  cd //
  ```

  ```
  cd etc
  ```

  ```
  gedit environment
  ```

  Add: 
  ```
  QT_QPA_PLATFORM=xcb
  ```

  Save and close.

    ```
    OR you can open Nautilus or Nemo GUI. 

    <CTRL + L>  
    Type: admin //
    Type: root password         
    Open etc/gdm3/custom.conf file and Uncommenting: ```WaylandEnable=false```.
    After, open etc/environment file and add ```QT_QPA_PLATFORM=xcb```
  ```
  

  5. From https://forum.qt.io/topic/93247/qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-though-it-was-found/17

  ```
  sudo apt-get install libxcb-xinerama0
  ```

  6. RESTART LINUX.
  7. CHECK WHETHER YOU ARE ON WAYLAND OR XORG USING:
  ```
  echo $XDG_SESSION_TYPE
  ```
  The expected return is: x11

## Contributing
- Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

- If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

  1. Fork the Project.
  2. Create your Feature Branch (````git checkout -b feature/AmazingFeature````)
  3. Commit your Changes (````git commit -m 'Add some AmazingFeature````)
  4. Push to the Branch (````git push origin feature/AmazingFeature````)
  5. Open a Pull Request