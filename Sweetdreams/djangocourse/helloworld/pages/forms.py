from django import forms

class JSONUploadForm(forms.Form):
    json_file = forms.FileField(
        label='Select a JSON file',
        widget=forms.FileInput(attrs={'placeholder': 'Choose a JSON file'}),
        error_messages={
            'required': 'Please select a JSON file to upload.',
            'invalid': 'Invalid file format. Please upload a valid JSON file.',
        }
    )
