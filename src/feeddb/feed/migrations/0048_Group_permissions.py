
from south.db import db
from django.db import models
from feeddb.feed.models import *
from django.db.models import Q

class Migration:
    anon_opers = ["add"]
    anon_models = ["bucket", "trialinbucket"]
    
    contributors_opers = ["add"]
    contributors_models = ["study", "studyprivate", "subject", "experiment", "setup", 
                           "emgsetup", "sonosetup", "sensor", "emgsensor", "sonosensor", 
                           "channel", "emgchannel", "sonochannel", "session", "trial", 
                           "illustration", "channellineup", "bucket", "trialinbucket", 
                           "strainsetup", "strainsensor", "strainchannel", "forcesetup", 
                           "pressuresetup", "kinematicssetup", "forcesensor", "pressuresensor", 
                           "kinematicssensor", "forcechannel", "pressurechannel", "kinematicschannel", 
                            ]
    
    terminologists_opers = ["add", "change", "delete"] 
    terminologists_models = ["developmentstage", "behavior", "taxon", "side", 
                             "depthaxis", "anteriorposterioraxis", "dorsalventralaxis", 
                             "restraint", "emgfiltering", "electrodetype", "unit", 
                             "anatomicallocation", "proximaldistalaxis", "mediallateralaxis", 
                             "ageunit", 
                             ] 
    
    
    def forwards(self, orm):
        def add_permissions(group_name, group_opers, group_models):
            group = orm['auth.Group'].objects.get(name__iexact=group_name)
            
            feeddb_perms = orm['auth.Permission'].objects.filter(
                            Q(content_type__app_label__iexact = "explorer") | Q(content_type__app_label__iexact = "feed"))
            
            for mod in group_models:
                for op in group_opers:
                    try:
                        perm = feeddb_perms.get(codename__iexact = op+"_"+mod)
                        group.permissions.add(perm)
                    except Exception:
                        pass

            group.save()  #not needed?

        add_permissions('anonymous', Migration.anon_opers, Migration.anon_models)
        add_permissions('terminologists', Migration.terminologists_opers, Migration.terminologists_models)
        add_permissions('contributors', Migration.contributors_opers, Migration.contributors_models)

        
    # Even though backwards() is not a perfect inverse of forwards(), 
    # (it removes even those permission assignments that existed prior to forwards())
    # it is likely safe to run.
    # It could even be beneficial, for removing possibly-wrong permissions. 
    def backwards(self, orm):
        def clear_permissions(group_name):
            group = orm['auth.Group'].objects.get(name__iexact = group_name)
            group.permissions.clear()
            group.save()  #not needed?
        clear_permissions('anonymous')
        clear_permissions('terminologists')
        clear_permissions('contributors')
        
    
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
        'feed.ageunit': {
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ageunit_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
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
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.EmgSensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']"})
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
        'feed.experiment': {
            'accession': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'bookkeeping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'experiment_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impl_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'study': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Study']"}),
            'subj_age': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '5', 'blank': 'True'}),
            'subj_ageunit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AgeUnit']", 'null': 'True', 'blank': 'True'}),
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
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ForceSensor']"}),
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
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.KinematicsSensor']"}),
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
        'feed.pressurechannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.PressureSensor']"}),
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
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Unit']"})
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
        'feed.strainchannel': {
            'channel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['feed.Channel']", 'unique': 'True', 'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.StrainSensor']"}),
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
            'resources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trial_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'data_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_duration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
