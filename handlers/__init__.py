from .main_handlers import register_main_handlers
from .profile_handlers import register_profile_handlers
from .admin_handlers import register_admin_handlers


def register_handlers(dp):
    register_admin_handlers(dp)
    register_main_handlers(dp)
    register_profile_handlers(dp)
