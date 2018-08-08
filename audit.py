
# coding: utf-8

# In[ ]:


#Here we take a sample of the original dataset, which is a XML OSM file.

import xml.etree.cElementTree as ET 

OSM_FILE = "newyork.osm"  
SAMPLE_FILE = "sample_ny.osm"

k = 40

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'w') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element).encode('utf-8'))

    output.write('</osm>')


# In[ ]:


import xml.etree.cElementTree as ET 
newyork = 'sample_ny.osm'

def get_root(fname):

    tree = ET.parse(fname)
    return tree.getroot()


get_root(newyork)


# In[ ]:


#We will audit some criteria of the dataset and clean them: street names, house numbers and zip codes.

from collections import defaultdict

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Avenue", "Boulevard", "Commons", "Court", "Drive", "Lane", "Parkway", 
                         "Place", "Road", "Square", "Street", "Trail"]

mapping = {'Ave'  : 'Avenue',
           'AVE.'  : 'Avenue',
           'Blvd' : 'Boulevard',
           'Dr'   : 'Drive',
           'Ln'   : 'Lane', 
           'Pkwy' : 'Parkway',
           'Rd'   : 'Road',
           'Rd.'   : 'Road',
           'St'   : 'Street',
           'st'   : 'Street',
           'street' :"Street",
           'Ct'   : "Court",
           'Cir'  : "Circle",
           'Cr'   : "Court",
           'ave'  : 'Avenue',
           'Hwg'  : 'Highway',
           'Hwy'  : 'Highway',
           'Sq'   : "Square",
           'Tpke' : 'Turnpike'
            }

#We audit the street names by grouping them in different types.

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

#We add all the street names to their corresponding street types.

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


# In[ ]:

#Here we can see the different street types we have.

ny_street_types = audit(newyork)
pprint.pprint(dict(ny_street_types))


# In[ ]:

#We will replace the abbreviated street names with the full versions that we indicate in the file "mapping".

def update_name(name, mapping, regex):
    m = regex.search(name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            name = re.sub(regex, mapping[street_type], name)
    

    print name

for street_type, ways in ny_street_types.items():
    for name in ways:
        better_name = update_name(name, mapping, street_type_re)
        print (name, "=>", better_name)


# In[ ]:



housenr_types_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def is_housenr(elem):
    return (elem.attrib['k'] == "addr:housenumber")
 
#With the same logic, we audit the housenumbers by grouping them into different types.

def audit_housenr_type(housenr_types, housenr):
    m = housenr_types_re.search(housenr)
    if m:
        housenr_type = m.group()
        housenr_types[housenr_type].add(housenr)

#We add all the housenumbers to their corresponding types.

def audit_housenr_types(osmfile):
    osm_file = open(osmfile, "r")
    housenr_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_housenr(tag):
                    audit_housenr_type(housenr_types, tag.attrib['v'])
    return housenr_types


# In[ ]:


ny_housenr_types = audit_housenr_types(newyork)


# In[ ]:

#Here we can see the different housenumber types we have.

pprint.pprint(dict(ny_housenr_types))


# In[ ]:

#We define a new audit function to loop through every housenumber in the dataset.

def audit_housenr(osmfile):
    osm_file = open(osmfile, "r")
    housenr = []
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_housenr(tag):
                    housenr.append(tag.attrib['v'])
    return housenr
    
ny_housenr = audit_housenr(newyork)
pprint.pprint((ny_housenr))

#We clean the housenumbers to get rid of the instances where we have added words (e.g. REAR, Park Street etc.).

def cleanHouse(housenumber):
    clean = []
    for item in housenumber.split():
        for ele in item:
            if ele.isdigit():
                clean.append(item + ' ')
                break
            
            else:
                print('none')
    clean = ''.join(clean)
    print 'clean: ', clean

for housenumber in ny_housenr:
    print (cleanHouse(housenumber)) 

#Now we will clean the zipcodes.

def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

#This is the function that we will use to clean the zipcodes.
def clean_zip(zipcode):
    # remove NY from zip
    new_zip = zipcode.replace("NY","")
    # strip white spaces
    new_zip = new_zip.strip()
    # encode to remove printable characters
    new_zip = new_zip.encode("utf-8")
    return new_zip

#Create a function to group the zipcodes, since there are more places in New York that have the same zipcode.

zipcode_types_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

def audit_zipcode_type(zipcode_types, zipcode):
    m = zipcode_types_re.search(zipcode)
    if m:
        zipcode_type = m.group()
        zipcode_types[zipcode_type].add(zipcode)

def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    zipcode_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode_type(zipcode_types, tag.attrib['v'])
    
    return zipcode_types

ny_zip = audit_zip(newyork)
pprint.pprint((ny_zip))

#Clean the necessary zipcodes.

for zipcode in ny_zip:
    print (clean_zip(zipcode))


# In[ ]:




