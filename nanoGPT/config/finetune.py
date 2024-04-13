import time

out_dir = 'out-headlines2'
eval_interval = 20
eval_iters = 40
wandb_log = False # feel free to turn on
wandb_project = 'headlines'
wandb_run_name = 'ft-' + str(time.time())

dataset = 'headlines'
init_from = 'gpt2-xl' # this is the largest GPT-2 model

# only save checkpoints if the validation loss improves
always_save_checkpoint = False

dropout = 0.11

# the number of examples per iter:
# 1 batch_size * 32 grad_accum * 1024 tokens = 32,768 tokens/iter
# shakespeare has 301,966 tokens, so 1 epoch ~= 9.2 iters
batch_size = 1
gradient_accumulation_steps = 32
block_size = 1024

max_iters = 100

# finetune at constant LR
learning_rate = 3e-5
decay_lr = False

