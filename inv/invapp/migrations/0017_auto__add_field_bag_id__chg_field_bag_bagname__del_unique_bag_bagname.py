# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        db.delete_foreign_key('invapp_bagaction', 'bag_id')
        # Removing unique constraint on 'Bag', fields ['bagname']
        db.delete_primary_key('invapp_bag')

        # Adding field 'Bag.id'
        db.add_column(u'invapp_bag', u'id',
                      self.gf('django.db.models.fields.IntegerField')(primary_key=True, default=0),
                      keep_default=False)

        db.delete_column(u'invapp_bagaction', 'bag_id')

        db.add_column(u'invapp_bagaction', 'bag_id', self.gf('django.db.models.fields.IntegerField')(default=0))

        db.execute("CREATE SEQUENCE invapp_bag_id_seq")
        db.execute("ALTER TABLE invapp_bag ALTER COLUMN id "
                   "SET DEFAULT nextval('invapp_bag_id_seq'::regclass)")

        sql = db.foreign_key_sql('invapp_bagaction', 'bag_id', 'invapp_bag', 'id')
        db.execute(sql)

        # Changing field 'Bag.bagname'
        db.alter_column(u'invapp_bag', 'bagname', self.gf('django.db.models.fields.TextField')())

        db.create_unique('invapp_bagaction', ['bag_id', 'action', 'timestamp'])

    def backwards(self, orm):

        db.delete_foreign_key('invapp_bagaction', 'bag_id')

        db.delete_primary_key('invapp_bag')

        # Deleting field 'Bag.id'
        db.delete_column(u'invapp_bag', u'id')

        db.execute('DROP SEQUENCE invapp_bag_id_seq')

        # Changing field 'Bag.bagname'
        db.alter_column(u'invapp_bag', 'bagname', self.gf('django.db.models.fields.TextField')(primary_key=True))

        db.create_primary_key(u'invapp_bag', ['bagname'])

        db.delete_column(u'invapp_bagaction', 'bag_id')

        db.add_column(u'invapp_bagaction', 'bag_id', self.gf('django.db.models.fields.TextField')())

        sql = db.foreign_key_sql('invapp_bagaction', 'bag_id', 'invapp_bag', 'bagname')
        db.execute(sql)

        db.create_unique('invapp_bagaction', ['bag_id', 'action', 'timestamp'])


    models = {
        u'invapp.bag': {
            'Meta': {'object_name': 'Bag'},
            'absolute_filesystem_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bag_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bagname': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
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
            'manager': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
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
