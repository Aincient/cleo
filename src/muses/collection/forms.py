from django import forms

__all__ = (
    'ImageForm',
    'ImageFormSet',
)


class ImageForm(forms.Form):
    """Image form."""

    object_number = forms.HiddenInput()
    include = forms.CheckboxInput()


ImageFormSet = forms.formset_factory(ImageForm)
