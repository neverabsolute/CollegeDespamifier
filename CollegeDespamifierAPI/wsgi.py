"""
WSGI config for CollegeDespamifierAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/college_despamifier')
sys.path.append('/usr/local/lib/python3.8/dist-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CollegeDespamifierAPI.settings")

try:
    application = get_wsgi_application()
except Exception as e:
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
    else:
        print(f'Error when attempting to initialize WSGI: {e}')
        raise e