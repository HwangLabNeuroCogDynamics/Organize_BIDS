import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where
    
    allowed template fields - follow python string module: 
    
    item: index within category 
    subject: participant id 
    seqitem: run number during scanning
    subindex: sub index within group
    """
    
    t1w = create_key('sub-{subject}/anat/sub-{subject}_T1w')
    task_MB2 = create_key('sub-{subject}/func/sub-{subject}_task-MB2_run-{item:03d}_bold')
    task_MB3 = create_key('sub-{subject}/func/sub-{subject}_task-MB3_run-{item:03d}_bold')
    task_MB3_pe1 = create_key('sub-{subject}/func/sub-{subject}_task-MB3pe1_run-{item:03d}_bold')
    task_MB3_pe0 = create_key('sub-{subject}/func/sub-{subject}_task-MB3pe0_run-{item:03d}_bold')
    fm_pe0 = create_key('sub-{subject}/fmap/sub-{subject}_dir-pe0_run-{item:03d}_epi')
    fm_pe1 = create_key('sub-{subject}/fmap/sub-{subject}_dir-pe1_run-{item:03d}_epi')
    #retinotopy = create_key('func/sub-{subject}_task-Retinotopy_run-{item:03d}_bold')
    #retinotopy_sbref = create_key('func/sub-{subject}_task-Retinotopy_run-{item:03d}_sbref')

    #pilot_t1w = create_key('anat/sub-{subject}_T1w')
    #pilot_retinotopy = create_key('func/sub-{subject}_task-Retinotopy_run-{item:03d}_bold')
    #pilot_retinotopy_sbref = create_key('func/sub-{subject}_task-Retinotopy_run-{item:03d}_sbref')

    info = {t1w: [], task_MB2: [], task_MB3: [], fm_pe0: [], fm_pe1:[], task_MB3_pe1:[], task_MB3_pe0:[] }

    for idx, seq in enumerate(seqinfo):
        '''
        seq contains the following fields
        * total_files_till_now
        * example_dcm_file
        * series_number
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        '''

        x,y,z,n_vol,protocol,dcm_dir, TR, TE, image_type, series, total = (seq[6], seq[7], seq[8], seq[9], seq[12], seq[3], seq[10], seq[11], seq[19], seq[18], seq[0] )
        #x,y,z,n_vol,protocol,dcm_dir, TR, TE, image_type, series, total = (seq[6], seq[7], seq[8], seq[9], seq[12], seq[3], seq[10], seq[11], seq[19], seq[18], seq[0] )

        # t1_mprage --> T1w
        if (TE == 2.968):
            info[t1w] = [seq[2]]
        
        # epi --> task    
        # if (n_vol == 94) and (z == 40):
        #     info[task].append({'item': seq[2]})


        if (series == 'fMRI MB3 SS w HOS' ) and (TR == 1.8) : #a hack for 7002, where forgot to switch sequence
            info[task_MB3_pe1].append({'item': seq[2]})
        
        if (series == 'fMRI HOS pepolar=0' ) and (TR == 1.8) : #a hack for 7002, where forgot to switch sequence
            info[task_MB3_pe0].append({'item': seq[2]})        
        
        # if (z == 12000 ) and (TR == 1.8) : #a hack for 7002, where forgot to switch sequence
        #     info[task_MB2].append({'item': seq[2]})    

        if (series == 'fMRI MB3 pepolar=0' ) and (TR == 1.8) : #a hack for 7002, where forgot to switch sequence
            info[fm_pe0].append({'item': seq[2]})
        
        if (series == 'fMRI MB3 pepolar=1' ) and (TR == 1.8) : #a hack for 7002, where forgot to switch sequence
            info[fm_pe1].append({'item': seq[2]})     


        #if (protocol == 'mb_bold_mb2_2p5mm_AP_Retinotopy') and (n_vol == 241) and ('NORM' in seq[19]):
        #    info[pilot_retinotopy].append({'item': seq[2]})
        
        #if (protocol == 'mb_bold_mb2_2p5mm_AP_Retinotopy') and (series == 'mb_bold_mb2_2p5mm_AP_Retinotopy_SBRef') and ('NORM' in seq[19]):
        #    info[pilot_retinotopy_sbref].append({'item': seq[2]})

        #if (protocol == 'mb_bold_mb2_2p5mm_AP_Retinotopy') and (n_vol == 241) and ('NORM' in seq[19]):
        #    info[pilot_retinotopy].append({'item': seq[2]})
        
        #if (protocol == 'mb_bold_mb2_2p5mm_AP_Retinotopy') and (series == 'mb_bold_mb2_2p5mm_AP_Retinotopy_SBRef') and ('NORM' in seq[19]):
        #    info[pilot_retinotopy_sbref].append({'item': seq[2]})
    

    return info