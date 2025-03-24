# LLM
Use of llm in various medical tasks
1. Extracting ground truths from reports
2. Quality assessment of extracted ground truth see this ![notebook](/notebooks/quality_assesmment.ipynb)

## Different ways to run Llama 3
1. using hugging face pipeline
2. downloading weights directly from meta


### How to use hugging face?
1. Sign up on hugging face
2. Go to meta llama repositories
3. complete the mandatory form, wait for approval
4. install git lfs (sudo apt install git-lfs)
5. now download llama repository from huggingface like one do for github
6. Download and install miniconda from here:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b
~/miniconda3/bin/conda init
source ~/.bashrc
```
7. make conda environment as mentioned below
```
conda create -n llm python=3.9
conda activate llm
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
pip install -r requirements.txt

```


## Use Deepseek trained LaLama 3.1


## Set up a llama server
One should always set up a llama server, so that flow of information is easy
1. Run this script using screen so that a llama server is running in background. All the server script are contained in a folder: server_scripts
`fastapi run server_3.1.py`
2. Now, a server url will be exposes that can be used as API like https://0.0.0.0:8000
3. You can run your main script or a jupyter notebook 



## Two ways to run llama hardware
1. cpu - https://github.com/abetlen/llama-cpp-python
2. gpu

## Making environments when not using hugging face
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


### Now different experiments

| Sr No. | Experiment Name | Notebook link |
| ------ | --------------- | ------------- |
| 1      | Classification of musculoskeletal fracture using vlm like llama 3.2, chatgpt, grok2 | ---- |


### To do
- [x] Add server scripts for llama 3.1
- [ ] Add server scripts for llama 3.2
- [ ] Add M42 medical LLM expermient
- [ ] Create a benchmark dataset of report classification
