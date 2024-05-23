# LLM
Use of llm in various medical tasks
1. Extracting ground truths from reports

## two ways to run llama
1. cpu - https://github.com/abetlen/llama-cpp-python
2. gpu

## Making environments
```
conda create -n llm
conda activate llm
pip install --extra-index-url https://download.pytorch.org/whl/test/cu118 llama-recipes

#now download weigths from llama: by going to https://llama.meta.com/llama-downloads/
#fill form
# recieve mail, visit https://github.com/meta-llama/llama
bash download.sh
# enter the link here you recieved in mail and then press enter to download all the models
bash convert_hf.sh
```

#### This is for code llama 3
```
bash download_llama3.sh
(enter the url you recived on mail)
torchrun --nproc_per_node 1 example_chat_completion.py \
    --ckpt_dir Meta-Llama-3-8B-Instruct/ \
    --tokenizer_path Meta-Llama-3-8B-Instruct/tokenizer.model \
    --max_seq_len 512 --max_batch_size 6
```