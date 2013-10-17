# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

        db.rename_column(u'invapp_collection', 'manager', 'contact_person')

    def backwards(self, orm):
        "Write your backwards methods here."

        db.rename_column(u'invapp_collection', 'contact_person', 'manager')

    models = {
        u'invapp.bag': {
            'Meta': {'object_name': 'Bag'},
            'absolute_filesystem_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bag_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bagname': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'on_delete': 'models.PROTECT', 'to': u"orm['invapp.Item']"}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'on_delete': 'models.PROTECT', 'to': u"orm['invapp.Machine']"}),
            'payload': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "u'null'"})
        },
        u'invapp.bagaction': {
            'Meta': {'unique_together': "(('bag', 'action', 'timestamp'),)", 'object_name': 'BagAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bag_action'", 'to': u"orm['invapp.Bag']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'invapp.collection': {
            'Meta': {'object_name': 'Collection'},
            'access_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "u'null'"})
        },
        u'invapp.item': {
            'Meta': {'object_name': 'Item'},
            'access_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['invapp.Collection']", 'blank': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_item_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': u"orm['invapp.Project']", 'blank': 'True', 'null': 'True'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "u'null'"}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'invapp.machine': {
            'Meta': {'object_name': 'Machine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'www_root': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'invapp.project': {
            'Meta': {'object_name': 'Project'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "u'null'"})
        }
    }

    complete_apps = ['invapp']
    symmetrical = True
