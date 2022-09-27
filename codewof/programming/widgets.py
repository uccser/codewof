"""Widgets for programming application."""

from django import forms

# https://docs.djangoproject.com/en/3.2/ref/forms/fields/#iterating-relationship-choices

# https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#checkboxselectmultiple

# https://github.com/django/django/blob/b9e872b59329393f615c440c54f632a49ab05b78/django/forms/widgets.py#L621


class IndentCheckbox(forms.CheckboxSelectMultiple):
    """IndentCheckbox extended from CheckboxSelectMultiple.

    Intended for use in the question filtering system
    Indents checkboxes based on the indent level of stored in the object, and sets the filter attribute to number.
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Indent the checkbox based on the indent level stored in the object."""
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['data-indent-level'] = value.instance.indent_level
            option['attrs']['filter'] = value.instance.number
        return option


class DifficultyCheckbox(forms.CheckboxSelectMultiple):
    """DifficultyCheckbox extended from CheckboxSelectMultiple.

    Intended for use in the question filtering system
    Sets the filter attribute to level.
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Indent the checkbox based on the indent level stored in the object."""
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['filter'] = value.instance.level
        return option


class TypeCheckbox(forms.CheckboxSelectMultiple):
    """TypeCheckbox extended from CheckboxSelectMultiple.

    Intended for use in the question filtering system
    Sets the filter attribute to value.
    """

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Indent the checkbox based on the indent level stored in the object."""
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['attrs']['filter'] = value
        return option
