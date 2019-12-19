import xml.etree.cElementTree as xml

# active 'exercise', 'questionnaire', 'experiment'
# reflexive 'diagram', 'figure', 'graphic', 'slide', 'table', 'narrative text', 'problems declaration'
# neutro 'simulation', 'test'
#
# sensory 'exercise', 'graphic', 'table', 'experiment', 'problems declaration'
# intuitive 'questionnaire', 'diagram', 'figure'
# neutro 'simulation', 'test', 'slide', 'narrative text'
#
# visual 'simulation', 'diagram', 'figure', 'graphic', 'table'
# verbal 'narrative text', 'reading'
# neutro 'slide'
#
# sequential 'exercise', 'simulation', 'experiment'
# global 'figure', 'graphic', 'table'
# neutro 'diagram', 'slide', 'narrative text'

def write_lom_file():
    # num_materials = len(materials)
    num_materials = 284

    for i in range(num_materials):
        str_interactivity_type = 'mixed'
        str_interactivity_level = 'low'
        str_learning_resource_types = ['narrative text', 'figure', 'simulation', 'diagram', 'exercise']
        str_difficulty = 'medium'
        str_typical_learning_time = 'PT28M18S'

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
        xml.SubElement(identifier, 'catalog').text = 'acs.getcomp.ufjf.br'
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

        interactivity_type = xml.SubElement(educational, 'interactivityType')
        xml.SubElement(interactivity_type, 'source').text = 'LOMv1.0'
        xml.SubElement(interactivity_type, 'value').text = str_interactivity_type

        for str_learning_resource_type in str_learning_resource_types:
            learning_resource_type = xml.SubElement(educational, 'learningResourceType')
            xml.SubElement(learning_resource_type, 'source').text = 'LOMv1.0'
            xml.SubElement(learning_resource_type, 'value').text = str_learning_resource_type

        interactivity_level = xml.SubElement(educational, 'interactivityLevel')
        xml.SubElement(interactivity_level, 'source').text = 'LOMv1.0'
        xml.SubElement(interactivity_level, 'value').text = str_interactivity_level

        difficulty = xml.SubElement(educational, 'difficulty')
        xml.SubElement(difficulty, 'source').text = 'LOMv1.0'
        xml.SubElement(difficulty, 'value').text = str_difficulty

        typical_learning_time = xml.SubElement(educational, 'typicalLearningTime')
        xml.SubElement(typical_learning_time, 'duration').text = str_typical_learning_time

        xml.SubElement(educational, 'language').text = 'pt-BR'

        tree = xml.ElementTree(lom)
        tree.write('results/LOMs/%d.xml'  % i)
