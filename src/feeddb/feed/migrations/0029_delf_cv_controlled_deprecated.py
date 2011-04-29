
from south.db import db
from django.db import models
from feeddb.feed.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting field 'ProximalDistalAxis.controlled'
        db.delete_column('feed_proximaldistalaxis', 'controlled')
        
        # Deleting field 'Unit.controlled'
        db.delete_column('feed_unit', 'controlled')
        
        # Deleting field 'Emgunit.deprecated'
        db.delete_column('feed_emgunit', 'deprecated')
        
        # Deleting field 'Technique.deprecated'
        db.delete_column('feed_technique', 'deprecated')
        
        # Deleting field 'Sonounit.controlled'
        db.delete_column('feed_sonounit', 'controlled')
        
        # Deleting field 'DevelopmentStage.controlled'
        db.delete_column('feed_developmentstage', 'controlled')
        
        # Deleting field 'AnatomicalLocation.deprecated'
        db.delete_column('feed_anatomicallocation', 'deprecated')
        
        # Deleting field 'Restraint.controlled'
        db.delete_column('feed_restraint', 'controlled')
        
        # Deleting field 'Technique.controlled'
        db.delete_column('feed_technique', 'controlled')
        
        # Deleting field 'DevelopmentStage.deprecated'
        db.delete_column('feed_developmentstage', 'deprecated')
        
        # Deleting field 'Muscle.controlled'
        db.delete_column('feed_muscle', 'controlled')
        
        # Deleting field 'DorsalVentralAxis.controlled'
        db.delete_column('feed_dorsalventralaxis', 'controlled')
        
        # Deleting field 'AnteriorPosteriorAxis.deprecated'
        db.delete_column('feed_anteriorposterioraxis', 'deprecated')
        
        # Deleting field 'ProximalDistalAxis.deprecated'
        db.delete_column('feed_proximaldistalaxis', 'deprecated')
        
        # Deleting field 'MedialLateralAxis.controlled'
        db.delete_column('feed_mediallateralaxis', 'controlled')
        
        # Deleting field 'ElectrodeType.deprecated'
        db.delete_column('feed_electrodetype', 'deprecated')
        
        # Deleting field 'Behavior.controlled'
        db.delete_column('feed_behavior', 'controlled')
        
        # Deleting field 'DorsalVentralAxis.deprecated'
        db.delete_column('feed_dorsalventralaxis', 'deprecated')
        
        # Deleting field 'Emgfiltering.controlled'
        db.delete_column('feed_emgfiltering', 'controlled')
        
        # Deleting field 'Sonounit.deprecated'
        db.delete_column('feed_sonounit', 'deprecated')
        
        # Deleting field 'DepthAxis.controlled'
        db.delete_column('feed_depthaxis', 'controlled')
        
        # Deleting field 'Behavior.deprecated'
        db.delete_column('feed_behavior', 'deprecated')
        
        # Deleting field 'Side.deprecated'
        db.delete_column('feed_side', 'deprecated')
        
        # Deleting field 'Emgunit.controlled'
        db.delete_column('feed_emgunit', 'controlled')
        
        # Deleting field 'ElectrodeType.controlled'
        db.delete_column('feed_electrodetype', 'controlled')
        
        # Deleting field 'AnteriorPosteriorAxis.controlled'
        db.delete_column('feed_anteriorposterioraxis', 'controlled')
        
        # Deleting field 'Side.controlled'
        db.delete_column('feed_side', 'controlled')
        
        # Deleting field 'Taxon.deprecated'
        db.delete_column('feed_taxon', 'deprecated')
        
        # Deleting field 'Emgfiltering.deprecated'
        db.delete_column('feed_emgfiltering', 'deprecated')
        
        # Deleting field 'DepthAxis.deprecated'
        db.delete_column('feed_depthaxis', 'deprecated')
        
        # Deleting field 'Muscle.deprecated'
        db.delete_column('feed_muscle', 'deprecated')
        
        # Deleting field 'AnatomicalLocation.controlled'
        db.delete_column('feed_anatomicallocation', 'controlled')
        
        # Deleting field 'Taxon.controlled'
        db.delete_column('feed_taxon', 'controlled')
        
        # Deleting field 'MedialLateralAxis.deprecated'
        db.delete_column('feed_mediallateralaxis', 'deprecated')
        
        # Deleting field 'Restraint.deprecated'
        db.delete_column('feed_restraint', 'deprecated')
        
        # Deleting field 'Unit.deprecated'
        db.delete_column('feed_unit', 'deprecated')
        
    
    
    def backwards(self, orm):
        
        # Adding field 'ProximalDistalAxis.controlled'
        db.add_column('feed_proximaldistalaxis', 'controlled', orm['feed.proximaldistalaxis:controlled'])
        
        # Adding field 'Unit.controlled'
        db.add_column('feed_unit', 'controlled', orm['feed.unit:controlled'])
        
        # Adding field 'Emgunit.deprecated'
        db.add_column('feed_emgunit', 'deprecated', orm['feed.emgunit:deprecated'])
        
        # Adding field 'Technique.deprecated'
        db.add_column('feed_technique', 'deprecated', orm['feed.technique:deprecated'])
        
        # Adding field 'Sonounit.controlled'
        db.add_column('feed_sonounit', 'controlled', orm['feed.sonounit:controlled'])
        
        # Adding field 'DevelopmentStage.controlled'
        db.add_column('feed_developmentstage', 'controlled', orm['feed.developmentstage:controlled'])
        
        # Adding field 'AnatomicalLocation.deprecated'
        db.add_column('feed_anatomicallocation', 'deprecated', orm['feed.anatomicallocation:deprecated'])
        
        # Adding field 'Restraint.controlled'
        db.add_column('feed_restraint', 'controlled', orm['feed.restraint:controlled'])
        
        # Adding field 'Technique.controlled'
        db.add_column('feed_technique', 'controlled', orm['feed.technique:controlled'])
        
        # Adding field 'DevelopmentStage.deprecated'
        db.add_column('feed_developmentstage', 'deprecated', orm['feed.developmentstage:deprecated'])
        
        # Adding field 'Muscle.controlled'
        db.add_column('feed_muscle', 'controlled', orm['feed.muscle:controlled'])
        
        # Adding field 'DorsalVentralAxis.controlled'
        db.add_column('feed_dorsalventralaxis', 'controlled', orm['feed.dorsalventralaxis:controlled'])
        
        # Adding field 'AnteriorPosteriorAxis.deprecated'
        db.add_column('feed_anteriorposterioraxis', 'deprecated', orm['feed.anteriorposterioraxis:deprecated'])
        
        # Adding field 'ProximalDistalAxis.deprecated'
        db.add_column('feed_proximaldistalaxis', 'deprecated', orm['feed.proximaldistalaxis:deprecated'])
        
        # Adding field 'MedialLateralAxis.controlled'
        db.add_column('feed_mediallateralaxis', 'controlled', orm['feed.mediallateralaxis:controlled'])
        
        # Adding field 'ElectrodeType.deprecated'
        db.add_column('feed_electrodetype', 'deprecated', orm['feed.electrodetype:deprecated'])
        
        # Adding field 'Behavior.controlled'
        db.add_column('feed_behavior', 'controlled', orm['feed.behavior:controlled'])
        
        # Adding field 'DorsalVentralAxis.deprecated'
        db.add_column('feed_dorsalventralaxis', 'deprecated', orm['feed.dorsalventralaxis:deprecated'])
        
        # Adding field 'Emgfiltering.controlled'
        db.add_column('feed_emgfiltering', 'controlled', orm['feed.emgfiltering:controlled'])
        
        # Adding field 'Sonounit.deprecated'
        db.add_column('feed_sonounit', 'deprecated', orm['feed.sonounit:deprecated'])
        
        # Adding field 'DepthAxis.controlled'
        db.add_column('feed_depthaxis', 'controlled', orm['feed.depthaxis:controlled'])
        
        # Adding field 'Behavior.deprecated'
        db.add_column('feed_behavior', 'deprecated', orm['feed.behavior:deprecated'])
        
        # Adding field 'Side.deprecated'
        db.add_column('feed_side', 'deprecated', orm['feed.side:deprecated'])
        
        # Adding field 'Emgunit.controlled'
        db.add_column('feed_emgunit', 'controlled', orm['feed.emgunit:controlled'])
        
        # Adding field 'ElectrodeType.controlled'
        db.add_column('feed_electrodetype', 'controlled', orm['feed.electrodetype:controlled'])
        
        # Adding field 'AnteriorPosteriorAxis.controlled'
        db.add_column('feed_anteriorposterioraxis', 'controlled', orm['feed.anteriorposterioraxis:controlled'])
        
        # Adding field 'Side.controlled'
        db.add_column('feed_side', 'controlled', orm['feed.side:controlled'])
        
        # Adding field 'Taxon.deprecated'
        db.add_column('feed_taxon', 'deprecated', orm['feed.taxon:deprecated'])
        
        # Adding field 'Emgfiltering.deprecated'
        db.add_column('feed_emgfiltering', 'deprecated', orm['feed.emgfiltering:deprecated'])
        
        # Adding field 'DepthAxis.deprecated'
        db.add_column('feed_depthaxis', 'deprecated', orm['feed.depthaxis:deprecated'])
        
        # Adding field 'Muscle.deprecated'
        db.add_column('feed_muscle', 'deprecated', orm['feed.muscle:deprecated'])
        
        # Adding field 'AnatomicalLocation.controlled'
        db.add_column('feed_anatomicallocation', 'controlled', orm['feed.anatomicallocation:controlled'])
        
        # Adding field 'Taxon.controlled'
        db.add_column('feed_taxon', 'controlled', orm['feed.taxon:controlled'])
        
        # Adding field 'MedialLateralAxis.deprecated'
        db.add_column('feed_mediallateralaxis', 'deprecated', orm['feed.mediallateralaxis:deprecated'])
        
        # Adding field 'Restraint.deprecated'
        db.add_column('feed_restraint', 'deprecated', orm['feed.restraint:deprecated'])
        
        # Adding field 'Unit.deprecated'
        db.add_column('feed_unit', 'deprecated', orm['feed.unit:deprecated'])
        
    
    
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
        'feed.anatomicallocation': {
            'category': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anatomicallocation_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.anteriorposterioraxis': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anteriorposterioraxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.behavior': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'behavior_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
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
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Channel']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'channellineup_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Session']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.depthaxis': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'depthaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.developmentstage': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'developmentstage_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.dorsalventralaxis': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dorsalventralaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.electrodetype': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'electrodetype_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
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
        'feed.emgfiltering': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgfiltering_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.emgsensor': {
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'electrode_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ElectrodeType']", 'null': 'True', 'blank': 'True'}),
            'location_controlled': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnatomicalLocation']"}),
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.emgsetup': {
            'preamplifier': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.emgunit': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgunit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.forcechannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ForceSensor']", 'null': 'True', 'blank': 'True'}),
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
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.KinematicsSensor']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.kinematicssensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.kinematicssetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.mediallateralaxis': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediallateralaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.muscle': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'muscle_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.pressurechannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.PressureSensor']", 'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']", 'null': 'True'})
        },
        'feed.pressuresensor': {
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.pressuresetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.proximaldistalaxis': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proximaldistalaxis_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.restraint': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'restraint_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.sensor': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loc_ap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_dv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_ml': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.MedialLateralAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_pd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ProximalDistalAxis']", 'null': 'True', 'blank': 'True'}),
            'loc_side': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Side']"}),
            'location_freetext': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.setup': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setup_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sampling_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'technique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Technique']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.side': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'side_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
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
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'location_controlled': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnatomicalLocation']"}),
            'sensor_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Sensor']", 'unique': 'True', 'primary_key': 'True'})
        },
        'feed.sonosetup': {
            'setup_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Setup']", 'unique': 'True', 'primary_key': 'True'}),
            'sonomicrometer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'feed.sonounit': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sonounit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.strainchannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.StrainSensor']", 'null': 'True', 'blank': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taxon_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'feed.technique': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'technique_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'waveform_picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'feed.unit': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'technique': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Technique']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['feed']
