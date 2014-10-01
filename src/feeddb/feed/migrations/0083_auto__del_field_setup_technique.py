# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Setup.technique'
        db.delete_column(u'feed_setup', 'technique')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Setup.technique'
        raise RuntimeError("Cannot reverse this migration. 'Setup.technique' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Setup.technique'
        db.add_column(u'feed_setup', 'technique',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'feed.ageunit': {
            'Meta': {'ordering': "['label']", 'object_name': 'AgeUnit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ageunit_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.anatomicallocation': {
            'Meta': {'object_name': 'AnatomicalLocation'},
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'anatomicallocation_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ontology_term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['feed.MuscleOwl']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.animalapprovaltype': {
            'Meta': {'object_name': 'AnimalApprovalType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animalapprovaltype_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.anteriorposterioraxis': {
            'Meta': {'object_name': 'AnteriorPosteriorAxis'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'anteriorposterioraxis_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.behavior': {
            'Meta': {'ordering': "['label']", 'object_name': 'Behavior'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'behavior_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.behaviorowl': {
            'Meta': {'object_name': 'BehaviorOwl'},
            'bfo_part_of_some': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'has_parts'", 'symmetrical': 'False', 'to': u"orm['feed.BehaviorOwl']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'obo_definition': ('django.db.models.fields.TextField', [], {}),
            'rdfs_comment': ('django.db.models.fields.TextField', [], {}),
            'rdfs_is_class': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rdfs_subClassOf_ancestors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'has_subClass_descendants'", 'symmetrical': 'False', 'to': u"orm['feed.BehaviorOwl']"}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '1500'})
        },
        u'feed.channel': {
            'Meta': {'object_name': 'Channel'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'channel_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Setup']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.channellineup': {
            'Meta': {'ordering': "['position']", 'object_name': 'ChannelLineup'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Channel']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'channellineup_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Session']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.depthaxis': {
            'Meta': {'object_name': 'DepthAxis'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'depthaxis_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.developmentstage': {
            'Meta': {'ordering': "['label']", 'object_name': 'DevelopmentStage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'developmentstage_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.dorsalventralaxis': {
            'Meta': {'object_name': 'DorsalVentralAxis'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dorsalventralaxis_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.electrodetype': {
            'Meta': {'ordering': "['label']", 'object_name': 'ElectrodeType'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'electrodetype_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.emgchannel': {
            'Meta': {'object_name': 'EmgChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'emg_amplification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'emg_filtering': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Emgfiltering']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.EmgSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']"})
        },
        u'feed.emgfiltering': {
            'Meta': {'object_name': 'Emgfiltering'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'emgfiltering_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.emgsensor': {
            'Meta': {'ordering': "['id']", 'object_name': 'EmgSensor', '_ormbases': [u'feed.Sensor']},
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'electrode_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.ElectrodeType']", 'null': 'True', 'blank': 'True'}),
            'location_controlled': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.AnatomicalLocation']"}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.MuscleOwl']", 'null': 'True'}),
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.emgsetup': {
            'Meta': {'object_name': 'EmgSetup', '_ormbases': [u'feed.Setup']},
            'preamplifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.eventchannel': {
            'Meta': {'object_name': 'EventChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'feed.eventsetup': {
            'Meta': {'object_name': 'EventSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.experiment': {
            'Meta': {'object_name': 'Experiment'},
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'experiment_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Study']"}),
            'subj_age': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '5', 'blank': 'True'}),
            'subj_ageunit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.AgeUnit']", 'null': 'True', 'blank': 'True'}),
            'subj_devstage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.DevelopmentStage']"}),
            'subj_tooth': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subj_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '5', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Subject']"}),
            'subject_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.feeduserprofile': {
            'Meta': {'object_name': 'FeedUserProfile'},
            'institutional_affiliation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.forcechannel': {
            'Meta': {'object_name': 'ForceChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.ForceSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']", 'null': 'True'})
        },
        u'feed.forcesensor': {
            'Meta': {'object_name': 'ForceSensor', '_ormbases': [u'feed.Sensor']},
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.forcesetup': {
            'Meta': {'object_name': 'ForceSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.illustration': {
            'Meta': {'object_name': 'Illustration'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'illustration_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Experiment']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Setup']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Subject']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.kinematicschannel': {
            'Meta': {'object_name': 'KinematicsChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.KinematicsSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']", 'null': 'True'})
        },
        u'feed.kinematicssensor': {
            'Meta': {'object_name': 'KinematicsSensor', '_ormbases': [u'feed.Sensor']},
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.kinematicssetup': {
            'Meta': {'object_name': 'KinematicsSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.mediallateralaxis': {
            'Meta': {'object_name': 'MedialLateralAxis'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'mediallateralaxis_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.muscleowl': {
            'Meta': {'object_name': 'MuscleOwl'},
            'bfo_part_of_some': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'has_parts'", 'symmetrical': 'False', 'to': u"orm['feed.MuscleOwl']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'obo_definition': ('django.db.models.fields.TextField', [], {}),
            'rdfs_comment': ('django.db.models.fields.TextField', [], {}),
            'rdfs_is_class': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rdfs_subClassOf_ancestors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'has_subClass_descendants'", 'symmetrical': 'False', 'to': u"orm['feed.MuscleOwl']"}),
            'uri': ('django.db.models.fields.CharField', [], {'max_length': '1500'})
        },
        u'feed.pressurechannel': {
            'Meta': {'object_name': 'PressureChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.PressureSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']", 'null': 'True'})
        },
        u'feed.pressuresensor': {
            'Meta': {'object_name': 'PressureSensor', '_ormbases': [u'feed.Sensor']},
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.pressuresetup': {
            'Meta': {'object_name': 'PressureSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.proximaldistalaxis': {
            'Meta': {'object_name': 'ProximalDistalAxis'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proximaldistalaxis_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.restraint': {
            'Meta': {'ordering': "['label']", 'object_name': 'Restraint'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'restraint_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sensor_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc_ap': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_dv': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_ml': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.MedialLateralAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_pd': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.ProximalDistalAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_side': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Side']"}),
            'location_freetext': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Setup']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.session': {
            'Meta': {'ordering': "['position']", 'object_name': 'Session'},
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['feed.Channel']", 'through': u"orm['feed.ChannelLineup']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'session_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Study']"}),
            'subj_anesthesia_sedation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subj_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subj_restraint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Restraint']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.setup': {
            'Meta': {'object_name': 'Setup'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'setup_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Experiment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sampling_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.side': {
            'Meta': {'ordering': "['label']", 'object_name': 'Side'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'side_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.sonochannel': {
            'Meta': {'object_name': 'SonoChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'crystal1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crystals1_related'", 'to': u"orm['feed.SonoSensor']"}),
            'crystal2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crystals2_related'", 'to': u"orm['feed.SonoSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']"})
        },
        u'feed.sonosensor': {
            'Meta': {'object_name': 'SonoSensor', '_ormbases': [u'feed.Sensor']},
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'location_controlled': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.AnatomicalLocation']"}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.MuscleOwl']", 'null': 'True'}),
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.sonosetup': {
            'Meta': {'object_name': 'SonoSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'}),
            'sonomicrometer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'feed.strainchannel': {
            'Meta': {'object_name': 'StrainChannel', '_ormbases': [u'feed.Channel']},
            u'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.StrainSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Unit']", 'null': 'True'})
        },
        u'feed.strainsensor': {
            'Meta': {'object_name': 'StrainSensor', '_ormbases': [u'feed.Sensor']},
            u'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.strainsetup': {
            'Meta': {'object_name': 'StrainSetup', '_ormbases': [u'feed.Setup']},
            u'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'feed.study': {
            'Meta': {'ordering': "['title']", 'object_name': 'Study'},
            'approval': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approval_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.AnimalApprovalType']", 'null': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'study_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'funding': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'funding_agency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pi': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'resources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.subject': {
            'Meta': {'object_name': 'Subject'},
            'breed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subject_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Study']"}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Taxon']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.taxon': {
            'Meta': {'ordering': "['genus']", 'object_name': 'Taxon'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taxon_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'feed.trial': {
            'Meta': {'object_name': 'Trial'},
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'behavior_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'behavior_primary': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Behavior']", 'null': 'True'}),
            'behavior_secondary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'behaviorowl_primary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_in_trials'", 'null': 'True', 'to': u"orm['feed.BehaviorOwl']"}),
            'behaviorowl_secondary': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondary_in_trials'", 'null': 'True', 'to': u"orm['feed.BehaviorOwl']"}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'trial_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Experiment']"}),
            'food_property': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'food_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'food_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['feed.Study']"}),
            'subj_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subj_treatment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'waveform_picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'feed.unit': {
            'Meta': {'ordering': "['technique', 'label']", 'object_name': 'Unit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'unit_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'technique': ('django.db.models.fields.IntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['feed']