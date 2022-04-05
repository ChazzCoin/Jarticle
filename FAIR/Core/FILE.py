import json
# from Models.Hookup import Hookup
from FAIR.Core import DICT, DATE
from FAIR import fig
from FAIR.Logger.CoreLogger import Log
import pandas as pd

Log = Log("FAIR.Base.FILE")

data_path = fig.MASTER_PATH + "/Data"
export_path = data_path + "/Export"
glewmetv_path = data_path + "/GlewMeTv"
log_path = fig.MASTER_PATH + "/Utils/Logs"

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

# def save_list_to_file(list_of_items, file_name, file_path=export_path):
#     # TODO: if export_path doesn't exist, create it.
#     try:
#         name_date = DATE.to_db_date().replace(' ', '.').replace(',', '').replace(':', '.')
#         with open(f"{file_path}/{file_name}-{name_date}.txt", 'w') as f:
#             f.write("\n")
#             f.write("\n")
#             f.write(f"Hookup Count: {len(list_of_items)}")
#             f.write("\n")
#             f.write("\n")
#             for item in list_of_items:
#                 rank = DICT.get('rank', item)
#                 title = DICT.get('title', item)
#                 body = DICT.get('body', item)
#                 d = DICT.get('published_date', item)
#                 date = DATE.from_db_date(str(d if d is not None else "01/01/1913"))
#                 # summary = DICT.get('summary', item)
#                 j = Hookup.to_file_json(item)
#                 f.write("\n")
#                 f.write("---------NEW HOOKUP--------")
#                 f.write("\n")
#                 f.write("\n")
#                 f.writelines(f"-> RANK: {str(rank)}")
#                 f.write("\n")
#                 f.writelines(f"-> TITLE: {title}")
#                 f.write("\n")
#                 f.writelines(f"-> DATE: {str(date)}")
#                 f.write("\n")
#                 # f.writelines(f"-> SUMMARY: {str(summary)}")
#                 f.write("\n")
#                 f.write("\n")
#                 json.dump(j, f, sort_keys=True, indent=4, default=str)
#                 f.write("\n")
#                 f.write("BODY:")
#                 f.write("\n")
#                 f.writelines(body)
#                 f.write("\n")
#                 f.write("\n")
#             Log.i(f"Hookups Exported Successfully to File: {file_name}")
#     except Exception as e:
#         Log.e("Failed to write hookups to file.", error=e)

