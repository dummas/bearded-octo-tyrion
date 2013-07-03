# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Schedule'
        db.create_table('planner_schedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.Profile'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('planner', ['Schedule'])

        # Adding model 'Problem'
        db.create_table('planner_problem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('planner', ['Problem'])

        # Adding model 'Client'
        db.create_table('planner_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('planner', ['Client'])

        # Adding model 'Pet'
        db.create_table('planner_pet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Client'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('planner', ['Pet'])

        # Adding model 'Visit'
        db.create_table('planner_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('to_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Problem'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Client'])),
            ('pet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['planner.Pet'])),
            ('appointment_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='doctors', to=orm['auth.User'])),
            ('appointment_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registers', to=orm['auth.User'])),
        ))
        db.send_create_signal('planner', ['Visit'])


    def backwards(self, orm):
        # Deleting model 'Schedule'
        db.delete_table('planner_schedule')

        # Deleting model 'Problem'
        db.delete_table('planner_problem')

        # Deleting model 'Client'
        db.delete_table('planner_client')

        # Deleting model 'Pet'
        db.delete_table('planner_pet')

        # Deleting model 'Visit'
        db.delete_table('planner_visit')


    models = {
        'accounts.profile': {
            'Meta': {'object_name': 'Profile'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'planner.client': {
            'Meta': {'object_name': 'Client'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'planner.pet': {
            'Meta': {'object_name': 'Pet'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Client']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'planner.problem': {
            'Meta': {'object_name': 'Problem'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'planner.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.Profile']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'planner.visit': {
            'Meta': {'object_name': 'Visit'},
            'appointment_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registers'", 'to': "orm['auth.User']"}),
            'appointment_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'doctors'", 'to': "orm['auth.User']"}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'from_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Pet']"}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['planner.Problem']"}),
            'to_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['planner']