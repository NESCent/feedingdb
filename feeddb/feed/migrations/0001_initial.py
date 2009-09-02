
from south.db import db
from django.db import models
from feeddb.feed.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Session'
        db.create_table('feed_session', (
            ('id', orm['feed.Session:id']),
            ('created_by', orm['feed.Session:created_by']),
            ('created_at', orm['feed.Session:created_at']),
            ('updated_at', orm['feed.Session:updated_at']),
            ('experiment', orm['feed.Session:experiment']),
            ('accession', orm['feed.Session:accession']),
            ('start', orm['feed.Session:start']),
            ('end', orm['feed.Session:end']),
            ('position', orm['feed.Session:position']),
            ('bookkeeping', orm['feed.Session:bookkeeping']),
            ('subj_notes', orm['feed.Session:subj_notes']),
            ('subj_restraint', orm['feed.Session:subj_restraint']),
            ('subj_anesthesia_sedation', orm['feed.Session:subj_anesthesia_sedation']),
        ))
        db.send_create_signal('feed', ['Session'])
        
        # Adding model 'Emgunit'
        db.create_table('feed_emgunit', (
            ('id', orm['feed.Emgunit:id']),
            ('created_by', orm['feed.Emgunit:created_by']),
            ('created_at', orm['feed.Emgunit:created_at']),
            ('updated_at', orm['feed.Emgunit:updated_at']),
            ('label', orm['feed.Emgunit:label']),
            ('controlled', orm['feed.Emgunit:controlled']),
            ('deprecated', orm['feed.Emgunit:deprecated']),
        ))
        db.send_create_signal('feed', ['Emgunit'])
        
        # Adding model 'Channel'
        db.create_table('feed_channel', (
            ('id', orm['feed.Channel:id']),
            ('created_by', orm['feed.Channel:created_by']),
            ('created_at', orm['feed.Channel:created_at']),
            ('updated_at', orm['feed.Channel:updated_at']),
            ('setup', orm['feed.Channel:setup']),
            ('name', orm['feed.Channel:name']),
            ('rate', orm['feed.Channel:rate']),
            ('notes', orm['feed.Channel:notes']),
        ))
        db.send_create_signal('feed', ['Channel'])
        
        # Adding model 'Trial'
        db.create_table('feed_trial', (
            ('id', orm['feed.Trial:id']),
            ('created_by', orm['feed.Trial:created_by']),
            ('created_at', orm['feed.Trial:created_at']),
            ('updated_at', orm['feed.Trial:updated_at']),
            ('session', orm['feed.Trial:session']),
            ('accession', orm['feed.Trial:accession']),
            ('position', orm['feed.Trial:position']),
            ('start', orm['feed.Trial:start']),
            ('end', orm['feed.Trial:end']),
            ('claimed_duration', orm['feed.Trial:claimed_duration']),
            ('bookkeeping', orm['feed.Trial:bookkeeping']),
            ('subj_treatment', orm['feed.Trial:subj_treatment']),
            ('subj_notes', orm['feed.Trial:subj_notes']),
            ('behavior_primary', orm['feed.Trial:behavior_primary']),
            ('behavior_secondary', orm['feed.Trial:behavior_secondary']),
            ('behavior_notes', orm['feed.Trial:behavior_notes']),
            ('food_type', orm['feed.Trial:food_type']),
            ('food_size', orm['feed.Trial:food_size']),
            ('food_property', orm['feed.Trial:food_property']),
            ('waveform_picture', orm['feed.Trial:waveform_picture']),
        ))
        db.send_create_signal('feed', ['Trial'])
        
        # Adding model 'SonoChannel'
        db.create_table('feed_sonochannel', (
            ('channel_ptr', orm['feed.SonoChannel:channel_ptr']),
            ('sono_unit', orm['feed.SonoChannel:sono_unit']),
            ('crystal1', orm['feed.SonoChannel:crystal1']),
            ('crystal2', orm['feed.SonoChannel:crystal2']),
        ))
        db.send_create_signal('feed', ['SonoChannel'])
        
        # Adding model 'EmgSetup'
        db.create_table('feed_emgsetup', (
            ('setup_ptr', orm['feed.EmgSetup:setup_ptr']),
            ('preamplifier', orm['feed.EmgSetup:preamplifier']),
        ))
        db.send_create_signal('feed', ['EmgSetup'])
        
        # Adding model 'Sonounit'
        db.create_table('feed_sonounit', (
            ('id', orm['feed.Sonounit:id']),
            ('created_by', orm['feed.Sonounit:created_by']),
            ('created_at', orm['feed.Sonounit:created_at']),
            ('updated_at', orm['feed.Sonounit:updated_at']),
            ('label', orm['feed.Sonounit:label']),
            ('controlled', orm['feed.Sonounit:controlled']),
            ('deprecated', orm['feed.Sonounit:deprecated']),
        ))
        db.send_create_signal('feed', ['Sonounit'])
        
        # Adding model 'ElectrodeType'
        db.create_table('feed_electrodetype', (
            ('id', orm['feed.ElectrodeType:id']),
            ('created_by', orm['feed.ElectrodeType:created_by']),
            ('created_at', orm['feed.ElectrodeType:created_at']),
            ('updated_at', orm['feed.ElectrodeType:updated_at']),
            ('label', orm['feed.ElectrodeType:label']),
            ('controlled', orm['feed.ElectrodeType:controlled']),
            ('deprecated', orm['feed.ElectrodeType:deprecated']),
        ))
        db.send_create_signal('feed', ['ElectrodeType'])
        
        # Adding model 'Study'
        db.create_table('feed_study', (
            ('id', orm['feed.Study:id']),
            ('created_by', orm['feed.Study:created_by']),
            ('created_at', orm['feed.Study:created_at']),
            ('updated_at', orm['feed.Study:updated_at']),
            ('accession', orm['feed.Study:accession']),
            ('name', orm['feed.Study:name']),
            ('bookkeeping', orm['feed.Study:bookkeeping']),
            ('start', orm['feed.Study:start']),
            ('end', orm['feed.Study:end']),
            ('funding_agency', orm['feed.Study:funding_agency']),
            ('approval_secured', orm['feed.Study:approval_secured']),
            ('description', orm['feed.Study:description']),
        ))
        db.send_create_signal('feed', ['Study'])
        
        # Adding model 'Muscle'
        db.create_table('feed_muscle', (
            ('id', orm['feed.Muscle:id']),
            ('created_by', orm['feed.Muscle:created_by']),
            ('created_at', orm['feed.Muscle:created_at']),
            ('updated_at', orm['feed.Muscle:updated_at']),
            ('label', orm['feed.Muscle:label']),
            ('controlled', orm['feed.Muscle:controlled']),
            ('deprecated', orm['feed.Muscle:deprecated']),
        ))
        db.send_create_signal('feed', ['Muscle'])
        
        # Adding model 'Behavior'
        db.create_table('feed_behavior', (
            ('id', orm['feed.Behavior:id']),
            ('created_by', orm['feed.Behavior:created_by']),
            ('created_at', orm['feed.Behavior:created_at']),
            ('updated_at', orm['feed.Behavior:updated_at']),
            ('label', orm['feed.Behavior:label']),
            ('controlled', orm['feed.Behavior:controlled']),
            ('deprecated', orm['feed.Behavior:deprecated']),
        ))
        db.send_create_signal('feed', ['Behavior'])
        
        # Adding model 'EmgSensor'
        db.create_table('feed_emgsensor', (
            ('sensor_ptr', orm['feed.EmgSensor:sensor_ptr']),
            ('muscle', orm['feed.EmgSensor:muscle']),
            ('side', orm['feed.EmgSensor:side']),
            ('axisdepth', orm['feed.EmgSensor:axisdepth']),
            ('axisap', orm['feed.EmgSensor:axisap']),
            ('axisdv', orm['feed.EmgSensor:axisdv']),
            ('electrode_type', orm['feed.EmgSensor:electrode_type']),
        ))
        db.send_create_signal('feed', ['EmgSensor'])
        
        # Adding model 'ChannelLineup'
        db.create_table('feed_channellineup', (
            ('id', orm['feed.ChannelLineup:id']),
            ('created_by', orm['feed.ChannelLineup:created_by']),
            ('created_at', orm['feed.ChannelLineup:created_at']),
            ('updated_at', orm['feed.ChannelLineup:updated_at']),
            ('session', orm['feed.ChannelLineup:session']),
            ('position', orm['feed.ChannelLineup:position']),
            ('channel', orm['feed.ChannelLineup:channel']),
        ))
        db.send_create_signal('feed', ['ChannelLineup'])
        
        # Adding model 'EmgChannel'
        db.create_table('feed_emgchannel', (
            ('channel_ptr', orm['feed.EmgChannel:channel_ptr']),
            ('sensor', orm['feed.EmgChannel:sensor']),
            ('emg_unit', orm['feed.EmgChannel:emg_unit']),
            ('emg_filtering', orm['feed.EmgChannel:emg_filtering']),
        ))
        db.send_create_signal('feed', ['EmgChannel'])
        
        # Adding model 'DevelopmentStage'
        db.create_table('feed_developmentstage', (
            ('id', orm['feed.DevelopmentStage:id']),
            ('created_by', orm['feed.DevelopmentStage:created_by']),
            ('created_at', orm['feed.DevelopmentStage:created_at']),
            ('updated_at', orm['feed.DevelopmentStage:updated_at']),
            ('label', orm['feed.DevelopmentStage:label']),
            ('controlled', orm['feed.DevelopmentStage:controlled']),
            ('deprecated', orm['feed.DevelopmentStage:deprecated']),
        ))
        db.send_create_signal('feed', ['DevelopmentStage'])
        
        # Adding model 'SonoSetup'
        db.create_table('feed_sonosetup', (
            ('setup_ptr', orm['feed.SonoSetup:setup_ptr']),
            ('sonomicrometer', orm['feed.SonoSetup:sonomicrometer']),
        ))
        db.send_create_signal('feed', ['SonoSetup'])
        
        # Adding model 'EmgElectrode'
        db.create_table('feed_emgelectrode', (
            ('id', orm['feed.EmgElectrode:id']),
            ('created_by', orm['feed.EmgElectrode:created_by']),
            ('created_at', orm['feed.EmgElectrode:created_at']),
            ('updated_at', orm['feed.EmgElectrode:updated_at']),
            ('setup', orm['feed.EmgElectrode:setup']),
            ('name', orm['feed.EmgElectrode:name']),
            ('notes', orm['feed.EmgElectrode:notes']),
            ('muscle', orm['feed.EmgElectrode:muscle']),
            ('side', orm['feed.EmgElectrode:side']),
            ('axisdepth', orm['feed.EmgElectrode:axisdepth']),
            ('axisap', orm['feed.EmgElectrode:axisap']),
            ('axisdv', orm['feed.EmgElectrode:axisdv']),
            ('electrode_type', orm['feed.EmgElectrode:electrode_type']),
            ('rate', orm['feed.EmgElectrode:rate']),
            ('emg_unit', orm['feed.EmgElectrode:emg_unit']),
            ('emg_filtering', orm['feed.EmgElectrode:emg_filtering']),
        ))
        db.send_create_signal('feed', ['EmgElectrode'])
        
        # Adding model 'Experiment'
        db.create_table('feed_experiment', (
            ('id', orm['feed.Experiment:id']),
            ('created_by', orm['feed.Experiment:created_by']),
            ('created_at', orm['feed.Experiment:created_at']),
            ('updated_at', orm['feed.Experiment:updated_at']),
            ('study', orm['feed.Experiment:study']),
            ('subject', orm['feed.Experiment:subject']),
            ('accession', orm['feed.Experiment:accession']),
            ('start', orm['feed.Experiment:start']),
            ('end', orm['feed.Experiment:end']),
            ('bookkeeping', orm['feed.Experiment:bookkeeping']),
            ('description', orm['feed.Experiment:description']),
            ('subj_devstage', orm['feed.Experiment:subj_devstage']),
            ('subj_age', orm['feed.Experiment:subj_age']),
            ('subj_weight', orm['feed.Experiment:subj_weight']),
            ('subj_tooth', orm['feed.Experiment:subj_tooth']),
            ('subject_notes', orm['feed.Experiment:subject_notes']),
            ('impl_notes', orm['feed.Experiment:impl_notes']),
        ))
        db.send_create_signal('feed', ['Experiment'])
        
        # Adding model 'Side'
        db.create_table('feed_side', (
            ('id', orm['feed.Side:id']),
            ('created_by', orm['feed.Side:created_by']),
            ('created_at', orm['feed.Side:created_at']),
            ('updated_at', orm['feed.Side:updated_at']),
            ('label', orm['feed.Side:label']),
            ('controlled', orm['feed.Side:controlled']),
            ('deprecated', orm['feed.Side:deprecated']),
        ))
        db.send_create_signal('feed', ['Side'])
        
        # Adding model 'Restraint'
        db.create_table('feed_restraint', (
            ('id', orm['feed.Restraint:id']),
            ('created_by', orm['feed.Restraint:created_by']),
            ('created_at', orm['feed.Restraint:created_at']),
            ('updated_at', orm['feed.Restraint:updated_at']),
            ('label', orm['feed.Restraint:label']),
            ('controlled', orm['feed.Restraint:controlled']),
            ('deprecated', orm['feed.Restraint:deprecated']),
        ))
        db.send_create_signal('feed', ['Restraint'])
        
        # Adding model 'Subject'
        db.create_table('feed_subject', (
            ('id', orm['feed.Subject:id']),
            ('created_by', orm['feed.Subject:created_by']),
            ('created_at', orm['feed.Subject:created_at']),
            ('updated_at', orm['feed.Subject:updated_at']),
            ('study', orm['feed.Subject:study']),
            ('taxon', orm['feed.Subject:taxon']),
            ('name', orm['feed.Subject:name']),
            ('breed', orm['feed.Subject:breed']),
            ('sex', orm['feed.Subject:sex']),
            ('source', orm['feed.Subject:source']),
            ('notes', orm['feed.Subject:notes']),
        ))
        db.send_create_signal('feed', ['Subject'])
        
        # Adding model 'SonoSensor'
        db.create_table('feed_sonosensor', (
            ('sensor_ptr', orm['feed.SonoSensor:sensor_ptr']),
            ('muscle', orm['feed.SonoSensor:muscle']),
            ('side', orm['feed.SonoSensor:side']),
            ('axisdepth', orm['feed.SonoSensor:axisdepth']),
            ('axisap', orm['feed.SonoSensor:axisap']),
            ('axisdv', orm['feed.SonoSensor:axisdv']),
        ))
        db.send_create_signal('feed', ['SonoSensor'])
        
        # Adding model 'AnteriorPosteriorAxis'
        db.create_table('feed_anteriorposterioraxis', (
            ('id', orm['feed.AnteriorPosteriorAxis:id']),
            ('created_by', orm['feed.AnteriorPosteriorAxis:created_by']),
            ('created_at', orm['feed.AnteriorPosteriorAxis:created_at']),
            ('updated_at', orm['feed.AnteriorPosteriorAxis:updated_at']),
            ('label', orm['feed.AnteriorPosteriorAxis:label']),
            ('controlled', orm['feed.AnteriorPosteriorAxis:controlled']),
            ('deprecated', orm['feed.AnteriorPosteriorAxis:deprecated']),
        ))
        db.send_create_signal('feed', ['AnteriorPosteriorAxis'])
        
        # Adding model 'Setup'
        db.create_table('feed_setup', (
            ('id', orm['feed.Setup:id']),
            ('created_by', orm['feed.Setup:created_by']),
            ('created_at', orm['feed.Setup:created_at']),
            ('updated_at', orm['feed.Setup:updated_at']),
            ('experiment', orm['feed.Setup:experiment']),
            ('technique', orm['feed.Setup:technique']),
            ('notes', orm['feed.Setup:notes']),
        ))
        db.send_create_signal('feed', ['Setup'])
        
        # Adding model 'Taxon'
        db.create_table('feed_taxon', (
            ('id', orm['feed.Taxon:id']),
            ('created_by', orm['feed.Taxon:created_by']),
            ('created_at', orm['feed.Taxon:created_at']),
            ('updated_at', orm['feed.Taxon:updated_at']),
            ('label', orm['feed.Taxon:label']),
            ('controlled', orm['feed.Taxon:controlled']),
            ('deprecated', orm['feed.Taxon:deprecated']),
            ('genus', orm['feed.Taxon:genus']),
            ('species', orm['feed.Taxon:species']),
            ('common_name', orm['feed.Taxon:common_name']),
        ))
        db.send_create_signal('feed', ['Taxon'])
        
        # Adding model 'DepthAxis'
        db.create_table('feed_depthaxis', (
            ('id', orm['feed.DepthAxis:id']),
            ('created_by', orm['feed.DepthAxis:created_by']),
            ('created_at', orm['feed.DepthAxis:created_at']),
            ('updated_at', orm['feed.DepthAxis:updated_at']),
            ('label', orm['feed.DepthAxis:label']),
            ('controlled', orm['feed.DepthAxis:controlled']),
            ('deprecated', orm['feed.DepthAxis:deprecated']),
        ))
        db.send_create_signal('feed', ['DepthAxis'])
        
        # Adding model 'Illustration'
        db.create_table('feed_illustration', (
            ('id', orm['feed.Illustration:id']),
            ('created_by', orm['feed.Illustration:created_by']),
            ('created_at', orm['feed.Illustration:created_at']),
            ('updated_at', orm['feed.Illustration:updated_at']),
            ('picture', orm['feed.Illustration:picture']),
            ('notes', orm['feed.Illustration:notes']),
            ('subject', orm['feed.Illustration:subject']),
            ('setup', orm['feed.Illustration:setup']),
            ('experiment', orm['feed.Illustration:experiment']),
        ))
        db.send_create_signal('feed', ['Illustration'])
        
        # Adding model 'Sensor'
        db.create_table('feed_sensor', (
            ('id', orm['feed.Sensor:id']),
            ('created_by', orm['feed.Sensor:created_by']),
            ('created_at', orm['feed.Sensor:created_at']),
            ('updated_at', orm['feed.Sensor:updated_at']),
            ('setup', orm['feed.Sensor:setup']),
            ('name', orm['feed.Sensor:name']),
            ('notes', orm['feed.Sensor:notes']),
        ))
        db.send_create_signal('feed', ['Sensor'])
        
        # Adding model 'Emgfiltering'
        db.create_table('feed_emgfiltering', (
            ('id', orm['feed.Emgfiltering:id']),
            ('created_by', orm['feed.Emgfiltering:created_by']),
            ('created_at', orm['feed.Emgfiltering:created_at']),
            ('updated_at', orm['feed.Emgfiltering:updated_at']),
            ('label', orm['feed.Emgfiltering:label']),
            ('controlled', orm['feed.Emgfiltering:controlled']),
            ('deprecated', orm['feed.Emgfiltering:deprecated']),
        ))
        db.send_create_signal('feed', ['Emgfiltering'])
        
        # Adding model 'DorsalVentralAxis'
        db.create_table('feed_dorsalventralaxis', (
            ('id', orm['feed.DorsalVentralAxis:id']),
            ('created_by', orm['feed.DorsalVentralAxis:created_by']),
            ('created_at', orm['feed.DorsalVentralAxis:created_at']),
            ('updated_at', orm['feed.DorsalVentralAxis:updated_at']),
            ('label', orm['feed.DorsalVentralAxis:label']),
            ('controlled', orm['feed.DorsalVentralAxis:controlled']),
            ('deprecated', orm['feed.DorsalVentralAxis:deprecated']),
        ))
        db.send_create_signal('feed', ['DorsalVentralAxis'])
        
        # Adding model 'StudyPrivate'
        db.create_table('feed_studyprivate', (
            ('id', orm['feed.StudyPrivate:id']),
            ('created_by', orm['feed.StudyPrivate:created_by']),
            ('created_at', orm['feed.StudyPrivate:created_at']),
            ('updated_at', orm['feed.StudyPrivate:updated_at']),
            ('study', orm['feed.StudyPrivate:study']),
            ('pi', orm['feed.StudyPrivate:pi']),
            ('organization', orm['feed.StudyPrivate:organization']),
            ('lab', orm['feed.StudyPrivate:lab']),
            ('funding', orm['feed.StudyPrivate:funding']),
            ('approval', orm['feed.StudyPrivate:approval']),
            ('notes', orm['feed.StudyPrivate:notes']),
        ))
        db.send_create_signal('feed', ['StudyPrivate'])
        
        # Adding model 'Technique'
        db.create_table('feed_technique', (
            ('id', orm['feed.Technique:id']),
            ('created_by', orm['feed.Technique:created_by']),
            ('created_at', orm['feed.Technique:created_at']),
            ('updated_at', orm['feed.Technique:updated_at']),
            ('label', orm['feed.Technique:label']),
            ('controlled', orm['feed.Technique:controlled']),
            ('deprecated', orm['feed.Technique:deprecated']),
        ))
        db.send_create_signal('feed', ['Technique'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Session'
        db.delete_table('feed_session')
        
        # Deleting model 'Emgunit'
        db.delete_table('feed_emgunit')
        
        # Deleting model 'Channel'
        db.delete_table('feed_channel')
        
        # Deleting model 'Trial'
        db.delete_table('feed_trial')
        
        # Deleting model 'SonoChannel'
        db.delete_table('feed_sonochannel')
        
        # Deleting model 'EmgSetup'
        db.delete_table('feed_emgsetup')
        
        # Deleting model 'Sonounit'
        db.delete_table('feed_sonounit')
        
        # Deleting model 'ElectrodeType'
        db.delete_table('feed_electrodetype')
        
        # Deleting model 'Study'
        db.delete_table('feed_study')
        
        # Deleting model 'Muscle'
        db.delete_table('feed_muscle')
        
        # Deleting model 'Behavior'
        db.delete_table('feed_behavior')
        
        # Deleting model 'EmgSensor'
        db.delete_table('feed_emgsensor')
        
        # Deleting model 'ChannelLineup'
        db.delete_table('feed_channellineup')
        
        # Deleting model 'EmgChannel'
        db.delete_table('feed_emgchannel')
        
        # Deleting model 'DevelopmentStage'
        db.delete_table('feed_developmentstage')
        
        # Deleting model 'SonoSetup'
        db.delete_table('feed_sonosetup')
        
        # Deleting model 'EmgElectrode'
        db.delete_table('feed_emgelectrode')
        
        # Deleting model 'Experiment'
        db.delete_table('feed_experiment')
        
        # Deleting model 'Side'
        db.delete_table('feed_side')
        
        # Deleting model 'Restraint'
        db.delete_table('feed_restraint')
        
        # Deleting model 'Subject'
        db.delete_table('feed_subject')
        
        # Deleting model 'SonoSensor'
        db.delete_table('feed_sonosensor')
        
        # Deleting model 'AnteriorPosteriorAxis'
        db.delete_table('feed_anteriorposterioraxis')
        
        # Deleting model 'Setup'
        db.delete_table('feed_setup')
        
        # Deleting model 'Taxon'
        db.delete_table('feed_taxon')
        
        # Deleting model 'DepthAxis'
        db.delete_table('feed_depthaxis')
        
        # Deleting model 'Illustration'
        db.delete_table('feed_illustration')
        
        # Deleting model 'Sensor'
        db.delete_table('feed_sensor')
        
        # Deleting model 'Emgfiltering'
        db.delete_table('feed_emgfiltering')
        
        # Deleting model 'DorsalVentralAxis'
        db.delete_table('feed_dorsalventralaxis')
        
        # Deleting model 'StudyPrivate'
        db.delete_table('feed_studyprivate')
        
        # Deleting model 'Technique'
        db.delete_table('feed_technique')
        
    
    
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
            'emg_filtering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgfiltering']"}),
            'emg_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgunit']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.EmgSensor']"})
        },
        'feed.emgelectrode': {
            'axisap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.AnteriorPosteriorAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdepth': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DepthAxis']", 'null': 'True', 'blank': 'True'}),
            'axisdv': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.DorsalVentralAxis']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emgelectrode_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'electrode_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.ElectrodeType']", 'null': 'True', 'blank': 'True'}),
            'emg_filtering': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgfiltering']"}),
            'emg_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Emgunit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muscle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Muscle']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {}),
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
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
        'feed.muscle': {
            'controlled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'muscle_related'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'deprecated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'updated_at': ('django.db.models.fields.DateTimeField', [], {}),
            'waveform_picture': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['feed']
