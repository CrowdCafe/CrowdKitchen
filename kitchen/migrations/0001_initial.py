# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'App'
        db.create_table(u'kitchen_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('callback_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kitchen', ['App'])

        # Adding model 'Job'
        db.create_table(u'kitchen_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitchen.App'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(default='New job', max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.CharField')(default='CF', max_length=2, blank=True)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='NP', max_length=2)),
            ('dataunits_per_page', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('device_type', self.gf('django.db.models.fields.CharField')(default='AD', max_length=2)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('webhook_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('userinterface_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('userinterface_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'kitchen', ['Job'])

        # Adding model 'QualityControl'
        db.create_table(u'kitchen_qualitycontrol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kitchen.Job'], unique=True)),
            ('min_answers_per_dataunit', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('max_dataunits_per_worker', self.gf('django.db.models.fields.IntegerField')(default=100)),
        ))
        db.send_create_signal(u'kitchen', ['QualityControl'])

        # Adding model 'GoldQualityControl'
        db.create_table(u'kitchen_goldqualitycontrol', (
            (u'qualitycontrol_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kitchen.QualityControl'], unique=True, primary_key=True)),
            ('gold_min', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('gold_max', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('score_min', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('qualitycontrol_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'kitchen', ['GoldQualityControl'])

        # Adding model 'DataUnit'
        db.create_table(u'kitchen_dataunit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitchen.Job'])),
            ('input_data', self.gf('jsonfield.fields.JSONField')(default={})),
            ('status', self.gf('django.db.models.fields.CharField')(default='NC', max_length=2)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kitchen', ['DataUnit'])

        # Adding model 'GoldDataUnit'
        db.create_table(u'kitchen_golddataunit', (
            (u'dataunit_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['kitchen.DataUnit'], unique=True, primary_key=True)),
            ('expected_data', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'kitchen', ['GoldDataUnit'])

        # Adding model 'Answer'
        db.create_table(u'kitchen_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataunit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kitchen.DataUnit'], blank=True)),
            ('output_data', self.gf('jsonfield.fields.JSONField')(default={}, blank=True)),
            ('score', self.gf('django.db.models.fields.FloatField')(default=0.0, null=True, blank=True)),
            ('worker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'kitchen', ['Answer'])


    def backwards(self, orm):
        # Deleting model 'App'
        db.delete_table(u'kitchen_app')

        # Deleting model 'Job'
        db.delete_table(u'kitchen_job')

        # Deleting model 'QualityControl'
        db.delete_table(u'kitchen_qualitycontrol')

        # Deleting model 'GoldQualityControl'
        db.delete_table(u'kitchen_goldqualitycontrol')

        # Deleting model 'DataUnit'
        db.delete_table(u'kitchen_dataunit')

        # Deleting model 'GoldDataUnit'
        db.delete_table(u'kitchen_golddataunit')

        # Deleting model 'Answer'
        db.delete_table(u'kitchen_answer')


    models = {
        u'account.account': {
            'Meta': {'object_name': 'Account'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Creator'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'total_earnings': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'total_spendings': ('django.db.models.fields.FloatField', [], {'default': '0', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kitchen.answer': {
            'Meta': {'object_name': 'Answer'},
            'dataunit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitchen.DataUnit']", 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'output_data': ('jsonfield.fields.JSONField', [], {'default': '{}', 'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'null': 'True', 'blank': 'True'}),
            'worker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'blank': 'True'})
        },
        u'kitchen.app': {
            'Meta': {'object_name': 'App'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.Account']"}),
            'callback_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        u'kitchen.dataunit': {
            'Meta': {'object_name': 'DataUnit'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitchen.Job']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NC'", 'max_length': '2'})
        },
        u'kitchen.golddataunit': {
            'Meta': {'object_name': 'GoldDataUnit', '_ormbases': [u'kitchen.DataUnit']},
            u'dataunit_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['kitchen.DataUnit']", 'unique': 'True', 'primary_key': 'True'}),
            'expected_data': ('jsonfield.fields.JSONField', [], {'default': '{}'})
        },
        u'kitchen.goldqualitycontrol': {
            'Meta': {'object_name': 'GoldQualityControl', '_ormbases': [u'kitchen.QualityControl']},
            'gold_max': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'gold_min': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            u'qualitycontrol_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['kitchen.QualityControl']", 'unique': 'True', 'primary_key': 'True'}),
            'qualitycontrol_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'score_min': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'})
        },
        u'kitchen.job': {
            'Meta': {'object_name': 'Job'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kitchen.App']"}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'CF'", 'max_length': '2', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'dataunits_per_page': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'device_type': ('django.db.models.fields.CharField', [], {'default': "'AD'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NP'", 'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'New job'", 'max_length': '255'}),
            'userinterface_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'userinterface_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'webhook_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'kitchen.qualitycontrol': {
            'Meta': {'object_name': 'QualityControl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['kitchen.Job']", 'unique': 'True'}),
            'max_dataunits_per_worker': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'min_answers_per_dataunit': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['kitchen']