from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<name>[-\w]+)/latest/plist/$', "deploy.views.get_plist", name="deploy-latest-plist"),
    url(r'^(?P<name>[-\w]+)/(?P<version>[\w\.\-]+)/plist/$', "deploy.views.get_plist", name="deploy-plist"),
    url(r'^(?P<name>[-\w]+)/latest/ipa/$', "deploy.views.get_ipa", name="deploy-latest-ipa"),
    url(r'^(?P<name>[-\w]+)/(?P<version>[\w\.-]+)/ipa/$', "deploy.views.get_ipa", name="deploy-ipa"),
    url(r'^(?P<name>[-\w]+)/latest/$', "deploy.views.get_latest", name="deploy-latest"),
)
