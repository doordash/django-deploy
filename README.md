django-deploy
=============

__In-house enterprise iOS app deployment for Django.__

Django Deploy is a simple Django app to assist in deploying in-house iOS enterprise apps.

You can upload your enterprise app builds and your devices can then check in to ensure that
they are up to date with the latest version.

Getting Started
-----------------

To get started with Django Deploy first clone the source repository:

`git clone git://github.com/stephenmuss/django-ios-notifications.git`.

Next drop the deploy directory into your project root:

`cp -r ./django-deploy/deploy/ /path/to/your/project/`

After that add 'deploy' to your `INSTALLED_APPS` in your settings.py file:

```python
INSTALLED_APPS = (
    # ...
    'deploy',
    # ...
)
```

Finally add Django Deploy's urls to your main urls.py file:

```python
urlpatterns = patterns('',
    # ...
    url(r'^deploy/', include('deploy.urls')),
    # ...
)
```

After this you should be ready to use Django Deploy.


Creating and Uploading Builds
-----------------

At this point you are ready to create and upload your first build.

__One important note to keep in mind__ is that Django Deploy uses the
last section of your app's bundle identifier as the app name. This means
it is important when it comes to specifying the download url when
your are creating the enterprise build in Xcode. For example, if your
bundle identifier is `com.example.foobar` you'll need to use the `foobar`
part when specifying your download url. Therefore when asked by Xcode
for your download url you will need to enter your url as follows:

`http://www.example.com/deploy/foobar/latest/ipa/`.

In this case substituting 'www.example.com' with your server hostname and
'foobar' with the final part of your bundle identifier.

Once you have created your build you should have a plist manifest file
as well as your build ipa file. You can now upload your build to your
Django server. This can be done in the Django Deploy section of your
site's admin.

Point your browser to your site's equivalent of the following url:

http://www.example.com/admin/deploy/app/add/

Simply attach your manifest and build files and check the box which
says the app is ready for deployment. Then submit the form.
Django Deploy will work out the app's name (as discussed above) as well
as the app's version by analysing the manifest file.

The first time installing the app you can simply open the installation
url within mobile Safari. In the case of the `foobar` example above,
you would need to point the device to the following url:

`itms-services://?action=download-manifest&url=http://www.example.com/deploy/foobar/latest/plist/`

This will install the first build on your device.


Ensuring that your device checks in to get the lastest app version.
-----------------

To make sure your device is always up to date with the latest version of the app
you'll need to add some code to your app.

Django deploy has a simple way to check which is the latest version
available for a given app.

To check the latest version you will need to call the url
`http://www.example.com/deploy/foobar/latest/`. This will send a JSON response
as follows:

```javascript
{"version": "1.01", "manifest": "/deploy/1.01/plist/"}
```

The best place to do this is in your AppDelegate class in:

```obj-c
- (void)applicationDidBecomeActive:(UIApplication *)application
```

You can then check your app's current version `[[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleVersion"]`
with the version specified in the JSON response. If the versions do not match you can then
force your app to update by pointing it to the manifest url supplied by the JSON response. e.g.:

```obj-c
NSString *currentVersion = [[[NSBundle mainBundle] infoDictionary] objectForKey:@"CFBundleVersion"];
NSString *latestVersion = [jsonResponse objectForKey:@"version"];
if (! [currentVersion isEqualToString:latestVersion]) {
    NSString *manifestUrlStr = [NSString stringWithFormat:@"http://www.example.com%@",
                                    [jsonResponse objectForKey:@"manifest"]];
    NSString *urlStr = [NSString stringWithFormat:
                            @"itms-services://?action=download-manifest&url=%@", manifestUrlStr];
    [[UIApplication sharedApplication] openURL:[NSURL URLWithString:urlStr]];
}
```

This will point your device to the latest version's manifest file and request the device's user to 
update the app.
