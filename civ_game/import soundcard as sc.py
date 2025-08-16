import soundcard as sc
import vosk
from googletrans import Translator
import json

# Configurações
MODEL_PATH = "model/vosk-model-pt"  # Modelo Vosk em Português
SAMPLE_RATE = 16000
TRANSLATE_DEST = "en"  # Traduzir para Inglês

# Inicializar componentes
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
translator = Translator()

def capture_audio():
    """Captura áudio do sistema por 10 segundos"""
    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        print("Capturando áudio...")
        audio_data = mic.record(numframes=SAMPLE_RATE*10)
        return audio_data[:,0]  # Converter para mono

def recognize_speech(audio_data):
    """Reconhecimento de fala offline"""
    if recognizer.AcceptWaveform(audio_data.tobytes()):
        result = json.loads(recognizer.Result())
        return result.get("text", "")
    return ""

def romanize_text(text, lang):
    """Romanização (exemplo para Japonês)"""
    if lang == "ja":
        import pykakasi
        kks = pykakasi.kakasi()
        return " ".join([item['hepburn'] for item in kks.convert(text)])
    return text  # Retorna original se não precisar de romanização

def translate_text(text, dest):
    """Tradução simples"""
    return translator.translate(text, dest=dest).text

# Fluxo principal
audio = capture_audio()
recognized_text = recognize_speech(audio)

if recognized_text:
    print(f"Texto Original: {recognized_text}")
    
    romanized = romanize_text(recognized_text, "pt")  # Substituir pela língua real
    print(f"Romanizado: {romanized}")
    
    translated = translate_text(recognized_text, TRANSLATE_DEST)
    print(f"Tradução: {translated}")
else:
    print("Nenhum texto reconhecido")