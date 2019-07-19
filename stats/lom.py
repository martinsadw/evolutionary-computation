import xml.etree.cElementTree as xml

lom = xml.Element("lom", attrib={
    "xmlns": "http://ltsc.ieee.org/xsd/LOM",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:schemaLocation": "http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd",
})
# lom.setAttribute("xmlns", "http://ltsc.ieee.org/xsd/LOM")
# lom.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
# lom.setAttribute("xsi:schemaLocation", "http://ltsc.ieee.org/xsd/LOM http://ltsc.ieee.org/xsd/lomv1.0/lom.xsd")

general = xml.SubElement(lom, "general")

identifier = xml.SubElement(general, "identifier")
xml.SubElement(identifier, "catalog").text = "PPAtoSCA.LAPIC.ufjf.br"
xml.SubElement(identifier, "entry").text = "0"

# title = xml.SubElement(general, "title")
# xml.SubElement(title, "string", language="pt-BR").text = "Algoritmos e Representações"

# xml.SubElement(general, "language").text = "pt-BR"

# description = xml.SubElement(general, "description")
# xml.SubElement(description, "string", language="pt-BR").text = "Este material apresenta o que é algoritmo, suas características e as formas de representação deste, como: descrição narrativa. fluxograma e pseudocódigo."

# keyword = xml.SubElement(general, "keyword")
# xml.SubElement(keyword, "string", language="pt-BR").text = "algoritmo"
# xml.SubElement(keyword, "string", language="pt-BR").text = "descrição narrativa"
# xml.SubElement(keyword, "string", language="pt-BR").text = "fluxograma"
# xml.SubElement(keyword, "string", language="pt-BR").text = "pseudocódigo"
# xml.SubElement(keyword, "string", language="pt-BR").text = "pseudolinguagem"
# xml.SubElement(keyword, "string", language="pt-BR").text = "representação"
# xml.SubElement(keyword, "string", language="pt-BR").text = "representação de algoritmos"

technical = xml.SubElement(lom, "technical")
xml.SubElement(technical, "format").text = "video/mp4"
# xml.SubElement(technical, "size").text = "185413"

educational = xml.SubElement(lom, "educational")

interactivity_type = xml.SubElement(educational, "interactivityType")
xml.SubElement(interactivity_type, "source").text = "LOMv1.0"
xml.SubElement(interactivity_type, "value").text = "mixed"

learning_resource_type = xml.SubElement(educational, "learningResourceType")
xml.SubElement(learning_resource_type, "source").text = "LOMv1.0"
xml.SubElement(learning_resource_type, "value").text = "narrative text"

learning_resource_type = xml.SubElement(educational, "learningResourceType")
xml.SubElement(learning_resource_type, "source").text = "LOMv1.0"
xml.SubElement(learning_resource_type, "value").text = "figure"

learning_resource_type = xml.SubElement(educational, "learningResourceType")
xml.SubElement(learning_resource_type, "source").text = "LOMv1.0"
xml.SubElement(learning_resource_type, "value").text = "simulation"

learning_resource_type = xml.SubElement(educational, "learningResourceType")
xml.SubElement(learning_resource_type, "source").text = "LOMv1.0"
xml.SubElement(learning_resource_type, "value").text = "diagram"

learning_resource_type = xml.SubElement(educational, "learningResourceType")
xml.SubElement(learning_resource_type, "source").text = "LOMv1.0"
xml.SubElement(learning_resource_type, "value").text = "exercise"

interactivity_level = xml.SubElement(educational, "interactivityLevel")
xml.SubElement(interactivity_level, "source").text = "LOMv1.0"
xml.SubElement(interactivity_level, "value").text = "low"

difficulty = xml.SubElement(educational, "difficulty")
xml.SubElement(difficulty, "source").text = "LOMv1.0"
xml.SubElement(difficulty, "value").text = "medium"

typical_learning_time = xml.SubElement(educational, "typicalLearningTime")
xml.SubElement(typical_learning_time, "duration").text = "PT28M18S"

# xml.SubElement(educational, "language").text = "pt-BR"

tree = xml.ElementTree(lom)
tree.write("results/lom_text.xml")
