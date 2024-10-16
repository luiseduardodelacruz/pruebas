
def make_prediction(predictor, project_id, iteration_name, image_bytes):
    try:
        return predictor.detect_image(project_id, iteration_name, image_bytes)
    except Exception as e:
        raise ValueError(f"Error al hacer la predicción: {e}")

def filter_predictions(predictions, threshold=0.15):
    return [pred for pred in predictions if pred.probability > threshold]
