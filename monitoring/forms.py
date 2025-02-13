from django import forms

TYPES_OF_SEARCH = (
    (1, "По координатам"),
    (2, "По RS id"),
    (3, "По гену"),
    (4, "По болезни")
)


class GettingDataForm(forms.Form):
    search_type = forms.ChoiceField(choices=TYPES_OF_SEARCH)
    gene = forms.CharField()
