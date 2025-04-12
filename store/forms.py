
from django import forms
from .models import Review
from .models import Item, Review  # ✅ Add this line if missing

class ReviewForm(forms.ModelForm):
    reviewer_last_name = forms.CharField(
        max_length=50, required=True, label="Last Name"
    )
    rating = forms.ChoiceField(
        choices=[(i, f"{i} star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="Rating"
    )
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label="Review Text",
        required=True
    )
    class Meta:
        model = Review
        fields = ['reviewer_last_name', 'rating', 'comment']
class ItemForm(forms.ModelForm):
    category = forms.CharField(label='Category', required=False, disabled=True)

    class Meta:
        model = Item
        fields = ['name', 'subcategory', 'brand', 'price', 'discount_price', 'image', 'description', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['category'].initial = self.instance.subcategory.category.name
