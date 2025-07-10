import configparser
import os

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def get_config():
    return load_config()