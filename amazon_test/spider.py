



def get_xpath(page,xpath,attribute = '',text = False,is_text = False):
    '''默认是通过xpath获取属性的 text为true获取文本  is_test为True是通过文本查找selector
    :param page: 浏览器对象
    :param xpath: 定位selector的xpath
    :param attribute: 获取的属性key
    :param text: 是否获取文本
    :param is_text: 是否通过文本定位selector
    :return:
    '''
    if attribute:
        if page.query_selector(xpath):
            if page.query_selector(xpath).get_attribute(attribute):
                a = data_clean(page.query_selector(xpath).get_attribute(attribute))
                return a
    elif text:
        if page.query_selector(xpath):
            if page.query_selector(xpath).text_content():
                a = data_clean(page.query_selector(xpath).text_content())
                return a
    return ''


def data_clean(str):
    #数据清洗
    str = str.replace('\n','',).strip().replace('"',"'").replace('\\','\\\\')
    return str