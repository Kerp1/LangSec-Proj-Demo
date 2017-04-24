from flask import Flask
from flask import session
from flask import *
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = 'super secret key'


oauth = OAuth()

facebook = oauth.remote_app("facebook",
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='281355375654091',
    consumer_secret='2800e8dd530883365a880c69eb1872ff',
    request_token_params={'scope': 'email'}
)

@app.route("/")
def hello():
    return "Hello World!<b><a href = /login?next=/authenticated>Login</a>"

@app.route("/thisishax")
def thisishax():
  return request.args.get("token")


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized', _external=True,
        next=request.args.get('next') or request.referrer or None))


@app.route('/authenticated')
def authenticated():
  me = facebook.get('/me')
  return 'Logged in as id=%s name=%s' % \
        (me.data['id'], me.data['name'])


@app.route('/oauth-authorized')
@facebook.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    print(resp)


    session['oauth_token'] = (resp['access_token'], '')
    flash('You were successfully logged in')
    return redirect(next_url + "?token=" + resp['access_token'])

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

if __name__ == "__main__":
    app.run()


