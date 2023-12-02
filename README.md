# Face Censoring Tool for Image Processing Class

## Introduction

This is a simple tool for censoring faces in images. It is written in Python and uses facenet for Face Detection, PIL for image I/O, and our own mosaic function.


## How to Use

### install requirements
```shell
python -m venv venv

source venv/Scripts/activate

pip install requirements.txt
```

### Run
```shell
python sources/app.py
```
you can see that server is running on http://localhost:5000.

## API Endpoint
### /hello
### /upload
### /change


## TODO

Pipeline:
- [x] Face Detection
- [ ] Click on Face to Select (Front End)
- [x] Crop Selected Face
- [x] Change Face to smile
- [x] Reintroduce Face to Original Image

- [ ] GUI
