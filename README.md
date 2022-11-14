# Kodif-api-inference
Inference script for Kodif api. 

Main file ```inference.py``` contains ```chain``` function which shall be deployed as a ```put/get``` method in API.

Firstly, we read all models into RAM approximately 4.2gb (```get_objects``` function), it shall be runned once, while building API.


Then we alternately call ```predict``` function inside of our ```chain``` and produce the name of class for current utterance.

# Usage
```bash
$ sh get_models.sh # download weights
$ python inference.py
```
