
from south.db import db
from django.db import models
from feeddb.feed.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ForceChannel.unit'
        db.add_column('feed_forcechannel', 'unit', orm['feed.forcechannel:unit'])
        
        # Adding field 'KinematicsChannel.unit'
        db.add_column('feed_kinematicschannel', 'unit', orm['feed.kinematicschannel:unit'])
        
        # Adding field 'PressureChannel.unit'
        db.add_column('feed_pressurechannel', 'unit', orm['feed.pressurechannel:unit'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'ForceChannel.unit'
        db.delete_column('feed_forcechannel', 'unit_id')
        
        # Deleting field 'KinematicsChannel.unit'
        db.delete_column('feed_kinematicschannel', 'unit_id')
        
        # Deleting field 'PressureChannel.unit'
        db.delete_column('feed_pressurechannel', 'unit_id')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'feed.anteriorposterioraxis': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anteriorposterioraxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.behavior': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'behavior_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.channel': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channel_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Setup']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.channellineup': {
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Channel']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channellineup_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Session']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.depthaxis': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'depthaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.developmentstage': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developmentstage_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.dorsalventralaxis': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dorsalventralaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.electrodetype': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electrodetype_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.emgchannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'emg_amplification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'emg_filtering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgfiltering']"}),
            'emg_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgunit']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.EmgSensor']"})
        },
        'feed.emgelectrode': {
            'axisap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgelectrode_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'electrode_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ElectrodeType']", 'null': 'True', 'blank': 'True'}),
            'emg_amplification': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'emg_filtering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgfiltering']"}),
            'emg_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgunit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Muscle']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {}),
            'sensor': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Setup']"}),
            'side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Side']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.emgfiltering': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgfiltering_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.emgsensor': {
            'axisap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'electrode_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ElectrodeType']", 'null': 'True', 'blank': 'True'}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Muscle']"}),
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'}),
            'side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Side']"})
        },
        'feed.emgsetup': {
            'preamplifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.emgunit': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgunit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.experiment': {
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiment_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Study']"}),
            'subj_age': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '5', 'blank': 'True'}),
            'subj_devstage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DevelopmentStage']"}),
            'subj_tooth': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subj_weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '5', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Subject']"}),
            'subject_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'new Experiment - edit this'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.forcechannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.forcesensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.forcesetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.illustration': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'illustration_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Experiment']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Setup']", 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Subject']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.kinematicschannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.kinematicssensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.kinematicssetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.muscle': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'muscle_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.pressurechannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.pressuresensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.pressuresetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.restraint': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'restraint_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.sensor': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc_region': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'loc_side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Side']", 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'setup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Setup']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.session': {
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'channels': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['feed.Channel']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subj_anesthesia_sedation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subj_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subj_restraint': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Restraint']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'new Recording Session - edit this'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.setup': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setup_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'technique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Technique']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.side': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'side_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.sonochannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'crystal1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crystals1_related'", 'to': "orm['feed.SonoSensor']"}),
            'crystal2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'crystals2_related'", 'to': "orm['feed.SonoSensor']"}),
            'sono_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Sonounit']"})
        },
        'feed.sonosensor': {
            'axisap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Muscle']"}),
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'}),
            'side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Side']"})
        },
        'feed.sonosetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'}),
            'sonomicrometer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'feed.sonounit': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sonounit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.strainchannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.strainsensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.strainsetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.study': {
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approval_secured': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'study_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'funding_agency': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.studyprivate': {
            'approval': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'studyprivate_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'funding': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pi': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Study']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.subject': {
            'breed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Study']"}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Taxon']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.taxon': {
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxon_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.technique': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'technique_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.trial': {
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'behavior_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'behavior_primary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Behavior']"}),
            'behavior_secondary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'claimed_duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '4', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trial_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'food_property': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'food_size': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'food_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Session']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subj_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'subj_treatment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'new Trial - edit this'", 'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'waveform_picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'feed.unit': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'technique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Technique']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['feed']
