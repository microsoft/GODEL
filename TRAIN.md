## Retraining full models

**Important:** 5/22/2023: It is no longer possible to retrain GODEL models from scratch as the [dump files](https://files.pushshift.io/reddit) of the Pushshift Reddit Dataset have been recently deleted. If you would like to recreate Reddit data, please consider using the Pushshift [API](https://github.com/pushshift/api) instead, but please note that the API is not supported by the GODEL codebase. We left the instructions below for historical reasons (e.g., for users who still have the Reddit dump files), but these instructions no longer work without the dump files.

### Data preparation
GODEL is pre-trained with three phases 1) Linguistic pre-training on public web documents to gain the capability of text generation. 2) Dialog pre-training on public dialog data to learn to chat like a human. 3) Grounded dialog pre-training to enable a dialog model to generate responses grounding on specific goals.

The first phase is rather straightforward, i.e., initiating from any pre-trained LMs. The remaining phases require:

- Generating 27GB Reddit dataset, which involves downloading full Reddit submission and comments dumps from https://files.pushshift.io/reddit creating intermediate files, which overall require 700GB of local disk space. Please follow this [repo](https://github.com/microsoft/DialoGPT) to prepare the data.

- Preparing grounded datasets including [DSTC7-End-to-End-Conversation-Modeling](https://github.com/mgalley/DSTC7-End-to-End-Conversation-Modeling), [UnifiedQA](https://github.com/allenai/unifiedqa), [MS MARCO](https://microsoft.github.io/msmarco/), [Schema-Guided Dataset](https://github.com/google-research-datasets/dstc8-schema-guided-dialogue). 

Prepare reddit data and specify its path in *create_reddit_dataset.sh*
```bash
cd scripts
./pretrain_data_preprocessing.sh
```

Downloading required datasets and specify its path in *create_grounded_dataset.sh*
```bash
cd scripts 
./create_grounded_dataset.sh
```

### Pre-Training
```bash
# Reddit training
OUTPUT_DIR={path_to_save_predictions}
accelerate launch --config_file configs/G16_config.yaml train.py 
	--model_name_or_path t5-base \
	--dataset_name ./datasets_loader/reddit_dataset.py \
	--output_dir ${OUTPUT_DIR} \
	--per_device_train_batch_size=16 \
	--per_device_eval_batch_size=16 \
	--max_target_length 256 \
	--max_length 512 \
	--num_train_epochs 10 \
	--preprocessing_num_workers 24 \
	--num_beams 5 \
	--exp_name GODEL_reddit_training  \
	--learning_rate 5e-5 \	
	--save_every_checkpoint \
	--save_steps 50000

# Grounded training
REDDIT_CHECKPOINT={path_to_saved_checkpoint}
OUTPUT_DIR={path_to_save_predictions}
accelerate launch --config_file configs/G16_config.yaml train.py 
	--model_name_or_path ${REDDIT_CHECKPOINT} \
	--dataset_name ./datasets_loader/grounded_dataset.py \
	--output_dir ${OUTPUT_DIR} \
