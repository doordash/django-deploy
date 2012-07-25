from xml.dom import minidom

from django import forms
from deploy.models import App


class AppForm(forms.ModelForm):
    def clean_plist(self):
        if not 'plist' in self.files:
            raise forms.ValidationError('No plist file attached.')
        plist = self.files['plist']
        extension = plist.name.split('.')[-1]
        if extension != 'plist':
            raise forms.ValidationError('Invalid plist file.')
        return self.cleaned_data['plist']

    def clean_ipa(self):
        if not 'ipa' in self.files:
            raise forms.ValidationError('No ipa file attached.')
        ipa = self.files['ipa']
        extension = ipa.name.split('.')[-1]
        if extension != 'ipa':
            raise forms.ValidationError('Invalid ipa file.')
        return self.cleaned_data['ipa']

    def clean_name(self):
        identifier = self.get_key_value_from_plist('bundle-identifier')
        name = identifier.split('.')[-1]
        self.cleaned_data['name'] = name
        return self.cleaned_data['name']

    def clean_version(self):
        version = self.get_key_value_from_plist('bundle-version')
        self.cleaned_data['version'] = version
        return self.cleaned_data['version']

    def get_key_value_from_plist(self, key):
        if not hasattr(self, 'dom'):
            plist = self.files['plist']
            self.dom = minidom.parse(plist)
        value = None
        for e in self.dom.getElementsByTagName('key'):
            if e.childNodes[0].nodeValue == key:
                value = e.nextSibling.nextSibling.childNodes[0].nodeValue

        return value

    class Meta:
        model = App
        # It is important that plist is validated before name and version
        fields = ('plist', 'ipa', 'is_active', 'name', 'version')
        widgets = {'name': forms.HiddenInput({'value': 'default'}),
                   'version': forms.HiddenInput({'value': 'default'})}
