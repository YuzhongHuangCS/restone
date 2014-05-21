import webapp2
from webapp2_extras import sessions
from google.appengine.ext import ndb
import os
import urllib
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',}
class User(ndb.Model):
    account=ndb.StringProperty()
    password=ndb.StringProperty()
    email=ndb.StringProperty()
    age=ndb.IntegerProperty()
    JW=ndb.IntegerProperty()
    XW=ndb.IntegerProperty()
    YW=ndb.IntegerProperty()
    TW=ndb.IntegerProperty()
    XG=ndb.IntegerProperty()
    YG=ndb.IntegerProperty()
    usetime=ndb.IntegerProperty()
    date=ndb.DateTimeProperty(auto_now_add=True)
class BaseHandler(webapp2.RequestHandler):              
    def dispatch(self):                                
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)       
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
class MainPage(BaseHandler):
    def get(self):
        template_values={
            'path': 'index.html',
            'account':self.session.get('account')}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
class Login(BaseHandler):
    def get(self):
        self.session.clear()
        template_values={
            'path': 'login.html',
            'account':self.session.get('account')}
        template=JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
    def post(self):
        account=self.request.get('account')
        pw=self.request.get('password')
        if pw== '' or account== '':
            template_values={
                'path':'login.html',
                'msg':'Error: Please specify your account and password',
                'account':self.session.get('account')
                }
            template=JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
            return
        result=User.query(ndb.GenericProperty('account')==account)
        result=result.filter(ndb.GenericProperty('password')==pw)
        resulf=result.fetch(limit=1)
        if len(resulf)>0:
            self.session['account']=account
            template_values={
                'path':'index.html',
                'account':self.session.get('account')
                }
            template=JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
        else:
            template_values={
                'path':'login.html',
                'msg':'Error: Incorrect Password',
                'account':self.session.get('account')
                }
            template=JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
class Logout(BaseHandler):
    def get(self):
        self.session.pop('account')
        template_values={
            'path': 'index.html',
            'account':self.session.get('account')}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
class Apply(BaseHandler):
    def get(self):
        template_values={
            'path': 'apply.html',
            'account':self.session.get('account')}
        template = JINJA_ENVIRONMENT.get_template('apply.html')
        self.response.write(template.render(template_values))
    def post(self):
        DEFAULTVALUE=1
        account=self.request.get('account')
        password=self.request.get('password')
        email=self.request.get('email',default_value='empty')
        age=self.request.get('age',DEFAULTVALUE)
        JW=self.request.get('JW',DEFAULTVALUE)
        XW=self.request.get('XW',DEFAULTVALUE)
        YW=self.request.get('YW',DEFAULTVALUE)
        TW=self.request.get('TW',DEFAULTVALUE)
        XG=self.request.get('XG',DEFAULTVALUE)
        YG=self.request.get('YG',DEFAULTVALUE)
        error=''
        if password=='' or account==''or email=='':
            error='Please at least fill in Account, Password and Email'
        result=User.query(ndb.GenericProperty('account')==account).fetch()
        if len(result)>0:
            error='Account Already Exists'
        if len(error)>2:
            template_values={
                'path':'apply.html',
                'account':self.session.get('account'),
                'error':error}
            template = JINJA_ENVIRONMENT.get_template('apply.html')
            self.response.write(template.render(template_values))
        else:
            newuser=User()
            newuser.account=account
            newuser.password=password
            newuser.email=email
            newuser.age=int(age)
            newuser.JW=int(JW)
            newuser.XW=int(XW)
            newuser.YW=int(YW)
            newuser.TW=int(TW)
            newuser.XG=int(XG)
            newuser.YG=int(YG)
            newuser.usetime=0
            newuser.put()
            self.session['account']=account
            template_values={
                'path': 'index.html',
                'account':account}
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
class settings(BaseHandler):
    def get(self):
        data=User.query(ndb.GenericProperty('account')==self.session['account']).fetch(limit=1)
        currentuser=data[0]
        template_values={
            'age':currentuser.age,
            'JW':currentuser.JW,
            'XW':currentuser.XW,
            'YW':currentuser.YW,
            'TW':currentuser.TW,
            'XG':currentuser.XG,
            'YG':currentuser.YG,
            'path': 'settings.html',
            'account':self.session.get('account'),
            'msg':'Set Your Data Below:'}
        template = JINJA_ENVIRONMENT.get_template('settings.html')
        self.response.write(template.render(template_values))
    def post(self):
        data=User.query(ndb.GenericProperty('account')==self.session['account']).fetch(limit=1)
        currentuser=data[0]
        age=self.request.get('age')
        JW=self.request.get('JW')
        XW=self.request.get('XW')
        YW=self.request.get('YW')
        TW=self.request.get('TW')
        XG=self.request.get('XG')
        YG=self.request.get('YG')
        currentuser.age=int(age)
        currentuser.JW=int(JW)
        currentuser.XW=int(XW)
        currentuser.YW=int(YW)
        currentuser.TW=int(TW)
        currentuser.XG=int(XG)
        currentuser.YG=int(YG)
        currentuser.put()
        template_values={
            'age':currentuser.age,
            'JW':currentuser.JW,
            'XW':currentuser.XW,
            'YW':currentuser.YW,
            'TW':currentuser.TW,
            'XG':currentuser.XG,
            'YG':currentuser.YG,
            'path': 'settings.html',
            'account':self.session.get('account'),
            'msg':'Your Data Have Been Updated!'}
        template = JINJA_ENVIRONMENT.get_template('settings.html')
        self.response.write(template.render(template_values))
class robot(BaseHandler):
    def get(self):
        template_values={
            'path': 'robot.html',
            'account':self.session.get('account'),
            'msg':'Set Your Data Below:'}
        template = JINJA_ENVIRONMENT.get_template('robot.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login',Login),
    ('/logout',Logout),
    ('/apply',Apply),
    ('/settings',settings),
    ('/robot',robot)], config=config, debug=True)
