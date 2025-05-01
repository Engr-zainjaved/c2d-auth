from odoo import http
from odoo.http import request
from werkzeug.utils import redirect

class AutoLogin(http.Controller):
    
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if session_id:
            # First set the cookie and redirect to a confirmation route
            response = redirect(f'/auth/confirm')
            response.set_cookie('session_id', session_id, path='/', httponly=True)
            return response
        return redirect('/web/login')

    @http.route('/auth/confirm', type='http', auth='none', csrf=False)
    def confirm(self, **kwargs):
        # At this point the browser has the session cookie
        return redirect('/web')
