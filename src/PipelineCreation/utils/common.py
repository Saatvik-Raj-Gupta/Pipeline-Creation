import os
from box.exceptions import BoxValueError
import yaml
from PipelineCreation import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations #Used to ensure that the annotations provided with the parameters are maintained and the function does not behave differentally than intended
def read_yaml(path_to_yaml: Path) -> ConfigBox: #ConfigBox class lests us access dictionary items in dict.keys format too
    '''Reads yaml file and returns
    
    Args:
        path_to_yaml (str): path like input
    
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    
    Returns:
        ConfigbBox: ConfigBox type'''
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded succesfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    '''Create list of directories
    
    Args:
        path_to_directories(list): list of the path of directories
        ignore_log (bool, optional): ignore if multiple dirs to be created; Default to False'''
    for path in path_to_directories:
        os.makedirs(path, exist_ok = True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves a json file
    
    Args:
        path (Path): path to json file
        data (dict): data to be saved in json file
    """ 
    with open(path, "w") as f:
        json.dump(data, f, indent = 4)
    
    logger.info(f"json file saved at: {path}")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load a json files data
    
    Args:
        path (Path): path to json file
    
    Returns:
        ConfigBox: data as class attributes insted of dict"""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"json file loaded successfully from: {path}")
    return ConfigBox(content)

@ensure_annotations
def load_bin(path: Path) -> Any:
    '''Loads a binary file
    
    Args:
        path (Path): path to the binary file
    
    Returns:
        Any: object stored in the file'''
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data

@ensure_annotations
def save_bins(data: Any, path: Path):
    '''saves binary file
    
    Args:
        data (Any): data to be saved in binary
        path (Path): path to the binary file'''
    joblib.dump(value = data, filename = path)
    logger.info(f"Binary file saved at: {path}")

@ensure_annotations
def get_size(path: Path) -> str:
    """Get file size in kilobytes
    
    Args:
        path (Path): path to the file to get the size from
    
    Returns:
        str: file size in KB in string format"""
    size_in_kb = round(os.path.get_size(path)/1024)
    return f"~ {size_in_kb} KB"