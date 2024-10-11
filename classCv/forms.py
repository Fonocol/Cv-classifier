# classCv/forms.py

from django import forms

class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label='Télécharger votre CV',
        help_text='Formats supportés : .txt, .pdf',
        required=False  # Rend le champ facultatif pour permettre la saisie manuelle
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Saisissez votre texte ici...'}),
        required=False,
        label='Ou Saisissez du Texte'
    )
