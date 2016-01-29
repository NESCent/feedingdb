# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import feeddb.feed.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeUnit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnatomicalLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('category', models.IntegerField(choices=[(1, 'Muscle'), (2, 'Bone')])),
            ],
            options={
                'verbose_name': 'Anatomical Location',
                'verbose_name_plural': 'Anatomical Locations',
            },
        ),
        migrations.CreateModel(
            name='AnimalApprovalType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnteriorPosteriorAxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Anterior-posterior Point',
                'verbose_name_plural': 'Anterior-posterior Axis',
            },
        ),
        migrations.CreateModel(
            name='Behavior',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BehaviorOwl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=1000)),
                ('obo_definition', models.TextField()),
                ('rdfs_comment', models.TextField()),
                ('uri', models.CharField(max_length=1500)),
                ('rdfs_is_class', models.BooleanField(default=False)),
                ('synonyms_comma_separated', models.CharField(max_length=1500, null=True)),
                ('bfo_part_of_some', models.ManyToManyField(related_name='has_parts', to='feed.BehaviorOwl')),
                ('rdfs_subClassOf_ancestors', models.ManyToManyField(related_name='has_subClass_descendants', to='feed.BehaviorOwl')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(help_text=b'Provide a short name for identifying the data contained in this Channel.', max_length=255)),
                ('rate', models.IntegerField(verbose_name=b'Recording Rate (Hz)')),
                ('notes', models.TextField(null=True, verbose_name=b'Notes', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChannelLineup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('position', models.IntegerField(help_text=b'The numeric position of the channel within this channel lineup; coincides with the column position in the data file.', verbose_name=b'Position (integer)')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name': 'Channel Position',
                'verbose_name_plural': 'Channel Lineup',
            },
        ),
        migrations.CreateModel(
            name='DepthAxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Depth Point',
                'verbose_name_plural': 'Depth Axis',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentStage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DorsalVentralAxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Dorsal-ventral Point',
                'verbose_name_plural': 'Dorsal-ventral Axis',
            },
        ),
        migrations.CreateModel(
            name='ElectrodeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Emgfiltering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'EMG Filtering',
                'verbose_name_plural': 'EMG Filterings',
            },
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=255, verbose_name=b'Experiment title')),
                ('bookkeeping', models.CharField(help_text=b'Enter any text required for lab bookkeeping concerning the Study here', max_length=255, null=True, verbose_name=b'Bookkeeping', blank=True)),
                ('start', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'Start Date')),
                ('end', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'End Date', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('subj_age', models.DecimalField(decimal_places=1, max_digits=19, blank=True, help_text=b'As a decimal; use the following field to specify age units.', null=True, verbose_name=b'Subject Age')),
                ('subj_weight', models.DecimalField(null=True, verbose_name=b'Subject Weight (kg)', max_digits=19, decimal_places=2, blank=True)),
                ('subj_tooth', models.CharField(help_text=b'Dental development and/or eruption status of the subject at the time of the experiment', max_length=255, null=True, verbose_name=b'Dental Developmental Stage', blank=True)),
                ('subject_notes', models.TextField(null=True, verbose_name=b'Subject Notes', blank=True)),
                ('impl_notes', models.TextField(null=True, verbose_name=b'Implantation Notes', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedUserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('institutional_affiliation', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Illustration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('picture', models.FileField(upload_to=b'illustrations', null=True, verbose_name=b'Picture', blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='illustration_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('experiment', models.ForeignKey(blank=True, to='feed.Experiment', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedialLateralAxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='mediallateralaxis_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Medial-lateral Point',
                'verbose_name_plural': 'Medial-lateral Axis',
            },
        ),
        migrations.CreateModel(
            name='MuscleOwl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=1000)),
                ('obo_definition', models.TextField()),
                ('rdfs_comment', models.TextField()),
                ('uri', models.CharField(max_length=1500)),
                ('rdfs_is_class', models.BooleanField(default=False)),
                ('synonyms_comma_separated', models.CharField(max_length=1500, null=True)),
                ('bfo_part_of_some', models.ManyToManyField(related_name='has_parts', to='feed.MuscleOwl')),
                ('rdfs_subClassOf_ancestors', models.ManyToManyField(related_name='has_subClass_descendants', to='feed.MuscleOwl')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProximalDistalAxis',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='proximaldistalaxis_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Proximal-distal Point',
                'verbose_name_plural': 'Proximal-distal Axis',
            },
        ),
        migrations.CreateModel(
            name='Restraint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='restraint_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(help_text=b'Provide a short name for identifying the data contained in this Sensor.', max_length=255)),
                ('notes', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=255, verbose_name=b'Session title')),
                ('bookkeeping', models.CharField(help_text=b'Enter any text required for lab bookkeeping concerning the Study here', max_length=255, null=True, verbose_name=b'Bookkeeping', blank=True)),
                ('position', models.IntegerField(help_text=b'The numeric position of this recording session among the other sessions within the current experiment.')),
                ('start', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'Start Date')),
                ('end', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'End Date', blank=True)),
                ('subj_notes', models.TextField(null=True, verbose_name=b'Subject Notes', blank=True)),
                ('subj_anesthesia_sedation', models.CharField(max_length=255, null=True, verbose_name=b'Subject Anesthesia / Sedation', blank=True)),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('technique', models.IntegerField(choices=[(1, 'EMG'), (2, 'Sono'), (3, 'Strain'), (4, 'Bite force'), (5, 'Pressure'), (6, 'Kinematics'), (7, 'Time/Event'), (8, 'Other')])),
                ('notes', models.TextField(help_text=b'Please provide detailed information on the bandpass filtering used.', null=True, verbose_name=b'Notes about all sensors and channels in this setup', blank=True)),
                ('sampling_rate', models.IntegerField(help_text=b'Recording rate is required for each sensor channel. If data are sampled at a rate different from the recording rate for individual channels, it is noted here.', null=True, verbose_name=b'Sampling Rate (Hz)', blank=True)),
            ],
            options={
                'verbose_name': 'Setup',
            },
        ),
        migrations.CreateModel(
            name='Side',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(related_name='side_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['label'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('title', models.CharField(help_text=b'Enter a short title for the Study here', max_length=255)),
                ('bookkeeping', models.CharField(help_text=b'Enter any text required for lab bookkeeping concerning the Study here', max_length=255, null=True, verbose_name=b'Bookkeeping', blank=True)),
                ('start', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', verbose_name=b'Start Date')),
                ('end', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'End Date', blank=True)),
                ('funding_agency', models.CharField(help_text=b'The agency that funded the research', max_length=255, null=True, blank=True)),
                ('description', models.TextField(help_text=b'A brief summary of the Study goals and data', verbose_name=b'Study Description')),
                ('resources', models.TextField(help_text=b'Published or other types of information relevant to interpreting the physiologic data can be cited here', null=True, verbose_name=b'External Resources', blank=True)),
                ('approval', models.CharField(help_text=b'A reference to approval documentation for Animal Care and Use or for Human Subjects, if it was secured.', max_length=255, null=True, verbose_name=b'Animal Use Approval (if applicable)', blank=True)),
                ('approval_type', models.ForeignKey(verbose_name=b'Approval Secured', to='feed.AnimalApprovalType', help_text=b'\n                                Affirmation that an institutional approval for\n                                Animal Care and Use or for Human Subjects was\n                                secured. Please read each statement very\n                                carefully. <b>Data upload can not continue\n                                without checking the appropriate\n                                affirmation.</b>\n                                ', null=True)),
                ('created_by', models.ForeignKey(related_name='study_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name_plural': 'Studies',
            },
        ),
        migrations.CreateModel(
            name='StudyPrivate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('pi', models.CharField(help_text=b'The name of the PI of the lab where the data were collected and/or of the grant that funded the research.', max_length=255, null=True, verbose_name=b'Lab PI')),
                ('notes', models.TextField(null=True, verbose_name=b'Private Notes', blank=True)),
                ('created_by', models.ForeignKey(related_name='studyprivate_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('study', models.OneToOneField(to='feed.Study')),
            ],
            options={
                'verbose_name': 'Study - Private Information',
                'verbose_name_plural': 'Study - Private Information',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('name', models.CharField(max_length=255)),
                ('breed', models.CharField(max_length=255, null=True, verbose_name=b'Sub-species, Strain, or Breed', blank=True)),
                ('sex', models.CharField(blank=True, max_length=2, null=True, help_text=b"'-----' means sex is not known.", choices=[('M', 'Male'), ('F', 'Female')])),
                ('source', models.CharField(help_text=b'E.g. wild-caught, zoo, laboratory raised, etc.', max_length=255, null=True, blank=True)),
                ('notes', models.TextField(help_text=b'Citations for, e.g., any relevant morphological data, such as muscle weights, muscle fiber angles, fiber types, CT scan images, anatomical drawings.', null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='subject_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('study', models.ForeignKey(to='feed.Study')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('genus', models.CharField(max_length=255)),
                ('species', models.CharField(max_length=255)),
                ('common_name', models.CharField(max_length=255, null=True, blank=True)),
                ('created_by', models.ForeignKey(related_name='taxon_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['genus'],
                'verbose_name_plural': 'Taxa',
            },
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=255, verbose_name=b'Trial title')),
                ('bookkeeping', models.CharField(help_text=b'Enter any text required for lab bookkeeping concerning the Study here', max_length=255, null=True, verbose_name=b'Bookkeeping', blank=True)),
                ('position', models.IntegerField(help_text=b'The numeric position of this trial among the other trials within the current recording session.')),
                ('start', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'Start Date')),
                ('end', models.DateField(help_text=b'To manually enter a date use the format yyyy-mm-dd or choose a date from the calendar', null=True, verbose_name=b'End Date', blank=True)),
                ('subj_treatment', models.TextField(null=True, verbose_name=b'Subject Treatment', blank=True)),
                ('subj_notes', models.TextField(null=True, verbose_name=b'Subject Notes', blank=True)),
                ('food_type', models.CharField(max_length=255, null=True, verbose_name=b'Food Type', blank=True)),
                ('food_size', models.CharField(max_length=255, null=True, verbose_name=b'Food Size (maximum dimension millimeters)', blank=True)),
                ('food_property', models.CharField(max_length=255, null=True, verbose_name=b'Food Property', blank=True)),
                ('is_calibration', models.BooleanField(default=False, help_text=b'Clicking Calibration means that the trial data you upload will be for a calibration file that does not contain any feeding behavior.', verbose_name=b'Calibration:')),
                ('behavior_secondary', models.CharField(max_length=255, null=True, verbose_name=b'Secondary Behavior', blank=True)),
                ('behavior_notes', models.TextField(null=True, verbose_name=b'Behavior Notes', blank=True)),
                ('data_file', models.FileField(validators=[feeddb.feed.models.validate_data_file_extension], upload_to=feeddb.feed.models.get_data_upload_to, blank=True, help_text=b'A tab-delimited file with columns corresponding to the channel lineup specified in the Recording Session.', null=True, verbose_name=b'Data File')),
                ('waveform_picture', models.FileField(help_text=b'A picture (jpeg, pdf, etc.) as a graphical overview of data in the data file.', upload_to=b'pictures', null=True, verbose_name=b'Illustration', blank=True)),
                ('behavior_primary', models.ForeignKey(verbose_name=b'Primary Behavior', blank=True, to='feed.Behavior', null=True)),
                ('behaviorowl_primary', models.ForeignKey(related_name='primary_in_trials', blank=True, to='feed.BehaviorOwl', help_text=b'You must choose a Feeding Behavior unless you have checked that this is a Calibration Trial.', null=True, verbose_name=b'Feeding Behavior')),
                ('created_by', models.ForeignKey(related_name='trial_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
                ('experiment', models.ForeignKey(to='feed.Experiment')),
                ('session', models.ForeignKey(to='feed.Session')),
                ('study', models.ForeignKey(to='feed.Study')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('label', models.CharField(max_length=255)),
                ('technique', models.IntegerField(choices=[(1, 'EMG'), (2, 'Sono'), (3, 'Strain'), (4, 'Bite force'), (5, 'Pressure'), (6, 'Kinematics'), (7, 'Time/Event'), (8, 'Other')])),
                ('created_by', models.ForeignKey(related_name='unit_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['technique', 'label'],
            },
        ),
        migrations.CreateModel(
            name='EmgChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
                ('emg_amplification', models.IntegerField(null=True, verbose_name=b'Amplification', blank=True)),
            ],
            options={
                'verbose_name': 'EMG Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='EmgSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'EMG Electrode',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='EmgSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
                ('preamplifier', models.CharField(help_text=b'The make and model of the (pre-)amplifier.', max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'EMG Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='EventChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
                ('unit', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Time/Event Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='EventSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Time/Event Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='ForceChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Bite Force Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='ForceSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
                ('location_text', models.CharField(max_length=255, null=True, verbose_name=b'Location')),
            ],
            options={
                'verbose_name': 'Bite Force Sensor',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='ForceSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Bite Force Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='KinematicsChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Kinematics Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='KinematicsSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
                ('anatomical_location_text', models.CharField(max_length=255, null=True, verbose_name=b'Anatomical Location')),
            ],
            options={
                'verbose_name': 'Kinematics Marker',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='KinematicsSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Kinematics Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='OtherChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Other Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='OtherSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
                ('location_text', models.CharField(max_length=255, null=True, verbose_name=b'Location')),
            ],
            options={
                'verbose_name': 'Other Sensor',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='OtherSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Other Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='PressureChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Pressure Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='PressureSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
                ('location_text', models.CharField(max_length=255, null=True, verbose_name=b'Location')),
            ],
            options={
                'verbose_name': 'Pressure Sensor',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='PressureSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Pressure Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='SonoChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Sono Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='SonoSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
            ],
            options={
                'verbose_name': 'Sono Crystal',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='SonoSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
                ('sonomicrometer', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Sono Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.CreateModel(
            name='StrainChannel',
            fields=[
                ('channel_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Channel')),
            ],
            options={
                'verbose_name': 'Strain Channel',
            },
            bases=('feed.channel',),
        ),
        migrations.CreateModel(
            name='StrainSensor',
            fields=[
                ('sensor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Sensor')),
                ('anatomical_location_text', models.CharField(max_length=255, null=True, verbose_name=b'Anatomical Location')),
                ('gage_type', models.IntegerField(blank=True, null=True, verbose_name=b'Gage Type', choices=[(1, b'Delta rosette'), (2, b'Rectangular rosette'), (3, b'Single element'), (4, b'Parallel (multiple single elements)'), (5, b'Biaxial'), (6, b'Other (describe in notes)')])),
            ],
            options={
                'verbose_name': 'Strain Sensor',
            },
            bases=('feed.sensor',),
        ),
        migrations.CreateModel(
            name='StrainSetup',
            fields=[
                ('setup_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='feed.Setup')),
            ],
            options={
                'verbose_name': 'Strain Setup',
            },
            bases=('feed.setup',),
        ),
        migrations.AddField(
            model_name='subject',
            name='taxon',
            field=models.ForeignKey(to='feed.Taxon'),
        ),
        migrations.AddField(
            model_name='setup',
            name='created_by',
            field=models.ForeignKey(related_name='setup_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='setup',
            name='experiment',
            field=models.ForeignKey(to='feed.Experiment'),
        ),
        migrations.AddField(
            model_name='setup',
            name='study',
            field=models.ForeignKey(to='feed.Study'),
        ),
        migrations.AddField(
            model_name='session',
            name='channels',
            field=models.ManyToManyField(to='feed.Channel', through='feed.ChannelLineup'),
        ),
        migrations.AddField(
            model_name='session',
            name='created_by',
            field=models.ForeignKey(related_name='session_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='experiment',
            field=models.ForeignKey(to='feed.Experiment'),
        ),
        migrations.AddField(
            model_name='session',
            name='study',
            field=models.ForeignKey(to='feed.Study'),
        ),
        migrations.AddField(
            model_name='session',
            name='subj_restraint',
            field=models.ForeignKey(verbose_name=b'Subject Restraint', to='feed.Restraint'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='created_by',
            field=models.ForeignKey(related_name='sensor_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='loc_ap',
            field=models.ForeignKey(verbose_name=b'AP', blank=True, to='feed.AnteriorPosteriorAxis', null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='loc_dv',
            field=models.ForeignKey(verbose_name=b'DV', blank=True, to='feed.DorsalVentralAxis', null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='loc_ml',
            field=models.ForeignKey(verbose_name=b'ML', blank=True, to='feed.MedialLateralAxis', null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='loc_pd',
            field=models.ForeignKey(verbose_name=b'PD', blank=True, to='feed.ProximalDistalAxis', null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='loc_side',
            field=models.ForeignKey(verbose_name=b'Side', to='feed.Side', null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='setup',
            field=models.ForeignKey(to='feed.Setup'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='study',
            field=models.ForeignKey(to='feed.Study', null=True),
        ),
        migrations.AddField(
            model_name='illustration',
            name='setup',
            field=models.ForeignKey(blank=True, to='feed.Setup', null=True),
        ),
        migrations.AddField(
            model_name='illustration',
            name='subject',
            field=models.ForeignKey(blank=True, to='feed.Subject', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='created_by',
            field=models.ForeignKey(related_name='experiment_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='study',
            field=models.ForeignKey(to='feed.Study'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='subj_ageunit',
            field=models.ForeignKey(verbose_name=b'Age Units', blank=True, to='feed.AgeUnit', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='subj_devstage',
            field=models.ForeignKey(verbose_name=b'Subject Developmental Stage', to='feed.DevelopmentStage'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='subject',
            field=models.ForeignKey(to='feed.Subject'),
        ),
        migrations.AddField(
            model_name='emgfiltering',
            name='created_by',
            field=models.ForeignKey(related_name='emgfiltering_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='electrodetype',
            name='created_by',
            field=models.ForeignKey(related_name='electrodetype_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='dorsalventralaxis',
            name='created_by',
            field=models.ForeignKey(related_name='dorsalventralaxis_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='developmentstage',
            name='created_by',
            field=models.ForeignKey(related_name='developmentstage_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='depthaxis',
            name='created_by',
            field=models.ForeignKey(related_name='depthaxis_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='channellineup',
            name='channel',
            field=models.ForeignKey(blank=True, to='feed.Channel', null=True),
        ),
        migrations.AddField(
            model_name='channellineup',
            name='created_by',
            field=models.ForeignKey(related_name='channellineup_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='channellineup',
            name='session',
            field=models.ForeignKey(to='feed.Session'),
        ),
        migrations.AddField(
            model_name='channel',
            name='created_by',
            field=models.ForeignKey(related_name='channel_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='channel',
            name='setup',
            field=models.ForeignKey(to='feed.Setup'),
        ),
        migrations.AddField(
            model_name='channel',
            name='study',
            field=models.ForeignKey(to='feed.Study', null=True),
        ),
        migrations.AddField(
            model_name='behavior',
            name='created_by',
            field=models.ForeignKey(related_name='behavior_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='behavior',
            name='ontology_term',
            field=models.ForeignKey(related_name='+', to='feed.BehaviorOwl', null=True),
        ),
        migrations.AddField(
            model_name='anteriorposterioraxis',
            name='created_by',
            field=models.ForeignKey(related_name='anteriorposterioraxis_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='animalapprovaltype',
            name='created_by',
            field=models.ForeignKey(related_name='animalapprovaltype_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='anatomicallocation',
            name='created_by',
            field=models.ForeignKey(related_name='anatomicallocation_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='anatomicallocation',
            name='ontology_term',
            field=models.ForeignKey(related_name='+', to='feed.MuscleOwl', null=True),
        ),
        migrations.AddField(
            model_name='ageunit',
            name='created_by',
            field=models.ForeignKey(related_name='ageunit_related', blank=True, editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='strainchannel',
            name='sensor',
            field=models.ForeignKey(to='feed.StrainSensor'),
        ),
        migrations.AddField(
            model_name='strainchannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'Strain Units', to='feed.Unit', null=True),
        ),
        migrations.AddField(
            model_name='sonosensor',
            name='axisdepth',
            field=models.ForeignKey(verbose_name=b'Crystal Depth', blank=True, to='feed.DepthAxis', null=True),
        ),
        migrations.AddField(
            model_name='sonosensor',
            name='location_controlled',
            field=models.ForeignKey(verbose_name=b'Muscle', to='feed.AnatomicalLocation', null=True),
        ),
        migrations.AddField(
            model_name='sonosensor',
            name='muscle',
            field=models.ForeignKey(verbose_name=b'Muscle', to='feed.MuscleOwl', null=True),
        ),
        migrations.AddField(
            model_name='sonochannel',
            name='crystal1',
            field=models.ForeignKey(related_name='crystals1_related', to='feed.SonoSensor'),
        ),
        migrations.AddField(
            model_name='sonochannel',
            name='crystal2',
            field=models.ForeignKey(related_name='crystals2_related', to='feed.SonoSensor'),
        ),
        migrations.AddField(
            model_name='sonochannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'Sono Units', to='feed.Unit'),
        ),
        migrations.AddField(
            model_name='pressurechannel',
            name='sensor',
            field=models.ForeignKey(to='feed.PressureSensor'),
        ),
        migrations.AddField(
            model_name='pressurechannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'Pressure Units', to='feed.Unit', null=True),
        ),
        migrations.AddField(
            model_name='otherchannel',
            name='sensor',
            field=models.ForeignKey(verbose_name=b'Sensor', to='feed.OtherSensor', null=True),
        ),
        migrations.AddField(
            model_name='kinematicschannel',
            name='sensor',
            field=models.ForeignKey(verbose_name=b'Marker', to='feed.KinematicsSensor'),
        ),
        migrations.AddField(
            model_name='kinematicschannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'Kinematics Units', to='feed.Unit', null=True),
        ),
        migrations.AddField(
            model_name='forcechannel',
            name='sensor',
            field=models.ForeignKey(to='feed.ForceSensor'),
        ),
        migrations.AddField(
            model_name='forcechannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'Bite Force Units', to='feed.Unit', null=True),
        ),
        migrations.AddField(
            model_name='emgsensor',
            name='axisdepth',
            field=models.ForeignKey(verbose_name=b'Electrode Depth', blank=True, to='feed.DepthAxis', null=True),
        ),
        migrations.AddField(
            model_name='emgsensor',
            name='electrode_type',
            field=models.ForeignKey(verbose_name=b'Electrode Type', blank=True, to='feed.ElectrodeType', null=True),
        ),
        migrations.AddField(
            model_name='emgsensor',
            name='location_controlled',
            field=models.ForeignKey(verbose_name=b'Muscle', to='feed.AnatomicalLocation', null=True),
        ),
        migrations.AddField(
            model_name='emgsensor',
            name='muscle',
            field=models.ForeignKey(verbose_name=b'Muscle', to='feed.MuscleOwl', null=True),
        ),
        migrations.AddField(
            model_name='emgchannel',
            name='emg_filtering',
            field=models.ForeignKey(verbose_name=b'EMG Filtering', to='feed.Emgfiltering'),
        ),
        migrations.AddField(
            model_name='emgchannel',
            name='sensor',
            field=models.ForeignKey(to='feed.EmgSensor'),
        ),
        migrations.AddField(
            model_name='emgchannel',
            name='unit',
            field=models.ForeignKey(verbose_name=b'EMG Units [from models.py]', to='feed.Unit'),
        ),
    ]
