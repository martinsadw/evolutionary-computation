import os
import xml.etree.cElementTree as xml

from utils.xml_prettifier import prettify_xml


def write_lom_file(results_folder, lom_data, prettify=False):
    interactivity_type = lom_data['interactivity_type']
    interactivity_level = lom_data['interactivity_level']
    learning_resource_types = lom_data['learning_resource_types']
    difficulty = lom_data['difficulty']
    typical_learning_time = lom_data['typical_learning_time']

    num_materials = len(interactivity_type)

    for i in range(num_materials):
        str_interactivity_type = interactivity_type[i]
        str_interactivity_level = interactivity_level[i]
        str_learning_resource_types = learning_resource_types[i]
        str_difficulty = difficulty[i]
        str_typical_learning_time = typical_learning_time[i]

        lom = xml.Element('lom', attrib={
        'xmlns': 'http://ltsc.ieee.org/xsd/LOM',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd',
        })
        # lom.setAttribute('xmlns', 'http://ltsc.ieee.org/xsd/LOM')
        # lom.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        # lom.setAttribute('xsi:schemaLocation', 'http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd')

        general = xml.SubElement(lom, 'general')

        identifier = xml.SubElement(general, 'identifier')
        xml.SubElement(identifier, 'catalog').text = 'acs.ufjf.br'
        xml.SubElement(identifier, 'entry').text = str(i)

        # NOTE(andre:2019-12-18): Essas tags não são relevantes para a nossa modelagem
        ########################################################################
        # title = xml.SubElement(general, 'title')
        # xml.SubElement(title, 'string', language='pt-BR').text = 'Algoritmos e Representações'

        # xml.SubElement(general, 'language').text = 'pt-BR'

        # description = xml.SubElement(general, 'description')
        # xml.SubElement(description, 'string', language='pt-BR').text = 'Este material apresenta o que é algoritmo, suas características e as formas de representação deste, como: descrição narrativa. fluxograma e pseudocódigo.'

        # keyword = xml.SubElement(general, 'keyword')
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'algoritmo'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'descrição narrativa'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'fluxograma'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'pseudocódigo'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'pseudolinguagem'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'representação'
        # xml.SubElement(keyword, 'string', language='pt-BR').text = 'representação de algoritmos'
        ########################################################################

        technical = xml.SubElement(lom, 'technical')
        xml.SubElement(technical, 'format').text = 'video/mp4'
        # xml.SubElement(technical, 'size').text = '185413'

        educational = xml.SubElement(lom, 'educational')

        node_interactivity_type = xml.SubElement(educational, 'interactivityType')
        xml.SubElement(node_interactivity_type, 'source').text = 'LOMv1.0'
        xml.SubElement(node_interactivity_type, 'value').text = str_interactivity_type

        for str_learning_resource_type in str_learning_resource_types:
            node_learning_resource_type = xml.SubElement(educational, 'learningResourceType')
            xml.SubElement(node_learning_resource_type, 'source').text = 'LOMv1.0'
            xml.SubElement(node_learning_resource_type, 'value').text = str_learning_resource_type

        node_interactivity_level = xml.SubElement(educational, 'interactivityLevel')
        xml.SubElement(node_interactivity_level, 'source').text = 'LOMv1.0'
        xml.SubElement(node_interactivity_level, 'value').text = str_interactivity_level

        node_difficulty = xml.SubElement(educational, 'difficulty')
        xml.SubElement(node_difficulty, 'source').text = 'LOMv1.0'
        xml.SubElement(node_difficulty, 'value').text = str_difficulty

        node_typical_learning_time = xml.SubElement(educational, 'typicalLearningTime')
        xml.SubElement(node_typical_learning_time, 'duration').text = str_typical_learning_time

        xml.SubElement(educational, 'language').text = 'pt-BR'

        tree = xml.ElementTree(lom)

        lom_path = os.path.join(results_folder, '%d.xml' % i)
        tree.write(lom_path)

        if prettify:
            prettify_xml(lom_path)
