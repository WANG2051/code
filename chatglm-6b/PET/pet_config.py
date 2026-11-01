# coding:utf-8
import torch
import sys
# print(sys.path)


class ProjectConfig(object):
    def __init__(self):
        # self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu' # windows电脑/linux服务器
        self.device = "mps:0" # MAC电脑
        self.pre_model = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/bert-base-chinese'
        self.train_path = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/PET/data/train.txt'
        self.dev_path = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/PET/data/dev.txt'
        self.prompt_file = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/PET/data/prompt.txt'
        self.verbalizer = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/PET/data/verbalizer.txt'
        self.max_seq_len = 256
        self.batch_size = 8
        self.learning_rate = 5e-5
        self.weight_decay = 0
        self.warmup_ratio = 0.06
        self.max_label_len = 2
        self.epochs = 20
        self.logging_steps = 2
        self.valid_steps = 20
        self.save_dir = '/Users/ligang/PycharmProjects/LLM/prompt_tasks/PET/checkpoints'


if __name__ == '__main__':
    pc = ProjectConfig()
    print(pc.prompt_file)
    print(pc.pre_model)
