import sys, os
import ctranslate2
import sentencepiece as spm
from typing import Union



def indexOf(arr: list, value):
    try: return arr.index(value)
    except: return -1


class SugoiTranslator:
    def __init__(self, modelDir= "./model") -> None:
        self.modelDir = modelDir
        self.sp_source_model = os.path.join(modelDir, "spm.ja.nopretok.model")
        self.sp_target_model = os.path.join(modelDir, "spm.en.nopretok.model")
        # inter_threads: quantas operações independentes podem ser executadas simultaneamente
        self.translator = ctranslate2.Translator(modelDir, device="cpu", intra_threads=3, inter_threads=2)

    def tokenizeBatch(self, text):
        sp = spm.SentencePieceProcessor(self.sp_source_model)
        if isinstance(text, list): return sp.encode(text, out_type=str)
        elif isinstance(text, str):
            return [sp.encode(text, out_type=str)]


    def detokenizeBatch(self, token):
        sp = spm.SentencePieceProcessor(self.sp_target_model)
        text = sp.decode(token)
        return text


    def translate(self, text: Union[str, list]):
        translated = self.translator.translate_batch(
            source= self.tokenizeBatch(text), 
            num_hypotheses= 1, 
            return_alternatives= False, 
            replace_unknowns= False, 
            no_repeat_ngram_size= 3, # repetition_penalty
            disable_unk= True, 
            beam_size= 5, 
            sampling_temperature= 0, 
        )

        return [''.join( self.detokenizeBatch(result.hypotheses[0]) ) for result in translated]


if __name__ == "__main__":
    global modelDir
    modelDir = "./model"
    index = indexOf(sys.argv, "-modelDir")
    if index != -1: modelDir = sys.argv[index+1]
    
    sugoiTranslator = SugoiTranslator(modelDir)
    translated = sugoiTranslator.translate("ダンガンロンパ 希望の学園と絶望の高校生")
    print(translated)


