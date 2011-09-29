from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count
from burialsite.models import *
from django.contrib.auth import authenticate, logout, login 
from django.contrib.auth.forms import AuthenticationForm


def home_redirect(request):
    return redirect('/burialsite/')

def sitelogout(request):
    logout(request)
    return redirect('/burialsite/')

def sitelogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('/burialsite')
        else:
            return redirect('/disabledaccount')
    else:
        return redirect('/invalidlogin')

    return redirect('/burialsite')


def homepage(request):
    t = loader.get_template('burialsite/homepage.html')
    af = AuthenticationForm(request)
    c = RequestContext(request, {
        'burial_sites': BurialSite.objects.all(),
        'login_form' : af
    })
    return HttpResponse(t.render(c))


def invalidlogin(request):
    t = loader.get_template('burialsite/invalidlogin.html')
    af = AuthenticationForm(request)
    c = RequestContext(request, {
        'burial_sites': BurialSite.objects.all(),
        'login_form' : af
    })
    return HttpResponse(t.render(c))


def disabledaccount(request):
    t = loader.get_template('burialsite/disabledaccount.html')
    af = AuthenticationForm(request)
    c = RequestContext(request, {
        'burial_sites': BurialSite.objects.all(),
        'login_form' : af
    })
    return HttpResponse(t.render(c))


def burial_site(request, burial_site_id):
    #features at burial site n
    features = Feature.objects.filter(burialsite = get_object_or_404(BurialSite, id = burial_site_id))

    af = AuthenticationForm(request)
    t = loader.get_template('burialsite/burial_site.html')
    c = RequestContext(request, {
        'login_form' : af,
        'burial_site': get_object_or_404(BurialSite, id = burial_site_id),
        'features': features,
    })
    return HttpResponse(t.render(c))


def feature(request, burial_site_id, feature_id):
    af = AuthenticationForm(request)
    #skeletons at feature n
    burial_site = get_object_or_404(BurialSite, id = burial_site_id)
    burial_site_type = ContentType.objects.get_for_model(BurialSite)

    feature = get_object_or_404(Feature, id = feature_id, content_type__pk = burial_site_type.id, object_id = burial_site.id)
    feature_type = ContentType.objects.get_for_model(Feature)

    skeletons = []
    skeletons.extend(BoneRecord.objects.filter(content_type__pk=feature_type.id, object_id = feature.id).values('skeleton_number').annotate(number_bones = Count('skeleton_number')))

    t = loader.get_template('burialsite/feature.html')
    c = RequestContext(request, {
        'login_form' : af,
        'feature': get_object_or_404(Feature, id = feature_id),
        'burial_site': get_object_or_404(BurialSite, id=burial_site_id),
        'skeletons' :  skeletons,
    })
    return HttpResponse(t.render(c))


def skeleton(request, burial_site_id, feature_id, skeleton_id):
    af = AuthenticationForm(request)
    t = loader.get_template('burialsite/skeleton.html')

    burial_site = get_object_or_404(BurialSite, id = burial_site_id)
    burial_site_type = ContentType.objects.get_for_model(BurialSite)

    feature = get_object_or_404(Feature, id = feature_id, content_type__pk = burial_site_type.id, object_id = burial_site.id)
    feature_type = ContentType.objects.get_for_model(Feature)

    cranial_records     = Cranial.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    foot_records        = Foot.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    fragment_records    = Fragment.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    hand_records        = Hand.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    longbone_records    = LongBone.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    postcranial_records = Postcranial.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    rib_records         = Rib.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    sternum_records     = Sternum.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    tooth_records       = Tooth.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)
    vertebra_records    = Vertebra.objects.filter(content_type__pk = feature_type.id, object_id = feature.id, skeleton_number = skeleton_id)


    cranial_pics     = []
    foot_pics        = []
    fragment_pics    = []
    hand_pics        = []
    longbone_pics    = []
    postcranial_pics = []
    rib_pics         = []
    sternum_pics     = []
    tooth_pics       = []
    vertebra_pics    = []

    cranial_taphonomies     = []
    foot_taphonomies        = []
    fragment_taphonomies    = []
    hand_taphonomies        = []
    longbone_taphonomies    = []
    postcranial_taphonomies = []
    rib_taphonomies         = []
    sternum_taphonomies     = []
    tooth_taphonomies       = []
    vertebra_taphonomies    = []

    cranial_type     = ContentType.objects.get_for_model(Cranial)
    foot_type        = ContentType.objects.get_for_model(Foot)
    fragment_type    = ContentType.objects.get_for_model(Fragment)
    hand_type        = ContentType.objects.get_for_model(Hand)
    longbone_type    = ContentType.objects.get_for_model(LongBone)
    postcranial_type = ContentType.objects.get_for_model(Postcranial)
    rib_type         = ContentType.objects.get_for_model(Rib)
    sternum_type     = ContentType.objects.get_for_model(Sternum)
    tooth_type       = ContentType.objects.get_for_model(Tooth)
    vertebra_type    = ContentType.objects.get_for_model(Vertebra)


    for fragment_record in fragment_records:
        fragment_pics.extend(OssuaryImage.objects.filter(content_type__pk=fragment_type.id, 
                                                      object_id = fragment_record.id))
        fragment_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=fragment_type.id, 
                                                      object_id = fragment_record.id))

    for cranial_record in cranial_records:
        cranial_pics.extend(OssuaryImage.objects.filter(content_type__pk=cranial_type.id, 
                                                      object_id = cranial_record.id))
        cranial_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=cranial_type.id, 
                                                      object_id = cranial_record.id))

    for longbone_record in longbone_records:
        longbone_pics.extend(OssuaryImage.objects.filter(content_type__pk=longbone_type.id, 
                                                      object_id = longbone_record.id))
        longbone_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=longbone_type.id, 
                                                      object_id = longbone_record.id))

    for hand_record in hand_records:
        hand_pics.extend(OssuaryImage.objects.filter(content_type__pk=hand_type.id, 
                                                      object_id = hand_record.id))
        hand_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=hand_type.id, 
                                                      object_id = hand_record.id))

    for foot_record in foot_records:
        foot_pics.extend(OssuaryImage.objects.filter(content_type__pk=foot_type.id, 
                                                      object_id = foot_record.id))
        foot_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=foot_type.id, 
                                                      object_id = foot_record.id))

    for postcranial_record in postcranial_records:
        postcranial_pics.extend(OssuaryImage.objects.filter(content_type__pk=postcranial_type.id, 
                                                      object_id = postcranial_record.id))
        postcranial_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=postcranial_type.id, 
                                                      object_id = postcranial_record.id))

    for vertebra_record in vertebra_records:
        vertebra_pics.extend(OssuaryImage.objects.filter(content_type__pk=vertebra_type.id, 
                                                      object_id = vertebra_record.id))
        vertebra_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=vertebra_type.id, 
                                                      object_id = vertebra_record.id))
    
    for sternum_record in sternum_records:
        sternum_pics.extend(OssuaryImage.objects.filter(content_type__pk=sternum_type.id, 
                                                      object_id = sternum_record.id))
        sternum_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=sternum_type.id, 
                                                      object_id = sternum_record.id))

    for rib_record in rib_records:
        rib_pics.extend(OssuaryImage.objects.filter(content_type__pk=rib_type.id, 
                                                      object_id = rib_record.id))
        rib_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=rib_type.id, 
                                                      object_id = rib_record.id))

    for tooth_record in tooth_records:
        tooth_pics.extend(OssuaryImage.objects.filter(content_type__pk=tooth_type.id, 
                                                      object_id = tooth_record.id))
        tooth_taphonomies.extend(Taphonomy.objects.filter(content_type__pk=tooth_type.id, 
                                                      object_id = tooth_record.id))

    c = RequestContext(request, {
        'login_form' : af,
        'skeleton_id' : skeleton_id,
        'burial_site' : burial_site,
        'feature' : feature,

        'cranial_records' : cranial_records,
        'foot_records'    : foot_records,
        'fragment_records': fragment_records,
        'hand_records'    : hand_records,
        'longbone_records': longbone_records,
        'postcranial_records' : postcranial_records,
        'rib_records'     : rib_records,
        'sternum_records' : sternum_records,
        'tooth_records'   : tooth_records,
        'vertebra_records' : vertebra_records,

        'cranial_pics' : cranial_pics,
        'foot_pics'    : foot_pics,
        'fragment_pics': fragment_pics,
        'hand_pics'    : hand_pics,
        'longbone_pics': longbone_pics,
        'postcranial_pics' : postcranial_pics,
        'rib_pics'     : rib_pics,
        'sternum_pics' : sternum_pics,
        'tooth_pics'   : tooth_pics,
        'vertebra_pics' : vertebra_pics,

        'cranial_taphs' : cranial_taphonomies,
        'foot_taphs'    : foot_taphonomies,
        'fragment_taphs': fragment_taphonomies,
        'hand_taphs'    : hand_taphonomies,
        'longbone_taphs': longbone_taphonomies,
        'postcranial_taphs' : postcranial_taphonomies,
        'rib_taphs'     : rib_taphonomies,
        'sternum_taphs' : sternum_taphonomies,
        'tooth_taphs'   : tooth_taphonomies,
        'vertebra_taphs' : vertebra_taphonomies
    })

    
    return HttpResponse(t.render(c))

