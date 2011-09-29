from django.db import models
from django.contrib.auth.models import User 
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class OssuaryImage(models.Model):
    img   = models.ImageField(upload_to='ossuaryimg/')
    content_type   = models.ForeignKey(ContentType, editable = False)
    object_id      = models.PositiveIntegerField(editable = False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
#    def __str__(self):
#        return "Ossuary Image"


class Taphonomy(models.Model):
    alteration_type       = models.CharField(max_length = 256, blank = True)
    modification_location = models.CharField(max_length = 256, blank = True)
    content_type   = models.ForeignKey(ContentType, editable = False)
    object_id      = models.PositiveIntegerField(editable = False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class BoneRecord(models.Model):
    rev = RegexValidator(regex='[a-zA-Z0-9_]+', message = 'Skeleton Number must be alphanumeric')
    observer        = models.ForeignKey(User)
    date            = models.DateField(blank = True)
    skeleton_number = models.CharField(validators = [rev], max_length = 256, blank = True) #no arithmetic so charfield
    present_location = models.CharField(max_length = 256, blank = True, help_text = "Present collection location") 

    sex_choices = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('?', 'Indeterminate'),
    )

    completeness_choices = (
        ('1, >= 75%',     '1, >= 75%'),
        ('2, 25% - 75%', '2, 25%-75%'),
        ('3, < 25%',     '3, < 25%')
    )

    side_choices = (
        ('Left', 'Left'),
        ('Right', 'Right'),
        ('Both', 'Both'),
        ('Midline', 'Midline'),
        ('Unsidable', 'Unsidable'),
    )

    age       = models.CharField(max_length = 255, blank = True)
    weight    = models.DecimalField(blank = True, help_text = "Weight of bone in kg", decimal_places=3, max_digits=6)
    sex       = models.CharField(max_length = 256, blank = True, choices = sex_choices)
    bone_side = models.CharField(max_length = 256, blank = True, choices = side_choices)
    bone_name = "bone record"
    image     = generic.GenericRelation(OssuaryImage, content_type_field = 'content_type', object_id_field = 'object_id')
    taphonomy = generic.GenericRelation(Taphonomy, content_type_field = 'content_type', object_id_field = 'object_id')

    notes     = models.TextField(blank = True)

    content_type   = models.ForeignKey(ContentType, editable = False)
    object_id      = models.PositiveIntegerField(editable = False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')


class Fragment(BoneRecord):
    completeness        = models.CharField(max_length = 256, blank = True, choices = BoneRecord.completeness_choices)
    minimum_individuals = models.IntegerField(blank = True)
    count               = models.IntegerField(blank = True, help_text = "Number of fragmented materials")
    def __unicode__(self):
        return u'%d Fragments' % (self.count)


class Cranial(BoneRecord):
    completeness = models.CharField(max_length = 256, blank = True, choices = BoneRecord.completeness_choices)
    name_choices = (
        ('frontal',   'Frontal'),
        ('parietal',  'Parietal'),
        ('occipital', 'Occiptal'),
        ('temporal',  'Temporal'),
        ('tmj',       'TMJ'),
        ('sphenoid',  'Sphenoid'),
        ('zygomatic', 'Zygomatic'),
        ('Maxilla',   'Maxilla'),
        ('palatine',  'Palatine'),
        ('mandible',  'Mandible')
    )
    bone_name    = models.CharField(max_length = 256, choices = name_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Cranial records"
    

class LongBone(BoneRecord):
    name_choices = (
        ('humerus', 'Humerus'),
        ('radius',  'Radius'),
        ('ulna',    'Ulna'),
        ('femur',   'Femur'),
        ('tibia',   'Tibia'),
        ('fibula',  'Fibula')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)

    completeness = ""
    proximal_epiphysis_completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    proximal_one_third_completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    distal_one_third_completeness   = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    distal_epiphysis_completeness   = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Long bones"


class Hand(BoneRecord):
    name_choices = (
        ('carpals',     'Carpals'),
        ('metacarpals', 'Metacarpals'),
        ('phalanges',   'Phalanges')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)
    completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Hand bone records"
    

class Foot(BoneRecord):
    name_choices = (
        ('tarsals',     'Tarsals'),
        ('metatarsals', 'Metatarsals'),
        ('phalanges',   'Phalanges'),
        ('talus',       'Talus'),
        ('calcaneus',   'Calcaneus')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)
    completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Foot bone records"


class Postcranial(BoneRecord):
    name_choices = (
        ('clavicle', 'Clavicle'),
        ('scapula_body', 'Scapula - Body'),
        ('scapula_glenoid', 'Scapula - Glenoid Fossa'),
        ('patella', 'Patella'),
        ('sacrum', 'Sacrum'),
        ('ilium', 'Ilium'),
        ('ischium', 'Ischium'),
        ('pubis', 'Pubis'),
        ('acetabulum', 'Acetabulum'),
        ('auricular surface', 'Auricular Surface')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)
    completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Other postcranial bones"


class Vertebra(BoneRecord):
    name_choices = (
        ('C1',   'C1'),
        ('C2',   'C2'),
        ('C3-6', 'C3-6'),
        ('C7',   'C7'),
        ('T1-9', 'T1-9'),
        ('T10',  'T10'),
        ('L1',   'L1'),
        ('L2',   'L2'),
        ('L3',   'L3'),
        ('L4',   'L4'),
        ('L5',   'L5')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)
    centra_present           = models.IntegerField(blank = True)
    neural_arches_present    = models.IntegerField(blank = True)
    centrum_completeness     = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    neural_arch_completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s' % (self.bone_name)

    class Meta:
        verbose_name_plural = "Vertebrae"


class Sternum(BoneRecord):
    bone_name = models.CharField(max_length = 256, default = "Sternum", editable = False, blank = True)
    manubrium_completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    body_completeness      = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s' % (self.bone_name)


class Rib(BoneRecord):
    name_choices = (
        ('Rib 1',    '1st'),
        ('Rib 2',    '2nd'),
        ('Ribs 3-10', '3-10'),
        ('Rib 11',   '11th'),
        ('Rib 12',   '12th')
    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)
    completeness = models.CharField(max_length = 256, choices = BoneRecord.completeness_choices, blank = True)
    def __unicode__(self):
        return u'%s %s' % (self.bone_side, self.bone_name)


class Tooth(BoneRecord):
    name_choices = (
        ('maxillary_central_incisor', 'Maxillary Central Incisor'),
        ('maxillary_lateral_incisor', 'Maxillary Lateral Incisor'),
        ('maxillary_canine', 'Maxillary Canine'),
        ('maxillary_first_premolar', 'Maxillary First Premolar'),
        ('maxillary_second_premolar', 'Maxillary Second Premolar'),
        ('maxillary_first_molar', 'Maxillary First Molar'),
        ('maxillary_second_molar', 'Maxillary Second Molar'),
        ('maxillary_third_molar', 'Maxillary Third Molar'),

        ('mandibular_central_incisor', 'Mandibular Central Incisor'),
        ('mandibular_lateral_incisor', 'Mandibular Lateral Incisor'),
        ('mandibular_canine', 'Mandibular Canine'),
        ('mandibular_first_premolar', 'Mandibular First Premolar'),
        ('mandibular_second_premolar', 'Mandibular Second Premolar'),
        ('mandibular_first_molar', 'Mandibular First Molar'),
        ('mandibular_second_molar', 'Mandibular Second Molar'),
        ('mandibular_third_molar', 'Mandibular Third Molar'),

        ('supernumerary', 'Supernumerary')

    )
    bone_name = models.CharField(max_length = 256, choices = name_choices, blank = True)

    maturity_choices = (
        ('permanent', 'Permanent'),
        ('deciduous', 'Deciduous')
    )
    buccal_notes   = models.TextField(blank = True)
    occlusal_notes = models.TextField(blank = True)
    lingual_notes  = models.TextField(blank = True)
    maturity = models.CharField(blank = True, max_length = 255, choices = maturity_choices)
    def __unicode__(self):
        return u'%s %s %s' % (self.maturity, self.bone_side, self.bone_name)

    class Meta:
        verbose_name_plural = "Teeth"


class Feature(models.Model):
    name = models.CharField(max_length = 256)
    content_type   = models.ForeignKey(ContentType, editable = False)
    object_id      = models.PositiveIntegerField(editable = False)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    cranials     = generic.GenericRelation(Cranial,     content_type_field = 'content_type', object_id_field = 'object_id')
    feet         = generic.GenericRelation(Foot,        content_type_field = 'content_type', object_id_field = 'object_id')
    fragments    = generic.GenericRelation(Fragment,    content_type_field = 'content_type', object_id_field = 'object_id')
    hands        = generic.GenericRelation(Hand,        content_type_field = 'content_type', object_id_field = 'object_id')
    longbones    = generic.GenericRelation(LongBone,    content_type_field = 'content_type', object_id_field = 'object_id')
    postcranials = generic.GenericRelation(Postcranial, content_type_field = 'content_type', object_id_field = 'object_id')
    ribs         = generic.GenericRelation(Rib,         content_type_field = 'content_type', object_id_field = 'object_id')
    sternums     = generic.GenericRelation(Sternum,     content_type_field = 'content_type', object_id_field = 'object_id')
    teeth        = generic.GenericRelation(Tooth,       content_type_field = 'content_type', object_id_field = 'object_id')
    vertebrae    = generic.GenericRelation(Vertebra,    content_type_field = 'content_type', object_id_field = 'object_id')

    def __unicode__(self):
        return u'%s' % (self.name)

class BurialSite(models.Model):
    name = models.CharField(max_length = 256)
    features = generic.GenericRelation(Feature, content_type_field = 'content_type', object_id_field = 'object_id')
    
    def __unicode__(self):
        return u'%s' % (self.name)

