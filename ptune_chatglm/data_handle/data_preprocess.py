import json
# 返回的字符串包含有关异常的详细信息
import traceback
import numpy as np
# tqdm进度条
from tqdm import tqdm
from datasets import load_dataset
from transformers import AutoTokenizer
from functools import partial

from glm_config import *


def convert_example_chatglm(
        examples: dict,
        tokenizer,
        max_source_seq_len: int,
        max_target_seq_len: int,
    ):
    """
    将样本数据转换为Prompt-tuning模型接收的输入数据。

    Args:
        examples (dict): 训练数据样本, e.g. -> {
                                                "text": [
                                                            '{"context": "年基准利率4.35%。从实际看...", "target": "2017年银行贷款基准利率"}',
                                                            ...
                                                ]
                                            }
        max_source_seq_len (int): prompt最大长度
        max_target_seq_len (int): 答案最大长度

    Returns:
        dict (str: np.array) -> tokenized_output = {
                            'input_ids': [[1525, 10, ...], [758, 2345, ...]],
                            'labels': [[822, 10, ...], [125, 58...]]
                        }
    """
    tokenized_output = {
        'input_ids': [],
        'labels': []
    }
    # 设定最大句子长度
    max_seq_length = max_source_seq_len + max_target_seq_len

    for example in examples['text']:
        try:
            # print(f'example-->{example}')
            # print(f'example2type-->{type(example)}')
            example = json.loads(example)
            # print(f'example==>{type(example)}')
            # print(f'example==>{example}')
            context = example["context"]
            target = example["target"]
            # print(f'context-->\n{context}')
            # print(f'context2len-->{len(context)}')
            # print("*"*80)
            # print(f'target-->\n{target}')
            # print("*"*80)
            # 对prompt输入进行编码
            prompts_ids = tokenizer.encode(
                text=context,
                add_special_tokens=False
            )
            # print(f'prompts_ids--》{prompts_ids}\n{len(prompts_ids)}')

            # 对target目标文本输入进行编码
            target_ids = tokenizer.encode(
                text=target,
                add_special_tokens=False
            )
            # print(f'target_ids--》{target_ids}\n{len(target_ids)}')
            # print("*" * 80)

            # print('37010-->', tokenizer.convert_ids_to_tokens([37010, 12, 5, 76331, 83362]))

            # 对prompt输入如果超过设置的最大长度截断
            if len(prompts_ids) >= max_source_seq_len:                                          # source 需要留一个 [gMASK] token 在结尾
                prompts_ids = prompts_ids[:max_source_seq_len - 1]
            # 对target如果超过设置的最大长度截断
            if len(target_ids) >= max_target_seq_len-1:                                       # target 需要留一个 <sop> 在开头和一个 <eop> token 在结尾
                target_ids = target_ids[:max_target_seq_len - 2]
            # print(f'new_prompts_ids--》{prompts_ids}\n{len(prompts_ids)}')
            # print(f'new_target_ids--》{target_ids}\n{len(target_ids)}')
            # print('*'*80)
            # 将输入和target合并作为ChatGLM-6B模型的输入（结合glm架构图去理解）
            input_ids = tokenizer.build_inputs_with_special_tokens(prompts_ids, target_ids)     # source_ids + [gMASK] + <sop>[也是bos] + target_ids + <eop>
            # print(f'input_ids-->{input_ids}')
            # print(f'input_ids-->{len(input_ids)}')
            # 查找bos_token_id的位置
            context_length = input_ids.index(tokenizer.bos_token_id)                            # bos 在 target 的第一位
            # print(f'context_length-->{context_length}')
            mask_position = context_length - 1                                                  # [gMASK] 在 source 的最后一位
            labels = [-100] * context_length + input_ids[mask_position + 1:]                    # 从 bos 开始到后面所有的 target 到 eos 都为 label

            pad_len = max_seq_length - len(input_ids)
            # print(f'pad_len-->{pad_len}')

            input_ids = input_ids + [tokenizer.pad_token_id] * pad_len
            # print(f'input_ids-->{input_ids}\n{len(input_ids)}')
            labels = labels + [-100] * pad_len
            # print(f'labels-->{labels}\n{len(labels)}')

            tokenized_output['input_ids'].append(input_ids)
            tokenized_output['labels'].append(labels)
        except:
            print(f'"{example}" -> {traceback.format_exc()}')
            continue

    for k, v in tokenized_output.items():
        tokenized_output[k] = np.array(v)

    return tokenized_output


def get_max_length(
        tokenizer,
        dataset_file: str
    ):
    """
    测试数据集最大的输入/输出tokens是多少。

    Args:
        dataset_file (str): _description_
    """
    source_seq_len_list = []
    target_seq_len_list = []
    with open(dataset_file, 'r') as f:
        for line in tqdm(f.readlines()):
            line = json.loads(line)
            # print(f'line---->{line}')
            source_len = tokenizer.encode(line['context'])
            # print(f'source_len--》{source_len}')
            source_seq_len_list.append(len(source_len))

            target_len = tokenizer.encode(line['target'])
            # print(f'target_len-->{target_len}')
            target_seq_len_list.append(len(target_len))
    print(f"【Source Sequence】 Max: {max(source_seq_len_list)}, Avg: {int(sum(source_seq_len_list) / len(source_seq_len_list))}, Middle: {sorted(source_seq_len_list)[int(len(source_seq_len_list) / 2)]}.")
    print(f"【Target Sequence】 Max: {max(target_seq_len_list)}, Avg: {int(sum(target_seq_len_list) / len(target_seq_len_list))}, Middle: {sorted(target_seq_len_list)[int(len(target_seq_len_list) / 2)]}.")




if __name__ == '__main__':
    pc = ProjectConfig()
    train_dataset = load_dataset('text', data_files={'train': pc.train_path})
    # print(type(train_dataset))
    # print(train_dataset)
    # print('*'*80)
    # print(train_dataset['train'])
    # print('*'*80)
    # print(train_dataset['train']["text"])
    tokenizer = AutoTokenizer.from_pretrained(pc.pre_model, trust_remote_code=True)
    # tokenized_output = convert_example_chatglm(examples=train_dataset['train'],
    #                                    tokenizer=tokenizer,
    #                                    max_source_seq_len=30,
    #                                    max_target_seq_len=20)
    # print(len(tokenized_output["input_ids"][2]))
    # print(len(tokenized_output["labels"][2]))

    get_max_length(tokenizer, pc.train_path)