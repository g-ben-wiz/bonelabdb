from burialsite.models import *
from django.contrib import admin
from django.contrib.contenttypes import generic

class GenericLinkedStackedInline(generic.GenericStackedInline):
    template = "admin/linked.html"
    admin_model_path = None

    def __init__(self, *args):
        super(GenericLinkedStackedInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()


class GenericLinkedTabularInline(generic.GenericTabularInline):
    template = "admin/linked.html"
    admin_model_path = None

    def __init__(self, *args):
        super(GenericLinkedTabularInline, self).__init__(*args)
        if self.admin_model_path is None:
            self.admin_model_path = self.model.__name__.lower()


class FeatureInline(GenericLinkedTabularInline):
    model = Feature


class OssuaryImageInline(generic.GenericTabularInline):
    model = OssuaryImage


class TaphonomyInline(generic.GenericTabularInline):
    model = Taphonomy


class CranialInline(GenericLinkedStackedInline):
    model = Cranial
    extra = 0


class FootInline(GenericLinkedStackedInline):
    model = Foot
    extra = 0


class FragmentInline(GenericLinkedStackedInline):
    model = Fragment
    extra = 0


class HandInline(GenericLinkedStackedInline):
    model = Hand
    extra = 0


class LongBoneInline(GenericLinkedStackedInline):
    model = LongBone
    extra = 0


class PostcranialInline(GenericLinkedStackedInline):
    model = Postcranial
    extra = 0


class RibInline(GenericLinkedStackedInline):
    model = Rib
    extra = 0


class SternumInline(GenericLinkedStackedInline):
    model = Sternum
    extra = 0


class ToothInline(GenericLinkedStackedInline):
    model = Tooth
    extra = 0


class VertebraInline(GenericLinkedStackedInline):
    model = Vertebra
    extra = 0


class BoneAdmin(admin.ModelAdmin):
    inlines = [
        OssuaryImageInline,
        TaphonomyInline
    ]


class BurialSiteAdmin(admin.ModelAdmin):
    inlines = [
        FeatureInline
    ]


class FeatureAdmin(admin.ModelAdmin):
    inlines = [
        CranialInline,
        FootInline,
        FragmentInline,
        HandInline,
        LongBoneInline,
        PostcranialInline,
        RibInline,
        SternumInline,
        ToothInline,
        VertebraInline
    ]


admin.site.register(BurialSite, BurialSiteAdmin)
admin.site.register(Feature, FeatureAdmin)

admin.site.register(Cranial, BoneAdmin)
admin.site.register(Foot, BoneAdmin)
admin.site.register(Fragment, BoneAdmin)
admin.site.register(Hand, BoneAdmin)
admin.site.register(LongBone, BoneAdmin)
admin.site.register(Postcranial, BoneAdmin)
admin.site.register(Rib, BoneAdmin)
admin.site.register(Sternum, BoneAdmin)
admin.site.register(Vertebra, BoneAdmin)
