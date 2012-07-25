from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError
from django.utils import simplejson as json
from django.template.base import TemplateDoesNotExist

from deploy.models import App

sample_plist = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
        <key>items</key>
        <array>
                <dict>
                        <key>assets</key>
                        <array>
                                <dict>
                                        <key>kind</key>
                                        <string>software-package</string>
                                        <key>url</key>
                                        <string>%s</string>
                                </dict>
                        </array>
                        <key>metadata</key>
                        <dict>
                                <key>bundle-identifier</key>
                                <string>com.example.someapp</string>
                                <key>bundle-version</key>
                                <string>%s</string>
                                <key>kind</key>
                                <string>software</string>
                                <key>title</key>
                                <string>App Title</string>
                        </dict>
                </dict>
        </array>
</dict>
</plist>
'''

class AppTest(TestCase):
    def get_app(self, version):
        plist_str = sample_plist % ('someapp', version)
        plist = ContentFile(plist_str.encode('UTF-8'))
        plist.name = 'someapp.plist'
        ipa = ContentFile(b'Some Data')
        ipa.name = 'someapp.ipa'
        plist.name = 'someapp.plist'
        app = App(name='someapp', version=version, plist=plist, ipa=ipa, is_active=True)
        return app

    def setUp(self):
        self.app = self.get_app('1.0')
        self.app.save()

    def test_unique_together_name_and_version(self):
        non_unique_app = self.get_app('1.0')
        self.assertRaises(IntegrityError, non_unique_app.save)


    def test_get_latest_app_info(self):
        new_app = self.get_app('1.1')
        new_app.save()
        response = self.client.get(reverse('deploy-latest', args=['someapp']))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual(new_app.version, data['version'])
        self.assertNotEqual(self.app.version, data['version'])

    def test_get_plist(self):
        url = reverse('deploy-plist', args=[self.app.name, self.app.version])
        response = self.client.get(url)
        self.assertTrue(response.has_header('content-type'))
        self.assertEqual('text/xml', response._headers['content-type'][1])
        self.assertEqual(self.app.plist.read(), response.content)

    def test_inactive_apps_excluded_when_getting_latest(self):
        not_ready_to_be_deployed_app = self.get_app('1.1')
        not_ready_to_be_deployed_app.is_active = False
        not_ready_to_be_deployed_app.save()
        response = self.client.get(reverse('deploy-latest', args=['someapp']))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertNotEqual(not_ready_to_be_deployed_app.version, data['version'])
        self.assertEqual(self.app.version, data['version'])

    def test_get_latest_ipa(self):
        response = self.client.get(reverse('deploy-latest-ipa',
                                   args=[self.app.name]))
        self.assertTrue(response.has_header('content-type'))
        self.assertEqual('application/octet-stream',
                         response._headers['content-type'][1])
        self.assertEqual(self.app.ipa.read(), response.content)

    def test_get_invalid_app(self):
        """
        Catches cases where a 404.html template does not exist.
        We are still basically testing that the response status
        is 404.
        """
        try:
            response = self.client.get(reverse('deploy-latest', args=['blah']))
            self.assertEqual(404, response.status_code)
        except Exception as e:
            self.assertEqual(TemplateDoesNotExist, e.__class__)
            self.assertTrue('404.html' in e.message)
