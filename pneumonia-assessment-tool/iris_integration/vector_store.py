import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
from sentence_transformers import SentenceTransformer
from .iris_connection import get_db_connection
from sqlalchemy import text
import json  # For serializing and deserializing vectors

# Initialize models
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
resnet_model = models.resnet50(pretrained=True).to(device)
resnet_model.eval()

# Define the image transformation pipeline for ResNet50 model
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Initialize the sentence transformer model for encoding symptoms
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

def process_xray(file):
    """
    Process an X-ray image to extract its feature vector using ResNet50.
    
    :param file: X-ray image file (PIL format)
    :return: Flattened feature vector as a list
    """
    image = Image.open(file).convert('RGB')
    img_t = transform(image)
    batch_t = torch.unsqueeze(img_t, 0).to(device)
    
    with torch.no_grad():
        features = resnet_model(batch_t)
    
    # Return the feature vector as a list
    return features.cpu().numpy().flatten().tolist()

def process_symptoms(symptoms):
    """
    Process symptoms text to extract feature vectors using a sentence transformer.
    
    :param symptoms: List of symptoms
    :return: Feature vector as a list
    """
    return sentence_model.encode(" ".join(symptoms), normalize_embeddings=True).tolist()

def get_all_symptoms(engine):
    """
    Get all unique symptoms from the database.
    
    :param engine: Database engine
    :return: List of symptoms
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT symptoms FROM symptom_data")).fetchall()
    return [symptom for (symptom,) in result]

def store_xray_vector(image_path, diagnosis, feature_vector):
    """
    Store X-ray feature vector in the database.
    
    :param image_path: Path to the X-ray image
    :param diagnosis: Diagnosis associated with the X-ray
    :param feature_vector: Feature vector for the X-ray image
    """
    engine = get_db_connection()
    feature_vector = json.dumps(feature_vector)  # Serialize vector before storing
    with engine.connect() as conn:
        sql = text("""
            INSERT INTO xray_data (image_path, diagnosis, feature_vector)
            VALUES (:image_path, :diagnosis, :feature_vector)
        """)
        conn.execute(sql, {
            'image_path': image_path,
            'diagnosis': diagnosis,
            'feature_vector': feature_vector
        })

def store_symptom_vector(symptoms, feature_vector):
    """
    Store symptom feature vector in the database.
    
    :param symptoms: Symptoms description
    :param feature_vector: Feature vector for the symptoms
    """
    engine = get_db_connection()
    feature_vector = json.dumps(feature_vector)  # Serialize vector before storing
    with engine.connect() as conn:
        sql = text("""
            INSERT INTO symptom_data (symptoms, feature_vector)
            VALUES (:symptoms, :feature_vector)
        """)
        conn.execute(sql, {
            'symptoms': symptoms,
            'feature_vector': feature_vector
        })

def search_similar_xrays(query_vector, top_k=3):
    """
    Search for X-ray images that are most similar to the provided query vector.
    
    :param query_vector: Query feature vector
    :param top_k: Number of top similar X-ray results to return
    :return: List of top-k similar X-rays and their diagnosis
    """
    engine = get_db_connection()
    query_vector = json.dumps(query_vector)  # Serialize vector
    with engine.connect() as conn:
        sql = text("""
            SELECT image_path, diagnosis
            FROM xray_data
            ORDER BY VECTOR_DOT_PRODUCT(CAST(feature_vector AS TEXT), :query_vector) DESC
            LIMIT :top_k
        """)
        results = conn.execute(sql, {'top_k': top_k, 'query_vector': query_vector}).fetchall()
    return results

def search_similar_symptoms(query_vector, top_k=3):
    """
    Search for symptom records that are most similar to the provided query vector.
    
    :param query_vector: Query feature vector
    :param top_k: Number of top similar symptom results to return
    :return: List of top-k similar symptoms
    """
    engine = get_db_connection()
    query_vector = json.dumps(query_vector)  # Serialize vector
    with engine.connect() as conn:
        sql = text("""
            SELECT symptoms
            FROM symptom_data
            ORDER BY VECTOR_DOT_PRODUCT(CAST(feature_vector AS TEXT), :query_vector) DESC
            LIMIT :top_k
        """)
        results = conn.execute(sql, {'top_k': top_k, 'query_vector': query_vector}).fetchall()
    return results
