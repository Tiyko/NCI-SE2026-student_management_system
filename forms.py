from allauth.account.forms import LoginForm, SignupForm
from django import forms

#   Edited by:
#   Ionut Ciobanu
#


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Match the login page styling used across the allauth auth screens.

        self.fields["login"].widget.attrs.update({
            "class": "form-control rounded-3 p-2",
            "placeholder": "Username",
        })

        self.fields["password"].widget.attrs.update({
            "class": "form-control rounded-3 p-2",
            "placeholder": "Password",
        })


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        label="First name",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control rounded-3 p-2",
            "placeholder": "First name",
        }),
    )
    last_name = forms.CharField(
        label="Last name",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control rounded-3 p-2",
            "placeholder": "Last name",
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keep the signup form aligned with the login page field sizing and placeholders.

        if "first_name" in self.fields:
            self.fields["first_name"].label = "First name"
        if "last_name" in self.fields:
            self.fields["last_name"].label = "Last name"
        if "email" in self.fields:
            self.fields["email"].label = "Email address"
            self.fields["email"].required = True
            self.fields["email"].widget.attrs.update({
                "class": "form-control rounded-3 p-2",
                "placeholder": "Email address",
            })
        if "username" in self.fields:
            self.fields["username"].widget.attrs.update({
                "class": "form-control rounded-3 p-2",
                "placeholder": "Username",
            })

        ordered_field_names = [
            field_name
            for field_name in ("first_name", "last_name", "email", "username", "password1", "password2")
            if field_name in self.fields
        ]
        ordered_field_names.extend(
            field_name for field_name in self.fields.keys() if field_name not in ordered_field_names
        )
        self.order_fields(ordered_field_names)

    def save(self, request):
        # Persist the required profile fields onto the built-in Django user object.
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name", "").strip()
        user.last_name = self.cleaned_data.get("last_name", "").strip()
        user.save(update_fields=["first_name", "last_name"])
        return user
