from django.http import HttpResponse
from django.urls import reverse
from authlib.integrations.django_client import OAuth

import config

oauth = OAuth()
oauth.register(
    name = 'camdram',
    client_id = config.API_KEY,
    client_secret = config.API_SECRET,
    access_token_url = config.CAMDRAM_URL + '/oauth/v2/token',
    access_token_params=None,
    authorize_url = config.CAMDRAM_URL + '/oauth/v2/auth',
    authorize_params=None,
    api_base_url = config.CAMDRAM_URL,
    client_kwargs={'scope': 'user_shows user_orgs'},
)

def home(request):
    login_uri = reverse('login')
    return HttpResponse(f'<a href="{login_uri}">Login with Camdram</a>')

def login(request):
    redirect_uri = request.build_absolute_uri(reverse('info'))
    return oauth.camdram.authorize_redirect(request, redirect_uri)

def info(request):
    token = oauth.camdram.authorize_access_token(request)
    user = oauth.camdram.get('/auth/account.json', token=token).json()
    shows = oauth.camdram.get('/auth/account/shows.json', token=token).json()
    organisations = oauth.camdram.get('/auth/account/organisations.json', token=token).json()

    response = HttpResponse()
    response.write('<h1>Hello ' + user['name'] + '</h1>')

    response.write('<h2>My Shows:</h2><ul>')
    for show in shows:
        response.write('<li>' + show['name'] + '</li>')
    response.write('</ul>')

    response.write('<h2>My Organisations:</h2><ul>')
    for organisation in organisations:
        response.write('<li>' + organisation['name'] + '</li>')
    response.write('</ul>')

    return response
