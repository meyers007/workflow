#!/usr/bin/env python 

#*** DO NOT EDIT - GENERATED FROM tseries/notebooks/tseries_services.ipynb ****

import sys, os,  glob, logging, datetime, json
from  mangorest.mango import webapi
from colabexts import utils as colabexts_utils
import pandas as pd
import xmltodict
import colabexts.utils as colabexts_utils

sys.path.append("../..")

MBASE  = "/opt/data/data/workflows/"
logger = logging.getLogger( "geoapp" )

#---------------------------------------------------------------------------------    
@webapi("/wf/save_wf")
def save_wf( name, jsn, xml, **kwargs):
    name = name or "default"
    if (name.endswith(".json")):  name = name[:-5]
    if (name.endswith(".xml")):   name = name[:-4]
        
    if not os.path.exists(MBASE ):
        os.makedirs(MBASE)
    
    with open(f"{MBASE}/{name}.xml",  "w") as f:   f.write(xml.strip())
    if ( len(jsn) < 30 ):
        jsn = xmltodict.parse(xml,attr_prefix='', cdata_key='#text')
        jsn = json.dumps(jsn, indent=4)

    with open(f"{MBASE}/{name}.json", "w") as f:   f.write(jsn.strip())

    return f"Saved "    
#---------------------------------------------------------------------------------    
@webapi("/wf/get_wf")
def get_wf( name, **kwargs):
    if (name.endswith(".json")):  name = name[:-5]
    if (name.endswith(".xml")):   name = name[:-4]

    xml = open(f"{MBASE}/{name}.xml",  "r").read()
    ret = dict(json="", xml=xml)

    return ret  
#------------------------------------------------------------------------------
@webapi("/wf/delete_wf")
def delete_wf(name="", **kwargs):
    if (name.endswith(".json")):  name = name[:-5]
    if (name.endswith(".xml")):   name = name[:-4]

    logger.info(f"DELETE {name}")
    
    dst = f"{MBASE}/{name}.xml"
    if ( os.path.exists(dst) ):  os.remove(dst)

    dst = f"{MBASE}/{name}.json"
    if ( os.path.exists(dst) ):  os.remove(dst)

    return f"Deleted {dst}."
#------------------------------------------------------------------------------
@webapi("/wf/getall_wfs")
def getAllWorkflows( nrows=10000, patt='*.xml', **kwargs):
    
    files = glob.glob(f"{MBASE}{patt}")
    files.sort(key=os.path.getmtime, reverse=True)

    ret = {
        "name": "workflows",
        "columns": ["name"],
        "values": [[f[len(MBASE):]] for f in files][0:nrows]
    }
    return ret
#---------------------------------------------------------------------------------    
@webapi("/wf/run_wf")
def run_wf( name, **kwargs):
    if (name.endswith(".json")):  name = name[:-5]
    if (name.endswith(".xml")):   name = name[:-4]

    wfdef  = f"/opt/data/data/workflows/{name}.xml"
    buf=open(wfdef,"r").read()
    wf = xmltodict.parse(buf,attr_prefix='', cdata_key='#text')


    wfsh="#Execute\n"
    for c in wf['mxGraphModel']['root']['mxCell']:
        w = colabexts_utils.Map(c)
        s = w.text or ""
        wfsh += f"#Processing ID: {w.id}, Value: {w.value} => Cmd: {s}\n"
        if (not s):
            continue
        wfsh += f"{s}\n"

    open("/tmp/run.sh","w").write(wfsh)

    return f"Running /tmp/run.sh {wfsh} "
