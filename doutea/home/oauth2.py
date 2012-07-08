from doutea.lib.oauth2 import OAuth2
from django.conf import settings

if settings.DEBUG_KEY:
    apikey_name = 'douban-test'
else:
    apikey_name = 'douban'

apikey = settings.APIKEY[apikey_name]

class DoubanOAuth2(OAuth2):
    APIKEY = apikey['apikey']
    APISECRET = apikey['secret']

    authenticate_url = 'https://www.douban.com/service/auth2/auth'
    access_token_url = 'https://www.douban.com/service/auth2/token'
    callback_url = apikey['callback']
    user_info_url = 'https://api.douban.com/people/@me?alt=json'
    response_type = 'code'
    grant_type = 'authorization_code'
    scope = ''

douban = DoubanOAuth2()

