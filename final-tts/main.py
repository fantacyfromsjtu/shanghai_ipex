from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import paddle
from paddlespeech.cli.tts import TTSExecutor
from IPython import display
from datetime import datetime



def generate_translation(model, tokenizer, example):
    """print out the source, target and predicted raw text."""
    source = example['sh']
    target = example['zh']
    input_ids = example['input_ids']
    input_ids = torch.LongTensor(input_ids).view(1, -1).to(model.device)
    generated_ids = model.generate(input_ids, max_new_tokens=64)
    prediction = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    
    print('source: ', source)
    print('target: ', target)
    print('prediction: ', prediction)
    return prediction


### translate ###

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = "./checkpoint-5000"
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
filename = "texts.txt"

with open(filename, "r", encoding="utf-8") as file:
    content = file.read()
text = content.replace("<unk>", "")  

with tokenizer.as_target_tokenizer():
    model_inputs = tokenizer(text, max_length=64, truncation=True)
    example = {}
    example['sh'] = text
    example['zh'] = text
    example['input_ids'] = model_inputs['input_ids']
    trans_text = generate_translation(model, tokenizer, example)


### tts ###

tts_executor = TTSExecutor()
current_time = datetime.now()
time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

wav_file = tts_executor(
    text=trans_text,
    output=f'./output/{time_str}.wav',
    am='fastspeech2_csmsc',
    am_config=None,
    am_ckpt=None,
    am_stat=None,
    spk_id=0,
    phones_dict=None,
    tones_dict=None,
    speaker_dict=None,
    voc='pwgan_csmsc',
    voc_config=None,
    voc_ckpt=None,
    voc_stat=None,
    lang='zh',
    device=paddle.get_device())

display.Audio(f'./output/{time_str}.wav')
display.clear_output()
