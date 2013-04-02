# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Machine'
        db.create_table('invapp_machine', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('invapp', ['Machine'])

        # Adding model 'Collection'
        db.create_table('invapp_collection', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=18, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('invapp', ['Collection'])

        # Adding model 'Project'
        db.create_table('invapp_project', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=18, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('manager', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_collection', to=orm['invapp.Collection'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('invapp', ['Project'])

        # Adding model 'Item'
        db.create_table('invapp_item', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=18, primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('local_id', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_collection', null=True, to=orm['invapp.Collection'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='item_project', null=True, to=orm['invapp.Project'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('original_item_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('rawfiles_loc', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('qcfiles_loc', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('qafiles_loc', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('finfiles_loc', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('ocrfiles_loc', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('invapp', ['Item'])

        # Adding model 'Bag'
        db.create_table('invapp_bag', (
            ('bagname', self.gf('django.db.models.fields.TextField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bag_item', to=orm['invapp.Item'])),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bag_machine', to=orm['invapp.Machine'])),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('bag_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('payload_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('payload_stats', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('invapp', ['Bag'])

        # Adding model 'BagAction'
        db.create_table('invapp_bagaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='bag_action', to=orm['invapp.Bag'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('note', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('invapp', ['BagAction'])

        # Adding unique constraint on 'BagAction', fields ['bag', 'action', 'timestamp']
        db.create_unique('invapp_bagaction', ['bag_id', 'action', 'timestamp'])


    def backwards(self, orm):
        # Removing unique constraint on 'BagAction', fields ['bag', 'action', 'timestamp']
        db.delete_unique('invapp_bagaction', ['bag_id', 'action', 'timestamp'])

        # Deleting model 'Machine'
        db.delete_table('invapp_machine')

        # Deleting model 'Collection'
        db.delete_table('invapp_collection')

        # Deleting model 'Project'
        db.delete_table('invapp_project')

        # Deleting model 'Item'
        db.delete_table('invapp_item')

        # Deleting model 'Bag'
        db.delete_table('invapp_bag')

        # Deleting model 'BagAction'
        db.delete_table('invapp_bagaction')


    models = {
        'invapp.bag': {
            'Meta': {'object_name': 'Bag'},
            'bag_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bagname': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bag_item'", 'to': "orm['invapp.Item']"}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'bag_machine'", 'to': "orm['invapp.Machine']"}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'payload_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'payload_stats': ('django.db.models.fields.TextField', [], {'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'invapp.item': {
            'Meta': {'object_name': 'Item'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_collection'", 'null': 'True', 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'finfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ocrfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'original_item_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'item_project'", 'null': 'True', 'to': "orm['invapp.Project']"}),
            'qafiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'qcfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'rawfiles_loc': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
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
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_collection'", 'to': "orm['invapp.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['invapp']