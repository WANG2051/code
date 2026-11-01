# coding:utf-8
import json
import ollama
import re
# from rich import print

# 定义不同类型下的实体类型
schema = {
    '金融': ['日期', '股票名称', '开盘价', '收盘价', '成交量']
}

IE_PATTERN = "{}\n\n提取上述句子中{}的实体，并按照JSON格式输出，上述句子中不存在的信息用['原文中未提及']来表示，多个值之间用','分隔。"



# 提供一些例子供模型参考
ie_examples = {
    '金融': [
        {
            'content': '2023-01-10，股市震荡。股票古哥-D[EOOE]美股今日开盘价100美元，一度飙升至105美元，随后回落至98美元，最终以102美元收盘，成交量达到520000。',
            'answers': {
                '日期': ['2023-01-10'],
                '股票名称': ['古哥-D[EOOE]美股'],
                '开盘价': ['100美元'],
                '收盘价': ['102美元'],
                '成交量': ['520000'],
            }
        }
    ]
}


def init_prompts():
    """
    初始化前置prompt，便于模型做 incontext learning。
    """

    ie_pre_history = [{"role": "system", "content": "你是一个信息抽取助手。"},]

    for _type, example_list in ie_examples.items():
        # print(f'_type-->{_type}')
        for example in example_list:
            # print(f'example-->{example}')
            sentence = example['content']
            # print(f'sentence--》{sentence}')
            properties_str = ', '.join(schema[_type])
            # print(f'properties_str--》{properties_str}')
            schema_str_list = f'“{_type}”({properties_str})'
            # print(f'schema_str_list-->{schema_str_list}')
            # print('*'*80)
            sentence_with_prompt = IE_PATTERN.format(sentence, schema_str_list)
            # print(f'sentence_with_prompt-->{sentence_with_prompt}')
            ie_pre_history.append({"role": "user", "content": f'{sentence_with_prompt}'})
            ie_pre_history.append({"role": "assistant", "content": f"{json.dumps(example['answers'], ensure_ascii=False)}"})

    return {'ie_pre_history': ie_pre_history}


def clean_response(response: str):
    """
    后处理模型输出。

    Args:
        response (str): _description_
    """
    # response1='```json["name":lucy]```abc```json["name":lucy]```'
    if '```json' in response:
        res = re.findall(r'```json(.*?)```', response, re.DOTALL)
        # print(f'res--》{res}')
        if len(res) and res[0]:
            response = res[0]
        response.replace('、', ',')
    try:
        return json.loads(response)
    except:
        return response


def inference(
        sentences: list,
        custom_settings: dict
    ):
    """
    推理函数。

    Args:
        sentences (List[str]): 待抽取的句子。
        custom_settings (dict): 初始设定，包含人为给定的 few-shot example。
    """
    for sentence in sentences:
        cls_res = "金融"
        if cls_res not in schema:
            print(f'The type model inferenced {cls_res} which is not in schema dict, exited.')
            exit()
        properties_str = ', '.join(schema[cls_res])
        schema_str_list = f'“{cls_res}”({properties_str})'
        sentence_with_ie_prompt = IE_PATTERN.format(sentence, schema_str_list)
        # print(f'sentence_with_ie_prompt-->{sentence_with_ie_prompt}')
        # 使用 Ollama 调用 Qwen2.5:7b 模型
        messages = [*custom_settings['ie_pre_history'],
                    {"role": "user", "content": sentence_with_ie_prompt}]
        response = ollama.chat(
            model="qwen2.5:7b",
            messages= messages
        )

        res_content = response["message"]["content"]
        # print(f'res_content-->{res_content}')

        ie_res = clean_response(res_content)
        print(f'sentence: {sentence}')
        print(f'inference answer: {ie_res}')


if __name__ == '__main__':

    # 初始化句子和自定义设置
    sentences = [
        '2023-02-15，寓意吉祥的节日，股票佰笃[BD]美股开盘价10美元，虽然经历了波动，但最终以13美元收盘，成交量微幅增加至460,000，投资者情绪较为平稳。',
        '2023-04-05，市场迎来轻松氛围，股票盘古(0021)开盘价23元，尽管经历了波动，但最终以26美元收盘，成交量缩小至310,000，投资者保持观望态度。',
    ]

    # 初始化自定义设置
    custom_settings = init_prompts()
    # print(custom_settings)

    # # 开始推理
    inference(
        sentences,
        custom_settings
    )
