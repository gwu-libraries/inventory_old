# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Machine.url'
        db.alter_column('invapp_machine', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, unique=True, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Machine.url'
        raise RuntimeError("Cannot reverse this migration. 'Machine.url' and its values cannot be restored.")

    models = {
        'invapp.bag': {
            'Meta': {'object_name': 'Bag'},
            'bag_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bagname': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'on_delete': 'models.PROTECT', 'to': "orm['invapp.Item']"}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'on_delete': 'models.PROTECT', 'to': "orm['invapp.Machine']"}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'payload': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        },
        'invapp.bagaction': {
            'Meta': {'unique_together': "(('bag', 'action', 'timestamp'),)", 'object_name': 'BagAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bag_action'", 'to': "orm['invapp.Bag']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'invapp.collection': {
            'Meta': {'object_name': 'Collection'},
            'access_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        },
        'invapp.item': {
            'Meta': {'object_name': 'Item'},
            'access_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['invapp.Collection']", 'blank': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_item_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'on_delete': 'models.SET_NULL', 'default': 'None', 'to': "orm['invapp.Project']", 'blank': 'True', 'null': 'True'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'invapp.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'default': 'None', 'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'invapp.project': {
            'Meta': {'object_name': 'Project'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        }
    }

    complete_apps = ['invapp']