import json
from FLog.LOGGER import Log
import pandas as pd
import os

Log = Log("Jarticle.jarProvider")
data_path = os.path.dirname(__file__)
export_path = data_path + "/Export"
glewmetv_path = data_path + "/GlewMeTv"
log_path = data_path + "/Utils/Logs"

def save_csv_file(file_name, json_input):
    df = pd.DataFrame.from_dict(json_input['data'][0]['symbol'])
    df.columns = ['var1']
    df.to_csv(file_name)

def create_open_file(name, file_path):
    return open(file_path + name + ".txt", "w+")


def build_file_with_data(name, file_path, list_data):
    with open(file_path + name + ".txt", "a") as f:
        for item in list_data:
            f.write('\n------NEW------\n')
            for k, v in item.items():
                f.write(str(k) + ': ' + str(v) + '\n')


def save_crypto_data_to_file(data):
    with open(f'{data_path}/crypto_tickers.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)


def get_crypto_data_from_file():
    file = open(f"{data_path}/crypto_tickers.json")
    data = json
    return data.get("data")


def save_dict_to_file(file_name, dic, file_path=export_path):
    try:
        with open(f'{file_path}/{file_name}.json', 'w') as f:
            json.dump(dic, f, sort_keys=True, indent=4)
        Log.d(f"Saved File {file_name}.json to Data Directory")
    except Exception as e:
        Log.e("Error saving dict.", error=e)
        return None


def load_dict_from_file(file_name, file_path=data_path):
    try:
        file = open(f"{file_path}/{file_name}.json")
        data = json.load(file)
        return data
    except Exception as e:
        Log.e("No File Found.", error=e)
        return None

if __name__ == '__main__':
    d = load_dict_from_file("events", file_path=glewmetv_path)
    print(d)


