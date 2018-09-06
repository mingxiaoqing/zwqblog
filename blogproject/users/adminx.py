import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset,Main,Side,Row
from django.utils.translation import ugettext as _
from .models import User

class UserInfoAdmin(UserAdmin):
    change_user_password_template = None
    list_display = ('username','name', 'gender', 'birday', 'mobile', 'email','address','date_joined','last_login','is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username','name','mobile', 'email','is_staff')
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


xadmin.site.unregister(User)
xadmin.site.register(User, UserInfoAdmin)
