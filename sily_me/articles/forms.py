from django import forms


class ArticleForm(forms.Form):
    url = forms.URLField(
        label='Article URL',
        required=True,
        widget=forms.URLInput(attrs={'placeholder': 'Enter article URL here'})
    )