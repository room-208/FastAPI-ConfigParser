import configparser
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT_DIR = Path(__file__).parents[1]
CONFIG_DIR = ROOT_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "config.ini"


class Parameter(BaseModel):
    section: str
    keys: List[str]
    values: List[str]


def read_config_file():
    config = configparser.ConfigParser()
    assert CONFIG_FILE.exists()
    config.read(CONFIG_FILE)
    return config


def write_config_file(section, keys, values):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if not config.has_section(section):
        config.add_section(section)
    for key, value in zip(keys, values):
        config.set(section, key, value)
    with open(CONFIG_FILE, "w") as configfile:
        config.write(configfile)


app = FastAPI()


@app.get("/")
def hello():
    return {"Hello World !"}


@app.get("/read")
def read():
    config = read_config_file()
    config_dict = {}
    for section in config.sections():
        config_dict[section] = dict(config.items(section))
    return config_dict


@app.post("/overwrite")
def overwrite(parameters: List[Parameter]):
    try:
        for param in parameters:
            if len(param.keys) != len(param.values):
                raise HTTPException(
                    status_code=400, detail="Keys and values length mismatch"
                )
            write_config_file(param.section, param.keys, param.values)
        return {"message": "Config overwritten successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
