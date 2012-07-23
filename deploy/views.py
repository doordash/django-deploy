from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.utils import simplejson as json

from deploy.models import App


def get_plist(request, **kwargs):
    app = get_object_or_404(App, **kwargs)
    response = HttpResponse(FileWrapper(app.plist.file), content_type='text/xml')
    return response


def get_ipa(request, **kwargs):
    if not 'version' in kwargs:
        app = App.objects.filter(name=kwargs.get('name')).latest('added_at')
    else:
        app = get_object_or_404(App, **kwargs)
    response = HttpResponse(FileWrapper(app.ipa.file), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.ipa' % (app.name, app.version)
    return response


def get_latest(request, **kwargs):
    app = App.objects.filter(**kwargs).latest('added_at')
    json_response = {'name': app.name,
                     'version': app.version,
                     'manifest': reverse('deploy-plist', args=[app.version])}
    return HttpResponse(json.dumps(json_response), mimetype='application/json')
