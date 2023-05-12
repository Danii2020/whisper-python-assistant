import re

tacotron_drive_id = "YOUR TACOTRON MODEL DRIVE ID LIKE IN THE VIDEO"
hifigan_id = "1-BylR6HF4vthtuCPFUODemBgjEh01_B3" #Leave it

if tacotron_drive_id != "":
    TACOTRON2_ID = tacotron_drive_id
else:
    raise Exception("No ID provided.")

if hifigan_id in {"", "universal"}:
    HIFIGAN_ID = "universal"
    print("Using universal Hifi-Gan model.")
else:
    HIFIGAN_ID = hifigan_id

# Check if Initialized
try:
    initialized
except NameError:
    print("Setting up, please wait.\n")
    with tqdm(total=5, leave=False) as pbar:
        
        import time
        import matplotlib
        import matplotlib.pylab as plt
        import gdown
        d = 'https://drive.google.com/uc?id='
  
        import IPython.display as ipd
        import numpy as np
        import torch
        import json
        from hparams import create_hparams
        from model import Tacotron2
        from layers import TacotronSTFT
        from audio_processing import griffin_lim
        from text import text_to_sequence
        from env import AttrDict
        from meldataset import mel_spectrogram, MAX_WAV_VALUE
        from models import Generator
        from denoiser import Denoiser
        import resampy
        import scipy.signal
        import num2words
        pbar.update(1) # initialized Dependancies

        # Setup Pronounciation Dictionary
        !gdown '1OZJ0KRjEIsIMdd21WeZaAn7CPO__8qw-'
        thisdict = {}
        for line in reversed((open('merged.dict.txt', "r").read()).splitlines()):
            thisdict[(line.split(" ",1))[0]] = (line.split(" ",1))[1].strip()
 
        pbar.update(1) # Downloaded and Set up Pronounciation Dictionary

        def ARPA(text, punctuation=r"!?,.;", EOS_Token=True):
            out = ''
            for word_ in text.split(" "):
                word=word_; end_chars = ''
                while any(elem in word for elem in punctuation) and len(word) > 1:
                    if word[-1] in punctuation: end_chars = word[-1] + end_chars; word = word[:-1]
                    else: break
                try:
                    word_arpa = thisdict[word.upper()]
                    word = "{" + str(word_arpa) + "}"
                except KeyError: pass
                out = (out + " " + word + end_chars).strip()
            if EOS_Token and out[-1] != ";": out += ";"
            return out

        def get_hifigan(MODEL_ID, conf_name):
            # Download HiFi-GAN
            hifigan_pretrained_model = 'hifimodel_' + conf_name
            #gdown.download(d+MODEL_ID, hifigan_pretrained_model, quiet=False)

            if MODEL_ID == 1:
              !wget "https://github.com/justinjohn0306/tacotron2/releases/download/assets/Superres_Twilight_33000" -O $hifigan_pretrained_model
            elif MODEL_ID == "universal":
              !wget "https://github.com/justinjohn0306/tacotron2/releases/download/assets/g_02500000" -O $hifigan_pretrained_model
            else:
              gdown.download(d+MODEL_ID, hifigan_pretrained_model, quiet=False)

            if not exists(hifigan_pretrained_model):
                raise Exception("HiFI-GAN model failed to download!")

            # Load HiFi-GAN
            conf = os.path.join("hifi-gan", conf_name + ".json")
            with open(conf) as f:
                json_config = json.loads(f.read())
            h = AttrDict(json_config)
            torch.cuda.manual_seed(h.seed)
            hifigan = Generator(h).to(torch.device("cuda"))
            state_dict_g = torch.load(hifigan_pretrained_model, map_location=torch.device("cuda"))
            hifigan.load_state_dict(state_dict_g["generator"])
            hifigan.eval()
            hifigan.remove_weight_norm()
            denoiser = Denoiser(hifigan, mode="normal")
            return hifigan, h, denoiser

        # Download character HiFi-GAN
        hifigan, h, denoiser = get_hifigan(HIFIGAN_ID, "config_v1")
        # Download super-resolution HiFi-GAN
        hifigan_sr, h2, denoiser_sr = get_hifigan(1, "config_32k")
        pbar.update(1) # Downloaded and Set up HiFi-GAN

        def has_MMI(STATE_DICT):
            return any(True for x in STATE_DICT.keys() if "mi." in x)

        def get_Tactron2(MODEL_ID):
            # Download Tacotron2
            tacotron2_pretrained_model = 'MLPTTS'
            gdown.download(d+MODEL_ID, tacotron2_pretrained_model, quiet=False)
            if not exists(tacotron2_pretrained_model):
                raise Exception("Tacotron2 model failed to download!")
            # Load Tacotron2 and Config
            hparams = create_hparams()
            hparams.ignore_layers=["embedding.weight"]
            hparams.sampling_rate = 22050
            hparams.max_decoder_steps = 3000 # Max Duration
            hparams.gate_threshold = 0.25 # Model must be 25% sure the clip is over before ending generation
            model = Tacotron2(hparams).cuda()
            state_dict = torch.load(tacotron2_pretrained_model, map_location=torch.device("cuda"))['state_dict']
            if has_MMI(state_dict):
                raise Exception("ERROR: This notebook does not currently support MMI models.")
            model.load_state_dict(state_dict)
            _ = model.eval()
            return model, hparams

        model, hparams = get_Tactron2(TACOTRON2_ID)
        previous_tt2_id = TACOTRON2_ID

        pbar.update(1) # Downloaded and Set up Tacotron2

        # Extra Info
        def end_to_end_infer(text, pronounciation_dictionary, GrifinLimSynthesis, file_path):
            for i in [x for x in text.split("\n") if len(x)]:
                if not pronounciation_dictionary:
                    if i[-1] != ";": i=i+";" 
                else: i = ARPA(i)
                with torch.no_grad(): # save VRAM by not including gradients
                    sequence = np.array(text_to_sequence(i, ['basic_cleaners']))[None, :]
                    sequence = torch.autograd.Variable(torch.from_numpy(sequence)).cuda().long()
                    mel_outputs, mel_outputs_postnet, _, alignments = model.inference(sequence)
                    if not GrifinLimSynthesis:
                      y_g_hat = hifigan(mel_outputs_postnet.float())
                      audio = y_g_hat.squeeze()
                      audio = audio * MAX_WAV_VALUE
                      audio_denoised = denoiser(audio.view(1, -1), strength=35)[:, 0]

                      # Resample to 32k
                      audio_denoised = audio_denoised.cpu().numpy().reshape(-1)

                      normalize = (MAX_WAV_VALUE / np.max(np.abs(audio_denoised))) ** 0.9
                      audio_denoised = audio_denoised * normalize
                      wave = resampy.resample(
                          audio_denoised,
                          h.sampling_rate,
                          h2.sampling_rate,
                          filter="sinc_window",
                          window=scipy.signal.windows.hann,
                          num_zeros=8,
                      )
                      wave_out = wave.astype(np.int16)

                      # HiFi-GAN super-resolution
                      wave = wave / MAX_WAV_VALUE
                      wave = torch.FloatTensor(wave).to(torch.device("cuda"))
                      new_mel = mel_spectrogram(
                          wave.unsqueeze(0),
                          h2.n_fft,
                          h2.num_mels,
                          h2.sampling_rate,
                          h2.hop_size,
                          h2.win_size,
                          h2.fmin,
                          h2.fmax,
                      )
                      y_g_hat2 = hifigan_sr(new_mel)
                      audio2 = y_g_hat2.squeeze()
                      audio2 = audio2 * MAX_WAV_VALUE
                      audio2_denoised = denoiser(audio2.view(1, -1), strength=35)[:, 0]
                    
                      # High-pass filter, mixing and denormalizing
                      audio2_denoised = audio2_denoised.cpu().numpy().reshape(-1)
                      b = scipy.signal.firwin(
                          101, cutoff=10500, fs=h2.sampling_rate, pass_zero=False
                      )
                      y = scipy.signal.lfilter(b, [1.0], audio2_denoised)
                      y *= superres_strength
                      y_out = y.astype(np.int16)
                      y_padded = np.zeros(wave_out.shape)
                      y_padded[: y_out.shape[0]] = y_out
                      sr_mix = wave_out + y_padded
                      sr_mix = sr_mix / normalize
                    else:
                      taco_stft = TacotronSTFT(
                          hparams.filter_length, hparams.hop_length, hparams.win_length,
                          sampling_rate=hparams.sampling_rate)
                      mel_decompress = taco_stft.spectral_de_normalize(mel_outputs_postnet)
                      mel_decompress = mel_decompress.transpose(1, 2).data.cpu()
                      spec_from_mel_scaling = 1000
                      spec_from_mel = torch.mm(mel_decompress[0], taco_stft.mel_basis)
                      spec_from_mel = spec_from_mel.transpose(0, 1).unsqueeze(0)
                      spec_from_mel = spec_from_mel * spec_from_mel_scaling
                      waveform = griffin_lim(torch.autograd.Variable(spec_from_mel[:, :, :-1]), taco_stft.stft_fn, n_iter)
                    
                    print("")
                    if not GrifinLimSynthesis:
                        sr_mix_audio = sr_mix.astype(np.int16)
                        sf.write(ruta_archivo, sr_mix_audio, h2.sampling_rate)
                    else:
                        waveform_audio = waveform.numpy()
                        sf.write(file_path, waveform_audio, 22050)
                    
    initialized = "Ready"

if previous_tt2_id != TACOTRON2_ID:
    print("Updating Models")
    model, hparams = get_Tactron2(TACOTRON2_ID)
    hifigan, h, denoiser = get_hifigan(HIFIGAN_ID, "config_v1")
    previous_tt2_id = TACOTRON2_ID
  

# Recommend to not chnage these parameters unless
# you know what are you doing

pronounciation_dictionary = False
GrifinLimSynthesis = False
n_iter = 50
max_duration = 30 
model.decoder.max_decoder_steps = max_duration * 100
stop_threshold = 0.5
model.decoder.gate_threshold = stop_threshold
superres_strength =  1.0

time.sleep(1)

contents = []
def convert_num_to_words(utterance):
    utterance = ' '.join([num2words.num2words(i ,lang='es') if i.isdigit() else i for i in utterance.split()])
    return utterance

def synthesize_voice(text, file_path):
  while True:
      try:
          transcript = text
          res = re.sub('(\d+(\.\d+)?)', r' \1 ', transcript)
          #strip() will remove the spaces that are in the first and last position of the string (if it stays)
          res = res.strip()
          ultima = (convert_num_to_words(res))
          line = ultima
          if line == "":
              continue
          end_to_end_infer(line, pronounciation_dictionary, GrifinLimSynthesis, file_path)
      except EOFError:
          break
      except KeyboardInterrupt:
          print("Stopping...")
          break
      except OverflowError:
          print ("Number too damn big")
          continue
