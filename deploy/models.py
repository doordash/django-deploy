from django.db import models


class App(models.Model):
    name = models.SlugField('App name')
    version = models.CharField(max_length=20)
    plist = models.FileField('Manifest file (plist)', upload_to='ios-builds/%Y-%m-%d')
    ipa = models.FileField('Build file (ipa)', upload_to='ios-builds/%Y-%m-%d')
    is_active = models.BooleanField('Ready for deployment', default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s %s' % (self.name, self.version)

    class Meta:
        unique_together = ('name', 'version')
