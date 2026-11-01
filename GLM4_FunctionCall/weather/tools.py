import json
import requests
# 定义函数工具的描述
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取给定位置的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或区，例如北京、海淀",
                    },
                },
                "required": ["location"],
            },
        }
    }
]

# todo:1.调用API接口，实现天气查询
def get_current_weather(location):
    """得到给定地址的当前天气信息"""
    with open('./cityCode_use.json', 'r') as file:
        # 使用 json.load() 函数加载 JSON 数据
        data = json.load(file)
    # print(f'data--》{data}')
    city_code = ""
    weather_info = {}
    for loc in data:
        if location == loc["市名"]:
            city_code = loc["编码"]
    # print(f'city_code--》{city_code}')

    if city_code:
        weather_url = "http://t.weather.itboy.net/api/weather/city/" + city_code
        response = requests.get(weather_url)
        # print(f'response.text-->{response.text}')
        # print(f'response.text-->{type(response.text)}')

        result1 = eval(response.text)
        # print(f'result1--》{result1}')

        forecast = result1["data"]["forecast"][0]
        # print(f'forecast-->{forecast}')

        weather_info = {
            "location": location,
            "high_temperature": forecast["high"],
            "low_temperature": forecast["low"],
            "week": forecast["week"],
            "type": forecast["type"],
        }
    return json.dumps(weather_info, ensure_ascii=False)

# todo: 2.根据模型回复来确定使用哪一个工具函数：

def parse_response(response):
    response_message = response.choices[0].message
    # 检测是否需要调用函数
    if response_message.tool_calls:
        # 调用函数
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function test in this example, but you can have multiple
        function_name = response_message.tool_calls[0].function.name
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message.tool_calls[0].function.arguments)
        function_response = fuction_to_call(
            location=function_args.get("location"),
        )
        return function_response

if __name__ == '__main__':
    print(get_current_weather(location="北京"))