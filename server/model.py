import ctranslate2
import sentencepiece as spm


modelDir = "./model"
sp_source_model = "./model/spm.ja.nopretok.model"
sp_target_model = "./model/spm.en.nopretok.model"
# inter_threads: quantas operações independentes podem ser executadas simultaneamente
translator = ctranslate2.Translator(modelDir, device="cpu", intra_threads=4, inter_threads=1)


def tokenizeBatch(text):
    sp = spm.SentencePieceProcessor(sp_source_model)
    if isinstance(text, list): return sp.encode(text, out_type=str)
    elif isinstance(text, str):
        return [sp.encode(text, out_type=str)]


def detokenizeBatch(text: str):
    sp = spm.SentencePieceProcessor(sp_target_model)
    translation = sp.decode(text)
    return translation


def translate(text: str):
    translated = translator.translate_batch(
        source=tokenizeBatch(text), 
        num_hypotheses= 1, 
        return_alternatives= False, 
        replace_unknowns= False, 
        no_repeat_ngram_size= 3, # repetition_penalty
        disable_unk= True, 
        beam_size= 5, 
        sampling_temperature= 0, 
    )

    return [''.join( detokenizeBatch(result.hypotheses[0]) ) for result in translated]