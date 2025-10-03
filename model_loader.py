from transformers import pipeline

def load_model(model_name="google/flan-t5-base"):
    """
    Load Flan-T5 model with text2text-generation pipeline.
    """
    return pipeline("text2text-generation", model=model_name)