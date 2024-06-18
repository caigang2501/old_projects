
import xml.etree.ElementTree as et


def indent(elem, level=0):
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def make_xml(library_path):
    """
    解析xml文件
    :param library_path: xml材料库文件路径
    :return: 返回重新解析排序好的xml文件
    """

    is_second = True
    # 解析材料库文件
    try:
        tree = et.parse(library_path)
        root = tree.getroot()
        all_material = root.findall('.//MATERIAL')
        directxml_node = root.find('DirectXML')
        # 判断是否有new_xml节点
        flag = directxml_node.get('flag')
        if not flag:

            directxml_node.set('flag', 'True')
            # 创建new_xml
            for m in all_material:
                # 遍历材料库
                id_text = m.find('ID').text
                # 查看材料库名称
                material = et.SubElement(directxml_node, 'MATERIAL', {'name': id_text})
                # 创建新材料库
                items = m.findall('Item')
                # 在材料库下找所有的材料
                for i in items:
                    str1 = ''
                    name = i.find('ID').text
                    # 找到材料的名字
                    item = et.SubElement(material, 'Item', {'name': name})
                    # 创建材料
                    id_label = et.SubElement(item, 'ID')
                    # 创建ID标签
                    id_label.text = name
                    # 设置ID内容

                    desc = et.SubElement(item, 'Card', {'name': 'Desc'})
                    # 创建DESC标签
                    cards = i.findall('Card')
                    # 找到所有的Card标签
                    if len(cards):
                        for card in cards:
                            if "***" in card.text:

                                is_second = False
                                continue
                            if not is_second and 'MATH' in card.text:
                                math = et.SubElement(item, 'Card', {'name': 'MATH'})
                                math.text = card.text
                            if 'MATD' in card.text:
                                matd = et.SubElement(item, 'Card', {'name': 'MATD'})
                                matd.text = card.text
                            elif 'MATH' not in card.text:
                                str1 += card.text
                                desc.text = str1
                directxml_node.remove(m)

            indent(root)
            # 写入xml文件
            tree.write(library_path, encoding="utf-8", xml_declaration=True)
            return library_path, True
        else:
            return library_path, True
    except Exception as e:
        msg = str(e)
        return msg, False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

