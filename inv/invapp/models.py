from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=256)
    gwulid = models.CharField(max_length=17, blank=True)
    create_date = models.DateTimeField()
    
class Collection(Entity):
    description = models.TextField(blank=True)
    manager = models.ForeignKey('Person', related_name='collection_manager')

class Item(Entity):
    collection = models.ForeignKey(Collection, related_name='item_collection', blank=True)

class Copy(Entity):
    item = models.ForeignKey(Item, related_name='copy_item')
    machine = models.ForeignKey('Machine', related_name='copy_machine')
    path = models.URLField()
    
    def get_full_path(self):
        pass
    
class Machine(models.Model):
    name = models.CharField(max_length=256)
    create_date = models.DateTimeField()
    owner = models.ForeignKey('Organization', related_name='%(class)s_owner')
    address = models.ForeignKey('Address', blank=True, related_name='%(class)s_address')

class Address(models.Model):
    street_number = models.CharField(max_length=36, blank=True)
    street_name = models.CharField(max_length=256, blank=True)
    building = models.CharField(max_length=256, blank=True)
    room_number = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=32, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.IntegerField(max_length=5, blank=True)
        
class Server(Machine):
    ip = models.IPAddressField()
    os = models.CharField(max_length=36)

class OfflineStorage(Machine):
    HARDWARE_TYPES = (
        ('h','hard drive'),
        ('u','USB drive'),
        ('c','CD-ROM'),
        ('d','DVD-ROM'),
        ('z','Iomega Zip disk'), # :P
        # and so on...
        )
    hardware_type = models.CharField(max_length=1, choices=HARDWARE_TYPES)
    notes = models.TextField(blank=True)

class Actor(models.Model):
    name = models.CharField(max_length=256)
    create_date = models.DateTimeField()

class Person(Actor):
    phone = models.IntegerField(blank=True)
    email = models.EmailField()
    organization = models.ForeignKey('Organization', blank=True, related_name='person_organization')

class System(Actor):
    machine = models.ForeignKey(Machine, related_name='system_machine')

class Organization(models.Model):
    create_date = models.DateTimeField()
    name = models.CharField(max_length=256)
    address = models.ForeignKey(Address, related_name='organization_address')
    parent_org = models.ForeignKey('Organization', blank=True, related_name='organization_parent')
    primary_contact = models.ForeignKey(Person, blank=True, related_name='organization_contact')

class Action(models.Model):
    ACTIONS = (
        ('1','minted GWUL identifier'),
        ('2','physical item submitted to library'),
        # and so on...
        )
        
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    actor = models.ForeignKey(Actor, related_name='action_actor')
    entity = models.ForeignKey(Entity, related_name='action_entity')

class Project(models.Model):
    create_date = models.DateTimeField()
    name = models.CharField(max_length=256)
    manager = models.ForeignKey(Person, related_name='project_manager')
    collection = models.ForeignKey(Collection, related_name='project_collection')
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    # Common Recipe Information
    create_mets = models.BooleanField()
    create_access_copy = models.BooleanField()
    create_preservation_copy = models.BooleanField()
    create_external_copy = models.BooleanField()
    external_copy_recipient = models.ForeignKey(Actor, blank=True, related_name='project_external_recipient')
    
class ReformattingProject(Project):

    class Meta():
        abstract = True

class ImageReformattingProject(ReformattingProject):
    OUTPUT_FORMATS = (
        ('jpeg','jpeg'),
        ('tiff','TIFF'),
        ('jp2k','JPEG2000'),
        )
    # scanning recipe info
    scan_dpi = models.IntegerField(max_length=4)
    # QC recipe info
    crop = models.BooleanField()
    deskew = models.BooleanField()
    color_correction = models.BooleanField()
    # QA recipe info
    qa_image_percentage = models.IntegerField(max_length=3)
    # image conversion recipe info
    # BIG QUESTION: How to specify different options for access and preservation copies? Nested projects?
    output_format = models.CharField(max_length=4, choices=OUTPUT_FORMATS)
    jpeg_quality = models.IntegerField(max_length=3, blank=True)
    jp2k_quality = models.IntegerField(max_length=3, blank=True)
    create_pdf = models.BooleanField()
    ocr = models.BooleanField()
    alto = models.BooleanField()
    
    class Meta():
        abstract = True
    
class BookScanningProject(ImageReformattingProject):
    SCAN_FORMATS = (
        ('jpeg','jpeg'),
        ('raw','raw'),
        )
    
    scan_format = models.CharField(max_length=4, choices=SCAN_FORMATS)
    
class MicrofilmScanningProject(ImageReformattingProject):
    SCAN_FORMATS = (
        ('jpeg','jpeg'),
        ('tiff','tiff'),
        )
    
    scan_format = models.CharField(max_length=4, choices=SCAN_FORMATS)

class LoosePaperScanningProject(ImageReformattingProject):
    SCAN_FORMATS = (
        ('jpeg','jpeg'),
        ('raw','raw'),
        )

    scan_format = models.CharField(max_length=4, choices=SCAN_FORMATS)
    
class AudioReformattingProject(ReformattingProject):
    pass
    
class VideoReformattingProject(ReformattingProject):
    pass
    
