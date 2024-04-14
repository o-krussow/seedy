"""
Sample from a trained model
"""
import os
import random
import pickle
from contextlib import nullcontext
import torch
import tiktoken
from model import GPTConfig, GPT

class nanoGPT:
    def __init__(self):
        # -----------------------------------------------------------------------------
        init_from = 'resume' # either 'resume' (from an out_dir) or a gpt2 variant (e.g. 'gpt2-xl')
        out_dir = 'nanoGPT/out-headlines' # ignored if init_from is not 'resume'
        start = "\n" # or "<|endoftext|>" or etc. Can also specify a file, use as: "FILE:prompt.txt"
        
        #self.num_samples = 5 # number of samples to draw
        
        self.max_new_tokens = 32 # number of tokens generated in each sample
        self.temperature = .25 # 1.0 = no change, < 1.0 = less random, > 1.0 = more random, in predictions
        self.top_k = 50 # retain only the top_k most likely tokens, clamp others to have 0 probability
        seed = random.randint(5,2000)
        device = 'cuda:1' # examples: 'cpu', 'cuda', 'cuda:0', 'cuda:1', etc.
        dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16' # 'float32' or 'bfloat16' or 'float16'
        compile = False # use PyTorch 2.0 to compile the self.model to be faster
        exec(open('nanoGPT/configurator.py').read()) # overrides from command line or config file
        # -----------------------------------------------------------------------------

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.backends.cuda.matmul.allow_tf32 = True # allow tf32 on matmul
        torch.backends.cudnn.allow_tf32 = True # allow tf32 on cudnn
        device_type = 'cuda' if 'cuda' in device else 'cpu' # for later use in torch.autocast
        ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
        self.ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

        # self.model
        if init_from == 'resume':
            # init from a self.model saved in a specific directory
            ckpt_path = os.path.join(out_dir, 'ckpt.pt')
            checkpoint = torch.load(ckpt_path, map_location=device)
            gptconf = GPTConfig(**checkpoint['model_args'])
            self.model = GPT(gptconf)
            state_dict = checkpoint['model']
            unwanted_prefix = '_orig_mod.'
            for k,v in list(state_dict.items()):
                if k.startswith(unwanted_prefix):
                    state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
            self.model.load_state_dict(state_dict)
        elif init_from.startswith('gpt2'):
            # init from a given GPT-2 self.model
            self.model = GPT.from_pretrained(init_from, dict(dropout=0.0))

        self.model.eval()
        self.model.to(device)
        if compile:
            self.model = torch.compile(self.model) # requires PyTorch 2.0 (optional)

        # look for the meta pickle in case it is available in the dataset folder
        load_meta = False
        if init_from == 'resume' and 'config' in checkpoint and 'dataset' in checkpoint['config']: # older checkpoints might not have these...
            meta_path = os.path.join('data', checkpoint['config']['dataset'], 'meta.pkl')
            load_meta = os.path.exists(meta_path)
        if load_meta:
            print(f"Loading meta from {meta_path}...")
            with open(meta_path, 'rb') as f:
                meta = pickle.load(f)
            # TODO want to make this more general to arbitrary encoder/decoder schemes
            stoi, itos = meta['stoi'], meta['itos']
            encode = lambda s: [stoi[c] for c in s]
            decode = lambda l: ''.join([itos[i] for i in l])
        else:
            # ok let's assume gpt-2 encodings by default
            print("No meta.pkl found, assuming GPT-2 encodings...")
            self.enc = tiktoken.get_encoding("gpt2")
            encode = lambda s: self.enc.encode(s, allowed_special={"<|endoftext|>"})
            decode = lambda l: self.enc.decode(l)

        # encode the beginning of the prompt
        start_ids = encode(start)
        self.x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])

    def generate(self): # run generation
        print("GENERATING")
        with torch.no_grad():
            with self.ctx:
                y = self.model.generate(self.x, self.max_new_tokens, temperature=self.temperature, top_k=self.top_k)
                
                headline = self.enc.decode(y[0].tolist()).lstrip().split("\n") #b you ti full

                return headline[0]

if __name__ == "__main__":
    gpt = nanoGPT()

    gpt.generate()

