#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import pandas as pd

import torch
import torch.nn as nn

import transformers
from transformers import (AutoTokenizer, AutoModel)

from constants import (first, second, third, fourth_a, fourth_b, fourth_c)
from parsing import parse_text

import warnings
warnings.simplefilter('ignore')


class CustomBERTModel(nn.Module):
    def __init__(self, num_classes):
        super(CustomBERTModel, self).__init__()
        self.bert = AutoModel.from_pretrained('bert-base-uncased')
        self.linear1 = nn.Linear(768, 256)
        self.linear2 = nn.Linear(256, num_classes)

    def forward(self, ids, mask):
        sequence_output = self.bert(ids, attention_mask=mask).last_hidden_state
        linear1_output = self.linear1(sequence_output[:, 0, :].view(-1,768))
        linear1_output = nn.functional.relu(linear1_output)
        linear2_output = self.linear2(linear1_output)
        return linear2_output


def get_objects(num_classes, path):
    model = CustomBERTModel(num_classes)
    model.load_state_dict(torch.load(path, map_location=device))
    model = model.to(device)
    model.eval()
    return model


@torch.no_grad()
def predict(model, text, id_to_val):
    inputs = tokenizer(text, max_length=185, padding=True, truncation=True, return_tensors='pt')
    
    outputs = model(ids=inputs['input_ids'].to(device), 
                    mask=inputs['attention_mask'].to(device))
    
    label = np.argmax(outputs.detach().cpu().numpy(), axis=1).item()
    predicted = id_to_val.get(label)
    return predicted

# folder with pt files
root = 'models/'

# can produce an error, shall be edited 
models_path = sorted(list(map(lambda x: os.path.join(root, x), os.listdir(root))), 
                     key=os.path.getmtime)

# next order, first_level_model, second_level, third_level, fourth_level_b, fourth_level_a, fourth_level_c
model_num_classes = list(zip(models_path, [2, 2, 12, 2, 4, 2]))

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
device = torch.device('cpu')

# this stage takes a lot of time, shall be outside of api's predict method
first_model, second_model, third_model, fourth_b_model, fourth_a_model, fourth_c_model = [get_objects(n_cl, path) 
                                                                                          for path, n_cl in model_num_classes]


# main method which takes a text and produces prediction as a text
def chain(text):
    # if you have any option please substitute this function
    text = parse_text(text)
    
    # stage 1
    first_level_prediction = predict(first_model, text, first)
    if first_level_prediction == 'tracking_information':
        return first_level_prediction
    
    # stage 2
    second_level_prediction = predict(second_model, text, second)
    if second_level_prediction == 'other':
        return second_level_prediction
    
    # stage 3
    third_level_prediction = predict(third_model, text, third)
    if third_level_prediction not in ['product_question', 'refund', 'order_cancellation']:
        return third_level_prediction
    
    # stage 4
    if third_level_prediction == 'product_question':
        response = predict(fourth_a_model, text, fourth_a)
    elif third_level_prediction == 'refund':
        response = predict(fourth_b_model, text, fourth_b)
    else:
        response = predict(fourth_c_model, text, fourth_c)
    return response




chain('i need to refund some money bitch')

