from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import InstaMemberSingo, InstaMember, InstaBoard

class MActiveBooleanFilter(admin.SimpleListFilter):
    title = _('계정 활성화 상태')
    parameter_name = 'm_active'

    def lookups(self, request, model_admin):
        return (
            (True, _('활성 계정')),
            (False, _('비활성 계정')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(m_active=self.value())
        return queryset
    
class BActiveBooleanFilter(admin.SimpleListFilter):
    title = _('게시물 상태')
    parameter_name = 'b_active'

    def lookups(self, request, model_admin):
        return (
            (True, _('정상')),
            (False, _('숨김')),
        )

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(b_active=self.value())
        return queryset    



@admin.register(InstaMember)
class InstaMemberAdmin(admin.ModelAdmin):
    list_display = ('m_no', 'm_id', 'm_name', 'm_email', 'm_active')
    list_editable = ('m_active',)
    search_fields = ('m_no', 'm_id', 'm_email','m_active',)
    readonly_fields = ('m_no', 'm_id', 'm_pwd', 'm_salt', 'm_name', 'm_email', 'm_img', 'm_date')
    list_filter = (MActiveBooleanFilter,)


@admin.register(InstaMemberSingo)
class InstaMemberSingoAdmin(admin.ModelAdmin):
    list_display = ('ms_no', 'reported_user', 'm_active_status')
    readonly_fields = ('ms_no',)
    actions = ['set_inactive']

    def reported_user(self, obj):
        return obj.ms_no.m_id

    def m_active_status(self, obj):
        return obj.ms_no.m_active

    m_active_status.short_description = 'User Active Status'

    def set_inactive(self, request, queryset):
        updated_count = 0
        for singo in queryset:
            singo.ms_no.m_active = False 
            singo.ms_no.save()
            updated_count += 1

            singo.delete()
        
        self.message_user(request, f'{updated_count}건이 계정 비활성 처리 되었습니다.')

    set_inactive.short_description = '선택된 계정들을 비활성 처리 합니다.'


@admin.register(InstaBoard)
class InstaBoardAdmin(admin.ModelAdmin):
    list_display = ('b_code', 'b_content', 'b_photo', 'b_no', 'b_date', 'b_active')
    list_editable = ('b_active',)
    search_fields = ('b_content', 'b_code', 'b_date', 'b_no',)
    readonly_fields = ('b_code', 'b_content', 'b_photo', 'b_no', 'b_date')
    list_filter = (BActiveBooleanFilter,)

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    


    

admin.site.site_header = '관리자 페이지'
# admin.site.site_title = 'Custom Admin Title'

