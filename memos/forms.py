# # forms.py
# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from django.utils.translation import gettext_lazy as _

# class CustomAdminAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(
#         label=_("Email"),
#         max_length=254,  # ここを適宜に調整してください
#         widget=forms.TextInput(attrs={'autocomplete': 'email', 'type': 'email'})
#     )
