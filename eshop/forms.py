from django import forms
class CartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(min_value=1, initial=1)
    action = forms.ChoiceField(choices=[("add", "Add"), ("increase", "Increase"),
                                        ("decrease", "Decrease"), ("remove", "Remove")])

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data.get("product_id")
        if not product_id:
            raise forms.ValidationError("Product ID is required")
        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-100 form-control border-0 py-3 mb-4',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-100 form-control border-0 py-3 mb-4',
            'placeholder': 'Enter Your Email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-100 form-control border-0 mb-4',
            'rows': '5',
            'cols': '10',
            'placeholder': 'Your Message'
        })
    )
