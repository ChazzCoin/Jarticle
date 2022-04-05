from FAIR import fig
from pathlib import Path
from FAIR.Logger.CoreLogger import Log
from FAIR.Core import DICT
import json
import os

Log = Log("FAIR.Cache.LocalCache")

cache_path = fig.MASTER_PATH + "/Data/Cache"

class LocalCache:
    processName = ""
    file = None
    data = None

    def __init__(self, processName, clearCache=False):
        self.processName = processName
        # if clearCache:
        #     self.clear_cache()
        # self.file = open(f"{cache_path}/{self.processName}.json", "w+")
        temp = Path(f"{cache_path}/{self.processName}.json")
        temp.touch(exist_ok=True)
        self.file = open(temp)
        Log.i(f"Caching Enabled for: {processName}.")

    def data_to_json(self, data):
        temp = []
        for item in data:
            temp.append(item)
        return temp

    def save_data(self, data):
        if type(data) is list:
            data = { "data": data }
        data = self.data_to_json(data)
        data = {"data": data}
        try:
            with open(f'{cache_path}/{self.processName}.json', 'w') as f:
                json.dump(data, f, sort_keys=True, indent=4)
            Log.d(f"Saved File {self.processName}.json to Cache Directory")
        except Exception as e:
            Log.e("Error saving dict'd dict.", error=e)
            return None

    def load_data(self):
        try:
            file = open(f"{cache_path}/{self.processName}.json")
            temp = json.load(file)
            self.data = DICT.get("data", temp)
            return self.data
        except Exception as e:
            Log.e("No File Found.", error=e)
            return None

    def clear_cache(self):
        try:
            os.remove(f"{cache_path}/{self.processName}.json")
            Log.d(f"Cleared cache file {self.processName}.json.")
        except Exception as e:
            Log.e("Failed to remove cache file", error=e)
