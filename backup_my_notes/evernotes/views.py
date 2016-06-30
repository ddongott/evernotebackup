from evernote.api.client import EvernoteClient

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import redirect

EN_CONSUMER_KEY = 'davidgwdong-2447'
EN_CONSUMER_SECRET = '5b772d216fd0c0de'


#https://sandbox.evernote.com/oauth?oauth_callback=http://www.foo.com&oauth_consumer_key=davidgwdong-2447&oauth_nonce=3166905818410889691&oauth_signature=T0+xCYjTiyz7GZiElg1uQaHGQ6I=&oauth_signature_method=HMAC-SHA1&oauth_timestamp=1429565574&oauth_version=1.0

def get_evernote_client(token=None):
    if token:
        return EvernoteClient(token=token, sandbox=True)
    else:
        return EvernoteClient(
            consumer_key=EN_CONSUMER_KEY,
            consumer_secret=EN_CONSUMER_SECRET,
            sandbox=True
        )


def index(request):
    return render_to_response('oauth/index.html')


def auth(request):
    client = get_evernote_client()
    callbackUrl = 'http://%s%s' % (
        request.get_host(), reverse('evernotes:evernote_callback'))
    request_token = client.get_request_token(callbackUrl)

    # Save the request token information for later
    request.session['oauth_token'] = request_token['oauth_token']
    request.session['oauth_token_secret'] = request_token['oauth_token_secret']

    # Redirect the user to the Evernote authorization URL
    return redirect(client.get_authorize_url(request_token))


def callback(request):
    try:
        client = get_evernote_client()
        client.get_access_token(
            request.session['oauth_token'],
            request.session['oauth_token_secret'],
            request.GET.get('oauth_verifier', '')
        )
    except KeyError:
        return redirect('/evernotes/')

    note_store = client.get_note_store()
    notebooks = note_store.listNotebooks()

    return render_to_response('oauth/callback.html', {'notebooks': notebooks})

def savenotes(request):
    if(request.GET.get('save_notes')):
        print request.GET.get('mytextbox')
        print "xxxxxxxxxxx save note button pressed xxxxxx"
        checked_nbs = request.GET.getlist('checked_nbs[]')
        for notebook in checked_nbs:
            print notebook
#        savenotes.saveNotesToHtml( int(request.GET.get('mytextbox')) )
    return render_to_response('base.html')


def reset(request):
    return redirect('/evernotes/')
