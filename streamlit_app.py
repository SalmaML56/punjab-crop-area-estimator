import gradio as gr
import pandas as pd
import numpy as np
from crop_yield_model import predict_crop_area  # Assuming you have this function

def estimate_area(rainfall, crop_type, district):
    # You can modify this logic based on your model
    result = predict_crop_area(rainfall, crop_type, district)
    return f"Estimated crop area: {result} hectares"

inputs = [
    gr.Number(label="Rainfall (mm)"),
    gr.Textbox(label="Crop Type"),
    gr.Textbox(label="District")
]

outputs = gr.Textbox(label="Prediction")

demo = gr.Interface(fn=estimate_area, inputs=inputs, outputs=outputs, title="Punjab Crop Area Estimator")
demo.launch()
