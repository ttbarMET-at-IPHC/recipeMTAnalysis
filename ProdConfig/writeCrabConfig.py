#! /usr/bin/env python
import sys
import os

def Execute():
    print "===================================================================="
    print " Writing crab config for " + sys.argv[1]
    print "===================================================================="

    print " Writing 'crab_"+sys.argv[1]+".cfg' file ..."

    output = file('crab_'+sys.argv[1]+'.cfg','w')
    output.write('[CRAB]\n')
    output.write('jobtype    = cmssw\n')
    output.write('use_server = 0\n')
    output.write('scheduler  = remoteGlidein\n')
    output.write('\n')

    output.write('[CMSSW]\n')

    if sys.argv[1]=='MCbkg':
        output.write('pset = MCbkg_cfg.py\n')
        output.write('total_number_of_events = -1\n')
        output.write('events_per_job         = 10000\n')
    if sys.argv[1]=='data':
        output.write('pset = data_cfg.py\n')
        output.write('split_by_lumi = 1\n')
        output.write('lumi_mask = Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.txt\n')
        output.write('total_number_of_lumis  = -1\n')
        output.write('lumis_per_job         = 30\n')

    output.write('\n')
    output.write('output_file            = SUSYPAT.root\n')
    output.write('\n')

    output.write('[USER]\n')
    output.write('eMail = alexandre.aubin@cern.ch\n')
    output.write('check_user_remote_dir =0\n')
    output.write('thresholdLevel = 98\n')
    output.write('copy_data = 1\n')
    output.write('publish_data = 1\n')
    output.write('publish_data_name = tauVetoValidationCharlie\n')
    output.write('dbs_url_for_publication = https://cmsdbsprod.cern.ch:'
                 + '8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet\n')
    output.write('srm_version = srmv2\n')
    output.write('storage_element = T2_FR_IPHC\n')
    output.write('use_central_bossDB = 0\n')
    output.write('use_boss_rt = 1\n')
    output.write('\n')

    output.write('[GRID]\n')
    output.write('lcg_version = 2\n')
    output.write('rb  = CERN\n')
    output.write('proxy_server = myproxy.cern.ch \n')
    output.write('virtual_organization = cms\n')
    output.write('retry_count = 6\n')
    output.write('lcg_catalog_type = lfc\n')
    output.write('lfc_host = lfc-cms-test.cern.ch\n')
    output.write('lfc_home = /grid/cms\n')
    output.write('\n')
    output.close()

# Check number of arguments
if len(sys.argv)<2:
    print "Error : wrong number of arguments"
    print "  > Syntax : python writeCrabConfig.py [MCbkg|data]"
else:
    Execute()



