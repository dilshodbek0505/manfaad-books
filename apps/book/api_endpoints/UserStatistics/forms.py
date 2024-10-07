from django import forms
from django.utils.translation import gettext_lazy as _
from apps.book.models import UserStatistics


class UserStatisticsForm(forms.ModelForm):
    class Meta:
        model = UserStatistics
        fields = ('user', 'goals', 'categories')

    def clean_goals(self):
        goals = self.cleaned_data['goals']
        if goals.count() > 3:
            raise forms.ValidationError(_("You can only select up to 3 goals"))
        return goals

    def clean_categories(self):
        categories = self.cleaned_data['categories']
        if categories.count() > 3:
            raise forms.ValidationError(_("You can only select up to 3 categories"))
        return categories