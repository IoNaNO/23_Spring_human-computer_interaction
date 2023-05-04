# 23_Spring_Human-computer_Interaction
## How to run the code
### Lab 1-1

```bash
conda create --name asr python=3.9
conda activate asr
python -m pip install speechrecognition
python -m pip install pyaudio
python -m pip install pocketsphinx
python -m pip install pyqt5
python asr.py
```

### Lab 2

1. Backend

Read `backend\README.md` and download the corresponding asserts: **imagenet** folder and datasets

```bash
conda create --name tf_web python=3.9
conda activate tf_web
conda install -c conda-forge pyqt
conda install Flask numpy tensorflow Flask-HTTPAuth scipy imageio matplotlib scikit-learn
python -m pip install flask_cors
python server/image_vectorizer.py
python server/rest-server.py
```

2. Frontend

```bash
npm i
npm run dev
```

