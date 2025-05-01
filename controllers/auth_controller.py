from odoo import http
from odoo.http import request, Response
from werkzeug.utils import redirect
import time

class AutoLogin(http.Controller):
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if not session_id:
            return redirect('/web/login')
            
        # Create a response that sets the cookie first
        response = Response("""
            <html>
                <head>
                    <meta http-equiv="refresh" content="0;url=/web" />
                </head>
                <body>
                    <script>
                        document.cookie = 'session_id={}; path=/; httponly'.replace('{}', '{value}');
                    </script>
                </body>
            </html>
        """.format('{value}', value=session_id))
        
        # Also set the cookie via HTTP headers as backup
        response.set_cookie('session_id', session_id, path='/', httponly=True)
        
        return response
