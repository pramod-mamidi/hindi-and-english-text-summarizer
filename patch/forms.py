from django import forms

class ConForm(forms.Form):
    link= forms.CharField(label="Link or Text",widget=forms.TextInput(attrs={'class':'link','placeholder':'Enter Link / Copy and paste text'}))
