from odoo import http
from odoo.http import request, Response
from werkzeug.utils import redirect

class AutoLogin(http.Controller):
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        try:
            session_id = request.httprequest.args.get('session_id')
            if not session_id:
                return redirect('/web/login')
            
            # Create a proper session first
            request.session.authenticate(request.session.db, 'admin', 'admin')
            
            # Set the session ID in cookies
            response = redirect('/web')
            response.set_cookie('session_id', session_id, path='/', httponly=True)
            
            # Ensure session is saved
            request.session['session_id'] = session_id
            request.session.modified = True
            
            return response
            
        except Exception as e:
            return Response("Error during auto-login: %s" % str(e), status=500)
