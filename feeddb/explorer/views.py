# VG: I suggest this usage for views.py: 
#  This is where back end (DB access & data massaging) and 
#  front end (presentation on web pages) are connected to each other. 
#  We will only keep the connecting code here. 
#  All non-trivial computations should be factored out separate modules. 

import os, re, tempfile, zipfile, csv
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.list_detail import object_detail
from django.template import RequestContext, Template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.simple import redirect_to
from django.contrib.auth import authenticate, login,logout
from django.db.models import Q
from django.utils.html import escape
from feeddb.explorer.models import *
from feeddb.feed.models import *
from feeddb.explorer.forms import *
from django.conf import settings

def portal_page(request):
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'content': 'Welcome!'  })
    return render_to_response('explorer/index.html', c, mimetype="text/html")

def bucket_index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    buckets = Bucket.objects.filter(created_by=request.user)
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'buckets': buckets})
    return render_to_response('explorer/bucket_list.html', c, mimetype="text/html")

def bucket_add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    message=None
    
    if request.method=='POST':
        bucket = Bucket(created_by=request.user)
        form = BucketModelForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            message = "successfully added the bucket."
            request.user.message_set.create(message=message)
            c = RequestContext(request, {'title': 'FeedDB Explorer',  'form':form})
            return render_to_response('explorer/bucket_detail.html', c)
        else:
            message = "failed to add the bucket."
    else:
        bucket = Bucket()
        form = BucketModelForm(instance=bucket)
    
    if message!=None:
        request.user.message_set.create(message=message)
    c = RequestContext(request, {'title': 'FeedDB Explorer',  'form':form})
    return render_to_response('explorer/bucket_add.html', c)

def bucket_delete(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    try:
        bucket = Bucket.objects.get(pk=id)
    except Bucket.DoesNotExist:
        request.user.message_set.create(message='Bucket with primary key %s does not exist.' % id)
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)
    #check if the user is the owner of the bucket. If not return error page 
    if bucket.created_by.pk != request.user.pk:
        request.user.message_set.create(message='Sorry, you are not allowed to delete a bucket owned by another user.')
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)
    bucket.delete()
    request.user.message_set.create(message='successfully deleted the bucket:%s' % bucket)
    return HttpResponseRedirect('/explorer/bucket/')

# VG-claim: Finishing this view in the 1st pass needs only  
#     a detailed implementation of the bucket_detail.html template. 
#  However, we'll later need to improve efficiency of DB lookups. 
def bucket_detail(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    message=None
    try:
        bucket = Bucket.objects.get(pk=id)
    except Bucket.DoesNotExist:
        request.user.message_set.create(message='Bucket with primary key %s does not exist.' % id)
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)

    #check if the user is the owner of the bucket. If not return error page 
    if bucket.created_by.pk != request.user.pk:
        request.user.message_set.create(message='Sorry, you are not allowed to view/edit a bucket owned by another user.')
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)
        
    if request.method=='POST':
        form = BucketModelForm(request.POST, instance=bucket)
        if form.is_valid():
            form.save()
            message = "successfully updated update the record."
        else:
            message = "failed to update the record."
    else:
        form = BucketModelForm(instance=bucket)
    
    if message!=None:
        request.user.message_set.create(message=message)
    c = RequestContext(request, {'title': 'FeedDB Explorer',  'form':form})
    return render_to_response('explorer/bucket_detail.html', c)

def bucket_download(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    message=""
    try:
        bucket = Bucket.objects.get(pk=id)
    except Bucket.DoesNotExist:
        request.user.message_set.create(message='Bucket with primary key %s does not exist.' % id)
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)

    if request.method=='POST':
        zipfile_name= request.POST['zipfile_name']
        if zipfile_name=="":
            message = 'no zip file name selected.'
            request.user.message_set.create(message=message)
            c = RequestContext(request, {'title': 'FeedDB Explorer'})
            return render_to_response('explorer/base.html', c)
        if not zipfile_name.endswith(".zip"):   
            zipfile_name +=".zip"
             
        download_choice= request.POST['download_choice']
        channel_choice = request.POST['channel_choice']
        #meta_option= request.POST['meta_option']
        quotechar_char='"'
        #delimiter= request.POST['delimiter']
        #if delimiter =="tab":
        #    delimiter_char = '\t'
        #elif delimiter =="comma":
        #    delimiter_char = ','
        #else:
        delimiter_char = ','
       
        
        #get selected fields
        field_selected = []
        for item in request.POST.items():
            if(item[1]=="on" and item[0].startswith("chk:")):
                field_selected.append(item[0])
                message += item[0]+"\n"
        if  (download_choice=="0" or  download_choice=="2") and  len(field_selected) ==0:
            message = 'no fields selected.'
            request.user.message_set.create(message=message)
            c = RequestContext(request, {'title': 'FeedDB Explorer'})
            return render_to_response('explorer/base.html', c)
        meta_selected = {}
        for field in field_selected:
            parts=field.split(":")
            if not parts[1] in meta_selected:
                meta_selected[parts[1]]=[]
            parameter=parts[1]+":"+parts[2]
            meta_selected[parts[1]].append([parts[2],request.POST[parameter]])
        
         #get selected channels
        channel_selected = []
        channel_headers=[]
        for item in request.POST.items():
            if(item[1]=="on" and item[0].startswith("channel:")):
                channel_selected.append(item[0])
                message += item[0]+"\n"
        if  (channel_choice=="1" and len(channel_selected) ==0):
            message = 'no channels selected.'
            request.user.message_set.create(message=message)
            c = RequestContext(request, {'title': 'FeedDB Explorer'})
            return render_to_response('explorer/base.html', c)
        channel_download = []
        channel_selected.sort()
        trials_download =[]
        for ch in channel_selected:
            parts=ch.split(":")
            channel_download.append([parts[1], parts[2]])
            channel_headers.append("Trial %s:Channel %s" % (parts[1], parts[2]))
            if not parts[1] in trials_download:
                trials_download.append(parts[1])
        filenames={}

        # create a temporary folder to store files
        from time import time
        tempdir = settings.EXPLORER_TEMPORARY_FOLDER+"/"+str(time()).replace('.', '')

        try:
            os.makedirs(tempdir)
        except OSError, err:
            message = 'failed to create folder for storing downloaded files.'
            request.user.message_set.create(message=message)
            c = RequestContext(request, {'title': 'FeedDB Explorer'})
            return render_to_response('explorer/base.html', c)
        
        #
        # create meta data if the user has chosen to do so
        #
        if  (download_choice=="0" or  download_choice=="2"):
            #create trials mate data file and out it into the temp zip file
            full_filename = "%s/trials.csv" % tempdir
            filenames["trials.csv"]=full_filename

            metaWriter = csv.writer(open(full_filename,"w"), delimiter=delimiter_char,  doublequote='false' , escapechar ='\\', quotechar=quotechar_char, quoting=csv.QUOTE_MINIMAL)
            
            #output trials
            #output headers
            headers=["Trial:ID"]
            for key, value in meta_selected.items():
                if not key in('Setup','EmgSetup','SonoSetup','Sensor','EmgSensor','SonoSensor','Channel','EmgChannel','SonoChannel'):
                    for v in value:
                        headers.append( v[1] )
            metaWriter.writerow(headers)
        
            objects={}
            for trial in bucket.trials.all():
                values=[trial.id]
                objects["Session"]= trial.session
                objects["Experiment"]=trial.session.experiment
                objects["Study"]=trial.session.experiment.study
                objects["Subject"]=trial.session.experiment.subject
                objects["Trial"]=trial
                for key, value in meta_selected.items():
                    if key in objects:
                        for v in value:
                            s=getattr(objects[key], v[0])
                            if hasattr(s,'split'): 
                                ss=s.split('\r\n')
                                if len(ss)>1:
                                    s=' '.join(ss)
                            
                            values.append(s) 
                            
                metaWriter.writerow(values)
        
            #output channels
            #generate channel headers
            headers=["Channel:ID"]
            for key, value in meta_selected.items():
                #generate headers meta data
                if key in('Setup','EmgSetup','Sensor','EmgSensor','SonoSetup','SonoSensor','Channel','EmgChannel','SonoChannel'):
                    for v in value:
                        headers.append( v[1] )
            
            for key, value in meta_selected.items():
                #generate headers for 2 meta data (specifically for crystal2 in sono data 
                if key in('Sensor','SonoSensor'):
                    for v in value:
                        headers.append( 'Sensor 2:%s' % v[1] )
                        
            channel_types = ['strainchannel','forcechannel','pressurechannel','kinematicschannel']        
            for trial in bucket.trials.all():
                #trial_name = trial.title.replace('.', '').replace(',', '').replace(' ', '_').strip().lower()
                #filename = "trial_%d_%s_channels.csv" % (trial.id, trial_name)
                #full_filename = "%s/trial_%d_%s_channels.csv" % (tempdir, trial.id,trial_name)
                filename = "trial_%d_channels.csv" % trial.id
                full_filename = "%s/trial_%d_channels.csv" % (tempdir, trial.id)
                filenames[filename]=full_filename

                f = open(full_filename,"w")
                metaWriter = csv.writer(f, delimiter=delimiter_char, doublequote='false', escapechar ='\\', quotechar=quotechar_char, quoting=csv.QUOTE_MINIMAL)
                metaWriter.writerow(headers)
                objects={}
                for lineup in trial.session.channellineup_set.all():
                    objects={}
                    ch=lineup.channel
                    
                    if ch == None:
                        values=["deadchannel"]
                    else:
                        objects["Channel"] = lineup.channel
                        values=[ch.id]
                        objects["Setup"]= ch.setup
                        for channel_type in channel_types:
	                        if hasattr(ch,channel_type):
	                            objects["Sensor"] = getattr(ch, channel_type).sensor
                        if hasattr(ch.setup, 'emgsetup'):
                            objects["EmgSetup"] = ch.setup.emgsetup
                        if hasattr(ch.setup, 'sonoetup'):
                            objects["SonoSetup"] = ch.setup.sonosetup
                        if hasattr(ch,'emgchannel'):
                            objects["EmgChannel"] = ch.emgchannel
                            objects["Sensor"] = ch.emgchannel.sensor
                            objects["EmgSensor"] = ch.emgchannel.sensor
                        if hasattr(ch,'sonochannel'):
                            objects["SonoChannel"] = ch.sonochannel
                            objects["Sensor"] = ch.sonochannel.crystal1
                            objects["SonoSensor"] = ch.sonochannel.crystal1
                        if hasattr(ch,'emgchannel'):
                            objects["Sensor"] = ch.emgchannel.sensor
                    
                    for key, value in meta_selected.items():
                        if key in('Setup','EmgSetup','SonoSetup','Sensor','EmgSensor','SonoSensor','Channel','EmgChannel','SonoChannel'):
                            for v in value:
                                s=''
                                if key in objects and objects[key]!=None:
                                    s=getattr(objects[key], v[0])
                                    if hasattr(s,'split'): 
		                                ss=s.split('\r\n')
		                                if len(ss)>1:
		                                    s=' '.join(ss)
                                values.append(s)                 
                           
                    #output the second crystal sensor information if it is sono channel
                    if hasattr(ch,'sonochannel'):
                        objects["Sensor"] = ch.sonochannel.crystal2
                        objects["SonoSensor"] = ch.sonochannel.crystal2
                        for key, value in meta_selected.items():
                            if key in('Sensor','SonoSensor'):
                                for v in value:
                                    s=''
                                    if key in objects:
		                                s=getattr(objects[key], v[0])
		                                if hasattr(s,'split'): 
		                                    ss=s.split('\r\n')
		                                    if len(ss)>1:
		                                        s=' '.join(ss)
                                    values.append(s)                 
                    metaWriter.writerow(values)
                                        
                f.close()
        #
        # put data files into the tmp zip
        #
        data_files = {}
        if  (download_choice=="1" or  download_choice=="2"):
            # download all trial files
            if channel_choice=="0": 
                for trial in bucket.trials.all():
                    #check if there is a data file
                    if(trial.data_file!=None and trial.data_file!=""):
                        filename = "trial_%d.dat" % trial.id
                        full_filename = "%s/%s" % (settings.MEDIA_ROOT, trial.data_file)
                        data_files[filename]=full_filename
            else:
                # download selected channels
                filename = "channels.dat"
                full_filename = "%s/channels.dat" % tempdir
                filenames[filename]=full_filename
                f = open(full_filename,"w")
                metaWriter = csv.writer(f, delimiter=delimiter_char, doublequote='false', escapechar ='\\', quotechar=quotechar_char, quoting=csv.QUOTE_MINIMAL)
                metaWriter.writerow(channel_headers)
                trial_readers={}
                total_trial_number=0
                for trial in bucket.trials.all():
                    #check if there is a data file
                    if(trial.data_file!=None and trial.data_file!="" and str(trial.id) in trials_download ):
                        full_filename = "%s/%s" % (settings.MEDIA_ROOT, trial.data_file)
                        csvfile = open(full_filename,"rU")
                        dialect = csv.Sniffer().sniff(csvfile.read(1024))
                        csvfile.seek(0)
                        reader = csv.reader(csvfile, dialect)
                        trial_readers[str(trial.id)]={"reader":reader,"hasmore":True,"file":csvfile}
                        total_trial_number += 1
                        
                rows ={}
                newrow=[]
                finished_file_number=0
                
                while finished_file_number<total_trial_number:
                    rows.clear()
                    for key in trial_readers:
                        try:
                            if trial_readers[key]["hasmore"]:
                                row = trial_readers[key]["reader"].next()
                                rows[key] = row
                        except StopIteration:
                            finished_file_number += 1
                            trial_readers[key]["hasmore"]=False
                            trial_readers[key]["file"].close()
                            
                    newrow=[]
                    for ch in channel_download:
                        if ch[0] in rows:
                            if int(ch[1]) > len(rows[ch[0]]):
                                message = "Error in channel lineup positions for trial: %s" % ch[0]
                                request.user.message_set.create(message=message)
                                c = RequestContext(request, {'title': 'FeedDB Explorer'})
                                return render_to_response('explorer/base.html', c)
                            newrow.append(rows[ch[0]][int(ch[1])-1])
                        else:
                            newrow.append('')                  
                    metaWriter.writerow(newrow)      
                f.close()
        response=send_zipfile(request, filenames,data_files, zipfile_name)
        for file, full_file in filenames.items():
            os.remove(full_file)
        os.rmdir(tempdir)
        return response
    if message!=None and message!="":
        request.user.message_set.create(message=message)
    meta_forms =[]
    meta_forms.append(StudyModelForm())
    meta_forms.append(SubjectModelForm())
    meta_forms.append(ExperimentModelForm())
    meta_forms.append(SessionModelForm())
    meta_forms.append(TrialModelForm())
    
    meta_forms.append(SetupModelForm())
    meta_forms.append(EmgSetupModelForm())
    meta_forms.append(SonoSetupModelForm())
    meta_forms.append(SensorModelForm())
    meta_forms.append(EmgSensorModelForm())
    meta_forms.append(SonoSensorModelForm())
    meta_forms.append(ChannelModelForm())
    meta_forms.append(EmgChannelModelForm())
    meta_forms.append(SonoChannelModelForm())
    
    bucket_name = bucket.title.replace(' ','_').strip().lower()
    bucket_name = "%s.zip" % bucket_name
    
    
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'file_name': bucket_name, 'bucket':bucket, 'meta_forms':meta_forms})
    return render_to_response('explorer/bucket_download.html', c)


def trial_search(request): 
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    if request.method == 'POST': 
        query = Q()
        form = SearchTrialForm(request.POST) 
        emg_tech_id = KnownTechniques.emg.id
        sono_tech_id = KnownTechniques.sono.id
        if form.is_valid():
            species = form.cleaned_data['species']
            if species!=None and species != "":
                query = query & Q(session__experiment__subject__taxon__id__exact = species)
            muscle = form.cleaned_data['muscle']
            behavior = form.cleaned_data['primary_behavior']
            if behavior!=None and behavior != "":
                query = query & Q(behavior_primary__id__exact = behavior) 
            food = form.cleaned_data['food_type']
            item_per_page = int(form.cleaned_data['item_per_page'])
            page = int(form.cleaned_data['page'])
            if food!=None and food != "":
                query = query & Q(food_type__icontains = food) 
            if muscle!=None and muscle != "":
                muscle_emg_query =  Q(session__channels__setup__technique__id__exact = emg_tech_id) & Q(session__channels__emgchannel__sensor__location_controlled__id__exact = int(muscle))
                muscle_sono_query =  Q(session__channels__setup__technique__id__exact = sono_tech_id) & (Q(session__channels__sonochannel__crystal1__location_controlled__id__exact = int(muscle)) | Q(session__channels__sonochannel__crystal2__location_controlled__id__exact = int(muscle)))
                muscle_query =  muscle_emg_query | muscle_sono_query
                query = query & muscle_query
            
            sensor = form.cleaned_data['sensor']
            if sensor!=None and sensor != "":
                #sensor_query = Q()
                #for tq in sensor:
                #    if tq!=None and tq != "":
                #sensor_query = sensor_query | Q(session__channels__setup__technique__id__exact = tq)
                query = query & Q(session__channels__setup__technique__id__exact = int(sensor))
            
            start = (page-1)*item_per_page
            end = start + item_per_page
            results= Trial.objects.filter(query).distinct().order_by('session__experiment__subject__taxon')
            total = results.count()
            total_page=total/item_per_page
            if (total - total_page*item_per_page >0):
                total_page=total_page+1
            pages=[]
            for i in range(1,total_page+1):
                pages.append(i)
            results= Trial.objects.filter(query).distinct().order_by('session__experiment__subject__taxon')[start:end]    
            item_per_page_choice = [10,30,50,100,200]        
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form, 'total': total, 'item_per_page':item_per_page, 'item_per_page_choice':item_per_page_choice, 'page': page, 'pages': pages, 'trials': results})
        return render_to_response('explorer/trial_list.html', c)
    else:
        form= SearchTrialForm()
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'form': form})
        return render_to_response('explorer/search_trial.html', c)

def trial_search_put(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    message = None
    #check if any trial selected
    trial_selected = []
    for item in request.POST.items():
        if(item[1]=="on"):
            trial_selected.append(item[0])
    if len(trial_selected) ==0:
        message = 'no trial selected.'
        request.user.message_set.create(message=message)
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no trial selected.'})
        return render_to_response('explorer/base.html', c)
    #check if new bucket selected
    bucket = None
    bucket_selected = request.POST['bucket']
    if bucket_selected ==None or bucket_selected =="":
        message = 'no bucket selected.'
        request.user.message_set.create(message=message)
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no bucket selected.'})
        return render_to_response('explorer/base.html', c)
    if request.POST['bucket']!='add new bucket':
        bucket = Bucket.objects.get(pk=bucket_selected)
    else: 
        new_bucket_name=request.POST['new_bucket_name']
        if new_bucket_name==None and new_bucket_name =="":
            c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': 'no new bucket name specified.'})
            return render_to_response('explorer/base.html', c)
        else:
            bucket = Bucket()
            bucket.created_by = request.user
            bucket.title = new_bucket_name
            bucket.save()
    #add trials to the bucket
    for trial_id in trial_selected:
        trial = Trial.objects.get(pk=trial_id)
        assocs = TrialInBucket.objects.filter(Q(trial__id__exact=trial_id) & Q(bin__id__exact=bucket.id))
        if len(assocs) ==0:
            assoc = TrialInBucket(trial=trial, bin = bucket)
            assoc.save()
    
    request.user.message_set.create(message='successfully put the selected trials to the bucket')
    return HttpResponseRedirect('/explorer/bucket/%s/' % bucket.id)

def bucket_remove_trials(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    #check if any trial selected
    trial_selected = []
    for item in request.POST.items():
        if(item[1]=="on"):
            trial_selected.append(item[0])
    if len(trial_selected) ==0:
        request.user.message_set.create(message='no trials selected')
        return HttpResponseRedirect('/explorer/bucket/%s/' % id)
    #check if bucket exists
    try:
        bucket = Bucket.objects.get(pk=id)
    except Trial.DoesNotExist:
        request.user.message_set.create(message='Bucket with primary key %(key)r does not exist.' % {'key': escape(id)})
        return HttpResponseRedirect('/explorer/bucket/%s/' % id)
    #check if the user is the owner of the bucket. If not return error page 
    if bucket.created_by.pk != request.user.pk:
        request.user.message_set.create(message='Sorry, you are not allowed to change a bucket owned by another user.')
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)
    #remove trials from the bucket
    for trial_id in trial_selected:
        trial = Trial.objects.get(pk=trial_id)
        assocs = TrialInBucket.objects.filter(Q(trial__id__exact=trial_id) & Q(bin__id__exact=bucket.id))
        for assoc in assocs:
            assoc.delete()
    request.user.message_set.create(message='successfully removed the selected trials from the bucket')
    return HttpResponseRedirect('/explorer/bucket/%s/' % id)
    
def trial_detail(request, id): 
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    try:
        trial = Trial.objects.get(pk=id)
    except Trial.DoesNotExist:
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
        return render_to_response('explorer/error.html', c)
    c = RequestContext(request, {'title': 'Trial Detail | FeedDB Explorer', 'trial': trial})
    return render_to_response('explorer/trial_detail.html', c)

def trial_remove(request, id, bucket_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    try:
        trial = Trial.objects.get(pk=id)
    except Trial.DoesNotExist:
        request.user.message_set.create(message='Trial with primary key %(key)r does not exist.' % {'key': escape(id)})
        c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
        return render_to_response('explorer/base.html', c)

    try:
        bucket = Bucket.objects.get(pk=bucket_id)
    except Bucket.DoesNotExist:
        request.user.message_set.create(message='Bucket with primary key %(key)r does not exist.' % {'key': escape(bucket_id)})
        return HttpResponseRedirect('/explorer/trial/%s/' % id)

    #check if the user is the owner of the bucket. If not return error page 
    if bucket.created_by.pk != request.user.pk:
        request.user.message_set.create(message='Sorry, you are not allowed to change a bucket owned by another user.')
        c = RequestContext(request, {'title': 'FeedDB Explorer'})
        return render_to_response('explorer/base.html', c)
            
    try:
        assoc = TrialInBucket.objects.filter(Q(trial__id__exact=id) & Q(bin__id__exact=bucket_id))
    except TrialInBucket.DoesNotExist:
        request.user.message_set.create(message='Trial: %s is not in the bucket: %s.' % (trial, bucket))
        return HttpResponseRedirect('/explorer/trial/%s/' % id)
    
    assoc.delete()
    request.user.message_set.create(message='Trial: %s has been successfully removed from the bucket: %s.' % (trial, bucket))
    return HttpResponseRedirect('/explorer/trial/%s/' % id)

def trial_add(request, id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=%s' % request.path)
    if request.method =='POST':
        try:
            trial = Trial.objects.get(pk=id)
        except Trial.DoesNotExist:
            c = RequestContext(request, {'title': 'Error | FeedDB Explorer', 'message': 'Trial with primary key %(key)r does not exist.' % {'key': escape(id)}})
            return render_to_response('explorer/error.html', c)
        #check if the user is the owner of the bucket. If not return error page 
        if bucket.created_by.pk != request.user.pk:
            request.user.message_set.create(message='Sorry, you are not allowed to change a bucket owned by another user.')
            c = RequestContext(request, {'title': 'FeedDB Explorer'})
            return render_to_response('explorer/base.html', c)
        if request.POST['bucket_id']!='add new bucket':
            bucket_id = request.POST['bucket_id']
            if bucket_id==None or bucket_id =="":
                request.user.message_set.create(message='no bucket specified')
                return HttpResponseRedirect('/explorer/trial/%s/' % id)
            try:
                bucket = Bucket.objects.get(pk=bucket_id)
            except Bukcet.DoesNotExist:
                request.user.message_set.create(message='Bucket with primary key %(key)r does not exist.' % {'key': escape(bucket_id)})
                return HttpResponseRedirect('/explorer/trial/%s/' % id)
        else: 
            new_bucket_name=request.POST['new_bucket_name']
            if new_bucket_name==None and new_bucket_name =="":
                request.user.message_set.create(message='no new bucket name specified')
                return HttpResponseRedirect('/explorer/trial/%s/' % id)
            else:
                bucket = Bucket()
                bucket.created_by = request.user
                bucket.title = new_bucket_name
                bucket.save()

        #check if bucket already contains the trial
        assocs = TrialInBucket.objects.filter(Q(trial__id__exact=id) & Q(bin__id__exact=bucket.id))
        if len(assocs) >0:
                request.user.message_set.create(message='trial already in the bucket')
                return HttpResponseRedirect('/explorer/trial/%s/' % id)
        #add trials to the bucket
        assoc = TrialInBucket(trial=trial, bin = bucket)
        assoc.save()
        request.user.message_set.create(message='Trial: %s has been successfully added to the bucket: %s.' % (trial, bucket))
        return HttpResponseRedirect('/explorer/trial/%s/' % id)

def logout_view(request):
    logout(request)
    message = 'You have logged out.'
    c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message})
    return render_to_response('explorer/index.html', c)

def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/explorer')
    message = 'Please login'
    if request.method == 'GET':
        next = '/explorer'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message, 'next':next})
        return render_to_response('explorer/login.html', c)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next = '/explorer'
                if request.POST.has_key('next'):
                    next = request.POST['next'] 
                if not next is None and next !="": 
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("/explorer/trial/search")
            else:
                message = "The account is no longer active. Please try another account." 
        else:
            message = "No matched account found. Please try again."

        next = '/explorer'
        if request.GET.has_key('next'):
            next = request.GET['next'] 
        c = RequestContext(request, {'title': 'FeedDB Explorer', 'message': message, 'next':next })
        return render_to_response('explorer/login.html', c)

def send_file(request, filename):
    """                                                                         
    Send a file through Django without loading the whole file into              
    memory at once. The FileWrapper will turn the file object into an           
    iterator for chunks of 8KB.                                                 
    """
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(filename)

    return response

def send_zipfile(request, files, data_files, zipfilename):
    """                                                                         
    Create a ZIP file on disk and transmit it in chunks of 8KB,                 
    without loading the whole file into memory. A similar approach can          
    be used for large dynamic PDF files.                                        
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    for file, filename in files.items():
        archive.write(filename, file)
    
    for file, filename in data_files.items():
        archive.write(filename, file)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Length'] = temp.tell()
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(zipfilename)
    temp.seek(0)
    return response


