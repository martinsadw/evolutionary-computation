import xml.dom.minidom

indent = ' ' * 4

def prettify_xml(xml_path):
    dom = xml.dom.minidom.parse(xml_path) # or xml.dom.minidom.parseString(xml_string)
    pretty_xml_as_string = dom.toprettyxml(indent=indent)

    with open(xml_path, 'w') as file:
        file.write(pretty_xml_as_string)


if __name__ == '__main__':
    for i in range(500):
        dom = xml.dom.minidom.parse('instances/andre/500/LOM/%d.xml' % i) # or xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = dom.toprettyxml(indent=indent)

        with open('instances/andre/500/PrettyLOM/%d.xml' % i, 'w') as file:
            file.write(pretty_xml_as_string)
