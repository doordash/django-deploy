from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.servers.basehttp import FileWrapper
from django.utils import simplejson as json

from deploy.models import App

def get_app(**kwargs):
    if not 'version' in kwargs:
        try:
            app = App.objects.filter(name=kwargs.get('name')).latest('added_at')
        except App.DoesNotExist:
            raise Http404
    else:
        app = get_object_or_404(App, **kwargs)
    return app



def get_plist(request, **kwargs):
    app = get_app(**kwargs)
    response = HttpResponse(FileWrapper(app.plist.file), content_type='text/xml')
    return response


def get_ipa(request, **kwargs):
    app = get_app(**kwargs)
    response = HttpResponse(FileWrapper(app.ipa.file), content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s-%s.ipa' % (app.name, app.version)
    return response


def get_latest(request, **kwargs):
    app = get_app(**kwargs)
    json_response = {'name': app.name,
                     'version': app.version,
                     'manifest': reverse('deploy-plist', args=[app.name, app.version])}
    return HttpResponse(json.dumps(json_response), mimetype='application/json')
