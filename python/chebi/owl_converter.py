from typing import Dict, List, Tuple
import xml.etree.ElementTree as ET

root_element_open_text = '<root_element xmlns="http://purl.obolibrary.org/obo/chebi.owl#" ' \
                 'xml:base="http://purl.obolibrary.org/obo/chebi.owl" ' \
                 'xmlns:chebi1="http://purl.obolibrary.org/obo/chebi#3" ' \
                 'xmlns:chebi2="http://purl.obolibrary.org/obo/chebi#" ' \
                 'xmlns:chebi3="http://purl.obolibrary.org/obo/chebi#1" ' \
                 'xmlns:chebi="http://purl.obolibrary.org/obo/chebi#2" ' \
                 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" ' \
                 'xmlns:owl="http://www.w3.org/2002/07/owl#" ' \
                 'xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#" ' \
                 'xmlns:xml="http://www.w3.org/XML/1998/namespace" ' \
                 'xmlns:xsd="http://www.w3.org/2001/XMLSchema#" ' \
                 'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#" ' \
                 'xmlns:obo="http://purl.obolibrary.org/obo/"> \n'
                 # '<owl:Ontology rdf:about="http://purl.obolibrary.org/obo/chebi.owl"> ' \
                 #    '<owl:versionIRI rdf:resource="http://purl.obolibrary.org/obo/chebi/221/chebi.owl"/> ' \
                 #    '<rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">ChEBI subsumes and replaces the Chemical Ontology first</rdfs:comment> ' \
                 #    '<oboInOwl:date rdf:datatype="http://www.w3.org/2001/XMLSchema#string">27:04:2023 19:26</oboInOwl:date> ' \
                 #    '<rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">Author: ChEBI curation team</rdfs:comment> ' \
                 #    '<rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">ChEBI Release version 221</rdfs:comment> ' \
                 #    '<rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">developed by Michael Ashburner &amp; Pankaj Jaiswal.</rdfs:comment> ' \
                 #    '<oboInOwl:saved-by rdf:datatype="http://www.w3.org/2001/XMLSchema#string">chebi</oboInOwl:saved-by> ' \
                 #    '<oboInOwl:hasOBOFormatVersion rdf:datatype="http://www.w3.org/2001/XMLSchema#string">1.2</oboInOwl:hasOBOFormatVersion> ' \
                 #    '<oboInOwl:default-namespace rdf:datatype="http://www.w3.org/2001/XMLSchema#string">chebi_ontology</oboInOwl:default-namespace> ' \
                 #    '<rdfs:comment rdf:datatype="http://www.w3.org/2001/XMLSchema#string">For any queries contact chebi-help@ebi.ac.uk</rdfs:comment> ' \
                 # '</owl:Ontology>\n'
root_element_close_text = '</root_element>'
namespaces = {'chebi1': 'http://purl.obolibrary.org/obo/chebi#3',
              'chebi2': 'http://purl.obolibrary.org/obo/chebi#',
              'chebi3': 'http://purl.obolibrary.org/obo/chebi#1',
              'chebi': 'http://purl.obolibrary.org/obo/chebi#2',
              'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'owl': 'http://www.w3.org/2002/07/owl#',
              'oboInOwl': 'http://www.geneontology.org/formats/oboInOwl#',
              'xml': 'http://www.w3.org/XML/1998/namespace',
              'xsd': 'http://www.w3.org/2001/XMLSchema#',
              'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
              'obo': 'http://purl.obolibrary.org/obo/'
              }

owl_file_name = 'input/ChEBI/chebi_lite.owl'


def get_owl_block(owl: List[str], start: int) -> Tuple[int, int, str]:
    i = start + 2
    xml_string = root_element_open_text
    while True:
        xml_string += owl[i]
        if owl[i][:-1] == '    </owl:Class>':
            break
        i += 1
    xml_string += root_element_close_text

    for k, v in namespaces.items():
        ET.register_namespace(k, v)
    root = ET.fromstring(xml_string)
    entity_subclass_elements = root.findall('.//{http://www.w3.org/2000/01/rdf-schema#}subClassOf[@{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource]')
    role_subclass_elements = root.findall('.//{http://www.w3.org/2000/01/rdf-schema#}subClassOf/{http://www.w3.org/2002/07/owl#}Restriction/{http://www.w3.org/2002/07/owl#}onProperty[@{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource=\'http://purl.obolibrary.org/obo/RO_0000087\']/../..')
    for et in entity_subclass_elements:
        root[0].remove(et)
    for et in role_subclass_elements:
        param = {'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':
                    et[0][1].attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource']}
        ET.SubElement(root[0], '{http://www.w3.org/2000/01/rdf-schema#}subClassOf', attrib=param)
        root[0].remove(et)
    new_xml = ET.tostring(root, encoding='unicode', xml_declaration=False)
    new_xml = owl[start] + owl[start + 1] + '\n'.join(new_xml.splitlines()[1:-1])
    # print(new_xml)
    return start, i, new_xml


def convert_owl(drugs: Dict[str, str]) -> None:
    drug_tags = ['    <!-- http://purl.obolibrary.org/obo/CHEBI_' + x + ' -->' for x in drugs.keys()]
    file = open(owl_file_name, 'r')
    owl = file.readlines()
    # print(len(owl))
    file.close()
    new_owl = []
    i = 0
    while i < len(owl):
        if owl[i][:-1] in drug_tags:
            start, end, new_xml = get_owl_block(owl, i)
            new_owl.append(new_xml)
            # print(owl[i][46:-5], drugs[owl[i][46:-5]], start, end)
            i = end + 1
        else:
            new_owl.append(owl[i][:-1])
            i += 1
    print('\n'.join(new_owl))
    print(len(owl), len(new_owl))
