# -*- coding: utf-8 -*-
"""
A tool to read AIS AIP SUP webpage for newly published supplements
and parse them to extract temporary restriction areas as geojson
files to be shown on a map.

Created on Mon Jun 17 12:07:54 2019

Copyright (C) 2019 Lauri Peltonen
"""

import urllib.request # Load the list of supplement links and the pdf files
import lxml.html # Parse the supplement page for links
import io # Convert received pdf file (string) to byte stream
import PyPDF2 # Extract the attached xml file from the pdf
from lxml import etree as ET # Parse the attached xml file
import datetime
import schedule
import time
import json
import geojson_rewind# Enforce right-hand rule on polygons
import argparse


restriction_types = 'R'       # Only generate features for e.g. R, D types
add_pending = False
add_passed = False
add_active = True
fetch_interval = 12
update_interval = 1
out_filename = 'sup.geojson'
verbose = 2


def remove_duplicates(l):
    return list(set(l))

def only_pdfs(l):
    return [x for x in l if x.endswith('.pdf')]


def get_sup_links():
    # Read AIP supplement page
    try:
        connection = urllib.request.urlopen('https://www.ais.fi/ais/aipsup/AipSup.htm')
    except Exception as e:
        print('Error loading AIS SUP page: ', str(e))
        return []
    
    # Parse all links
    #dom =  lxml.html.fromstring(connection.read())
    dom = lxml.html.parse(connection)
    dom.getroot().make_links_absolute()
    connection.close()
    
    # Remove duplicates
    links = dom.xpath('//a/@href')
    links = remove_duplicates(links)
    links = only_pdfs(links)

    return links


def remove_matching(l1, l2):
    return set(l1).difference(l2)


def get_pdf_file(link):
    try:
        connection = urllib.request.urlopen(link)
        pdf_file = connection.read()
    except Exception as e:
        print('Could not read pdf file:', link)
        print(str(e))
        return None
    finally:
        connection.close()
    
    pdf_stream = io.BytesIO(pdf_file)
    
    return pdf_stream



# Modified from https://kevinmloeffler.com/2018/07/08/how-to-extract-pdf-file-attachments-using-python-and-pypdf2/
def getAttachments(pdf):
    global verbose
    
    """
    Retrieves the file attachments of the PDF as a dictionary of file names
    and the file data as a bytestring.
    :return: dictionary of filenames and bytestrings
    """
    reader = PyPDF2.PdfFileReader(pdf)
    catalog = reader.trailer["/Root"]
    
    if not '/Names' in catalog:
        if verbose > 1:
            print('No /Names in PDF file catalog')
        return None

    if not '/EmbeddedFiles' in catalog['/Names']:
        if verbose > 1:
            print('No /EmbeddedFiles in PDF file catalog /Names')
        return None
    
    fileNames = catalog['/Names']['/EmbeddedFiles']['/Names']
    attachments = {}
    for f in fileNames:
        if isinstance(f, str):
            name = f
            dataIndex = fileNames.index(f) + 1
            fDict = fileNames[dataIndex].getObject()
            fData = fDict['/EF']['/F'].getData()
            attachments[name] = fData
    
    if verbose > 1:
        print('Found attachments:', len(attachments))
    return attachments


def parse_sup_xml(real_root):
    global restriction_types
    global verbose
    
    output = []

    # TODO: Loop through each message:hasMember tag and parse those!
    members = real_root.xpath('.//message:hasMember', namespaces=real_root.nsmap)
    for root in members:    
        data = {'type':'Feature', 'properties':{}, 'geometry':{}}

        # ID
        nid = root.xpath('.//aixm:designator', namespaces=real_root.nsmap)
        if len(nid) > 0:
            data['id'] = nid[0].text
        else:
            data['id'] = ''

        if verbose > 1:
            print('Feature ID:', data['id'])

        # Try to find the restriction type
        ntype = root.xpath('.//aixm:type', namespaces=real_root.nsmap)
        if len(ntype) > 0:
            # Check if we want to generate this type
            if not ntype[0].text in restriction_types:
                if verbose > 1:
                    print('Discarding feature of type', ntype[0].text)
                continue
            
            data['properties']['type'] = ntype[0].text
            
            if verbose > 1:
                print('Feature type:', ntype[0].text)
        else:
            # No type defined --> pass
            # data['properties']['type'] = ''
            if verbose > 1:
                print('Feature contains no type, discarded')
            continue
        
        # Name
        name = root.xpath('.//aixm:name', namespaces=real_root.nsmap)
        if len(name) > 0:
            data['properties']['name'] = name[0].text
        else:
            data['properties']['name'] = ''
    
    
        # Try to find the validity time
        timePeriod = root.xpath('.//gml:validTime/gml:TimePeriod', namespaces=real_root.nsmap)
        if len(timePeriod) > 0:
            try:
                beginPosition = timePeriod[0].find('gml:beginPosition', real_root.nsmap).text
                endPosition = timePeriod[0].find('gml:endPosition', real_root.nsmap).text
                data['properties']['timeBegin'] = beginPosition
                data['properties']['timeEnd'] = endPosition
            except:
                data['properties']['timeBegin'] = ''
                data['properties']['timeEnd'] = ''        
    
        # Parse the area boundary
        # TODO: This is probably too simple but seems to work most of the time...
        boundary = root.xpath('.//aixm:Curve/gml:segments/gml:GeodesicString', namespaces=real_root.nsmap)
        if len(boundary) > 0:
            data['geometry']['type'] = 'Polygon'
            data['geometry']['coordinates'] = []
            data['geometry']['coordinates'].append([])
            
            points = boundary[0].findall('gml:pos', real_root.nsmap)
            for point in points:
                (lat, lon) = point.text.split()
                data['geometry']['coordinates'][0].append([float(lon), float(lat)])
        else:
            pass

        # Make sure the polygon follows right-hand rule
        data = geojson_rewind.rewind(data)

        # print(data)
        output.append(data)

    # print(output)

    return output


feature_data = []
already_parsed = []


def add_new_sups():
    global feature_data
    global already_parsed
    global verbose
    
    if verbose:
        print('Fetching new links')

    links = get_sup_links()
    new_links = remove_matching(links, already_parsed)
    
    # TODO: Parse
    for link in new_links:
        # Retrieve the PDF file
        if verbose:
            print('New:', link)
        
        pdf_stream = get_pdf_file(link)    
        if not pdf_stream:
            continue

        attachments = getAttachments(pdf_stream)
    
        # No attached XML files
        if not attachments:
            continue
    
        # Read all attached XML files (should be only one)
        for xml_name in [x for x in attachments.keys() if x.endswith('.xml')]:
            if verbose > 1:
                print('XML:', xml_name)
            
            # Parse the XML file
            root = ET.fromstring(attachments[xml_name])
            
            notam_data = parse_sup_xml(root)
            
            feature_data.extend(notam_data)
            
    #already_parsed.extend(new_links)
    already_parsed = links.copy()



def create_json_from_features():
    global feature_data
    global add_pending
    global add_passed
    global add_active
    global out_filename
    global verbose

    current_time = datetime.datetime.now()
    
    zones = []
    for feature in feature_data:
        # print(feature)
        
        try:
            # Parse timestamps
            beginTime = datetime.datetime.strptime(feature['properties']['timeBegin'], '%Y-%m-%dT%H:%M:%SZ')
            endTime = datetime.datetime.strptime(feature['properties']['timeEnd'], '%Y-%m-%dT%H:%M:%SZ')
        except:
            # print('Error in time formats')
            # print(feature['properties']['timeBegin'])
            # print(feature['properties']['timeEnd'])
            continue # No time data for this feature --> discard
        
        if current_time < beginTime:
            print('Pending: ' + feature['id'])
            if add_pending:
                zones.append(feature)
        elif current_time > endTime:
            print('Passed: ' + feature['id'])
            if add_passed:
                zones.append(feature)
        else:
            print('Active: ' + feature['id'])
            if add_active:
                zones.append(feature)
            

    geojson = {'type':'FeatureCollection','features':zones}
    
    if verbose:
        print('Writing to file:', out_filename)
        
    with open(out_filename, 'w') as file:
        file.write(json.dumps(geojson))
        
    #print(json.dumps(geojson))


# Parse command line
parser = argparse.ArgumentParser(
    description='A program to fetch AIP supplements from AIS webpage, parse them and export geojson featureset of those.', 
    epilog='Example: python ais_sup.py --file=sup.geojson')
parser.add_argument('--file', help='output file name', default='sup.geojson')
parser.add_argument('--types', default='R', help='feature types to export, e.g. RD (restricted, danger)')
parser.add_argument('--fetch', default=fetch_interval, type=int, help='fetch new sup files interval, hours')
parser.add_argument('--update', default=update_interval, type=int, help='update the geojson file interval, hours')
parser.add_argument('--no-active', action='store_false', help='do no create features for currently active regions')
parser.add_argument('--no-passed', action='store_false', help='do no create features for passed regions')
parser.add_argument('--no-pending', action='store_false', help='do no create features for pending (future) regions')
parser.add_argument('-v', '--verbose', action='count', help='verbose output, add multiple for more info', default=1)
args = parser.parse_args()

if args.fetch:
    if args.fetch <= 0:
        print('Fetch interval must be positive, defaulting to', fetch_interval)
    else:
        fetch_interval = args.fetch

if args.update:
    if args.update <= 0:
        print('Update interval must be positive, defaulting to', update_interval)
    else:
        update_interval = args.update
        
if args.file:
    out_filename = args.file
    
if args.types:
    restriction_types = args.types

verbose = args.verbose

add_active = args.no_active
add_passed = args.no_passed
add_pending = args.no_pending

try:
    #add_new_sups()
    #create_json_from_features()

    schedule.every(fetch_interval).hours.do(add_new_sups)
    schedule.every(update_interval).hours.do(create_json_from_features)

    # Run instantly the first time
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)


except KeyboardInterrupt as e:
    print("Quit, reason:", str(e))
    
