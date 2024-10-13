# classCv/views.py

from django.shortcuts import render, redirect
from .forms import ResumeUploadForm
from django.conf import settings
from django.http import JsonResponse
import os
import pickle
import re
import nltk
from pdfminer.high_level import extract_text

#from .utils import predict_sentiment
#from transformers import pipeline

# Charger le modèle Hugging Face pour la classification des sentiments
#sentiment_analyzer = pipeline('sentiment-analysis')

# Télécharger les ressources NLTK si nécessaire
nltk.download('punkt')
nltk.download('stopwords')

# Charger les modèles une seule fois
model_path = os.path.join(settings.BASE_DIR, 'classCv', 'finalized_model.pkl')
tfidt_path = os.path.join(settings.BASE_DIR, 'classCv', 'tfidt.pkl')

with open(model_path, 'rb') as f:
    knn = pickle.load(f)

with open(tfidt_path, 'rb') as f:
    tfidt = pickle.load(f)

# Dictionnaire de mapping des catégories
CATEGORY_MAPPING = {
    19: 'HR',
    13: 'DESIGNER',
    20: 'INFORMATION-TECHNOLOGY',
    23: 'TEACHER',
    1: 'ADVOCATE',
    9: 'BUSINESS-DEVELOPMENT',
    18: 'HEALTHCARE',
    17: 'FITNESS',
    2: 'AGRICULTURE',
    8: 'BPO',
    22: 'SALES',
    12: 'CONSULTANT',
    14: 'DIGITAL-MEDIA',
    5: 'AUTOMOBILE',
    10: 'CHEF',
    16: 'FINANCE',
    3: 'APPAREL',
    15: 'ENGINEERING',
    0: 'ACCOUNTANT',
    11: 'CONSTRUCTION',
    21: 'PUBLIC-RELATIONS',
    7: 'BANKING',
    4: 'ARTS',
    6: 'AVIATION'
}

def getHome(request):
    category_name = None
    text_content = ""

    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data.get('resume')
            user_text = form.cleaned_data.get('text')

            if resume_file:
                resume_text = extract_resume_text(resume_file)
                text_content = resume_text
            elif user_text:
                text_content = user_text

            if text_content:
                # Pré-traitement du texte
                cleaned_text = clean_text(text_content)

                # Transformation TF-IDF
                resume_transformed = tfidt.transform([cleaned_text])

                # Prédiction
                predict_id = knn.predict(resume_transformed)[0]
                category_name = CATEGORY_MAPPING.get(predict_id, 'Unknown')

            # Vérifier si la requête est AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category_name': category_name,
                    'text_content': text_content
                })
    else:
        form = ResumeUploadForm()

    context = {
        'form': form,
        'category_name': category_name,
        'text_content': text_content
    }
    return render(request, 'classCv/layout/home.html', context)

def extract_resume_text(resume_file):
    filename = resume_file.name
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext == '.txt':
        return resume_file.read().decode('utf-8', errors='ignore')
    elif file_ext == '.pdf':
        # Sauvegarder temporairement le fichier PDF pour extraction
        temp_path = os.path.join(settings.MEDIA_ROOT, 'temp_resume.pdf')
        with open(temp_path, 'wb+') as destination:
            for chunk in resume_file.chunks():
                destination.write(chunk)
        # Extraire le texte du PDF
        text = extract_text(temp_path)
        # Supprimer le fichier temporaire
        os.remove(temp_path)
        return text
    else:
        return ""

def clean_text(text):
    # Exemple de nettoyage : suppression des caractères spéciaux et mise en minuscules
    text = re.sub(r'\W+', ' ', text)
    text = text.lower()
    return text

def about(request):
    return render(request, 'classCv/layout/abaout.html')



def comment_view2(request):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user_comment = request.POST.get('comment', '').strip()
        if user_comment:
            # Prédiction de sentiment avec Hugging Face Transformers
            prediction = sentiment_analyzer(user_comment)[0]
            label = prediction['label']
            score = prediction['score']

            # Reformater la réponse selon le sentiment détecté
            sentiment = "positif" if label == "POSITIVE" else "négatif"

            # Retourner une réponse JSON
            return JsonResponse({
                'success': True,
                'message': f"Votre message '{user_comment}' est {sentiment} avec un score de confiance de {score:.2f}."
            })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        }, status=400)

def comment_page(request):
    # Simple page rendering
    return render(request, 'classCv/layout/comment.html')

def comment_view(request):
    if request.method == "POST":
        user_comment = request.POST.get('comment')
        
        # Simple analyse de sentiment basé sur des mots
        positive_keywords = ['good', 'happy', 'love', 'great', 'excellent', 'proud', 'amazing', 'awesome']
        negative_keywords = ['bad', 'sad', 'angry', 'terrible', 'horrible', 'hate']

        if any(word in user_comment.lower() for word in positive_keywords):
            response = "Your comment is positive!"
        elif any(word in user_comment.lower() for word in negative_keywords):
            response = "Your comment is negative!"
        else:
            response = "Your comment is neutral."

        return JsonResponse({'success': True, 'response': response})
    
    return render(request, 'classCv/layout/comment.html')

