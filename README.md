# whisper-python-assistant
This is the repository for the Whisper Python virtual assistant series of videos

# Warning

This is an experimental branch, the assistant will only work if you have an Nvidia GPU.

# Instructions

In order to test it, please install the following packages using these commands in your terminal:

```
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install tqdm -q
pip install num2words
pip install git+https://github.com/wkentaro/gdown.git
pip install resampy
pip install num2words
pip install git+https://github.com/savoirfairelinux/num2words
pip install tacotron2-model
git clone -q --recursive https://github.com/justinjohn0306/hifi-gan
pip install -q librosa unidecode
```
