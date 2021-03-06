from flask import render_template,Blueprint

errorbp=Blueprint('error_bp',__name__,template_folder='error_bp_templates',static_folder='error_bp_static')

@errorbp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@errorbp.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'),500