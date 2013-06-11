# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.manager'
        db.delete_column('invapp_project', 'manager')

        # Deleting field 'Project.end_date'
        db.delete_column('invapp_project', 'end_date')

        # Deleting field 'Project.start_date'
        db.delete_column('invapp_project', 'start_date')

        # Deleting field 'Project.access_loc'
        db.delete_column('invapp_project', 'access_loc')


    def backwards(self, orm):
        # Adding field 'Project.manager'
        db.add_column('invapp_project', 'manager',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)

        # Adding field 'Project.end_date'
        db.add_column('invapp_project', 'end_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.start_date'
        db.add_column('invapp_project', 'start_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.access_loc'
        db.add_column('invapp_project', 'access_loc',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)


    models = {
        'invapp.bag': {
            'Meta': {'object_name': 'Bag'},
            'bag_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bagname': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'to': "orm['invapp.Item']"}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bags'", 'to': "orm['invapp.Machine']"}),
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
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
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_item_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'null': 'True', 'to': "orm['invapp.Project']"}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'invapp.machine': {
            'Meta': {'object_name': 'Machine'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        'invapp.project': {
            'Meta': {'object_name': 'Project'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'null': 'True', 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        }
    }

    complete_apps = ['invapp']