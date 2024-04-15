mkdir hf
source activate base
conda activate llm
python convert_meta_hf.py --input_dir llama-2-7b --model_size 7B --output_dir hf/7b
python convert_meta_hf.py --input_dir llama-2-7b-chat --model_size 7Bf --output_dir hf/7bc
python convert_meta_hf.py --input_dir llama-2-13b --model_size 13B --output_dir hf/13b
python convert_meta_hf.py --input_dir llama-2-13b-chat --model_size 13Bf --output_dir hf/13bc
python convert_meta_hf.py --input_dir llama-2-70b --model_size 70B --output_dir hf/70b
python convert_meta_hf.py --input_dir llama-2-70b-chat --model_size 70Bf --output_dir hf/70bc