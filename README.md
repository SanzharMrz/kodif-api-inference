# Kodif-api-inference
Inference script for Kodif api. 

Main file ```inference.py``` contains ```chain``` function which shall be deployed as a ```put/get``` method in API.

Firstly, we read all models into RAM approximately 4.2gb (by [```get_objects```](https://github.com/SanzharMrz/kodif-api-inference/blob/94d6d840c04d2660efdc257c8930f059267cfa94/inference.py#L67) function), it shall be runned once, while building API.


Then we alternately call [```predict```](https://github.com/SanzharMrz/kodif-api-inference/blob/94d6d840c04d2660efdc257c8930f059267cfa94/inference.py#L44) function inside of our [```chain```](https://github.com/SanzharMrz/kodif-api-inference/blob/94d6d840c04d2660efdc257c8930f059267cfa94/inference.py#L73) and produce the name of class for current utterance.

# Usage
```bash
$ sh get_models.sh # download weights
$ python inference.py
```
