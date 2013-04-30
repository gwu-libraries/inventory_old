# -*- coding: utf-8 -*-
import datetime
import json
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models...
        for bag in orm.Bag.objects.all():
            bag.payload = bag.payload_raw
            bag.stats = json.loads(bag.payload_stats)
            bag.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for bag in orm.Bag.objects.all():
            bag.payload_raw = bag.payload
            bag.payload_stats = json.dumps(bag.stats)
            bag.save()

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
            'payload_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payload_stats': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        },
        'invapp.item': {
            'Meta': {'object_name': 'Item'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'null': 'True', 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'finfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ocrfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'original_item_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'null': 'True', 'to': "orm['invapp.Project']"}),
            'qafiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'qcfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'rawfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stats': ('json_field.fields.JSONField', [], {'default': "'null'"})
        }
    }

    complete_apps = ['invapp']
    symmetrical = True
