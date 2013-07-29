Setup for MT Analysis
=====================

Usage
----

Setup the relevant CMSSW version

    cmsrel CMSSW_5_3_2_patch4
    cd CMSSW_5_3_2_patch4/src
    cmsenv 

If you want read-only (you won't be able to commit changes without changing origin in git)

    git clone git://github.com/ttbarMET-at-IPHC/recipeMTAnalysis.git ./

If you want read-write (if you have write permissions on this repo)

    git clone git@github.com:ttbarMET-at-IPHC/recipeMTAnalysis ./
    
Launch the install
    
    source install.sh


