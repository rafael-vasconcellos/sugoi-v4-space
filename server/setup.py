import sys, os
from huggingface_hub import snapshot_download
import ctranslate2


def download_model():
    model_id = "JustFrederik/sugoi-v4-ja-en-ct2"
    local_folder = snapshot_download(repo_id=model_id, local_dir="./server/model")
    print(f"Files downloaded in: {local_folder}")

def convert_model():    
    model_dir = "./fairseq_model"
    output_dir = "./server/ctranslate2_model"
    if (os.path.exists(output_dir) and "-overwrite" not in sys.argv) or not os.path.exists(model_dir): return

    print("Converting...")
    converter = ctranslate2.converters.FairseqConverter(model_dir)
    converter.convert(output_dir)  # Você pode escolher entre "int8", "float16" ou deixar como None para não quantizar
    print(f"Model converted and saved in: {output_dir}")



if __name__ == "__name__":
    if "-download" in sys.argv: download_model()
    if "-convert" in sys.argv: convert_model()

