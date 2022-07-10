import ast
from collections import OrderedDict
from playwright.sync_api import sync_playwright
from task.utils.selector.selector import SelectorABC as FatherSelector

class PhantomJSSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            html = page.content()
            browser.close()
        return html

    def get_by_xpath(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, xpath_ext in selector_dict.items():
            result[key] = self.xpath_parse(html, xpath_ext)

        return result

    def get_by_css(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)

        result = OrderedDict()
        for key, css_ext in selector_dict.items():
            result[key] = self.css_parse(html, css_ext)

        return result
    
    def get_by_json(self, url, selector_dict, headers=None):
        html = self.get_html(url, headers)
        html = html.replace('({"resp', '{"resp').replace('":{}}})', '":{}}}')  # .replace后的代码解决了标普出错
        result = OrderedDict()
        for key, json_ext in selector_dict.items():
            result[key] = self.json_parse(html, json_ext)
            result[key] = result[key].replace('[', '').replace(']', '').replace('"', '') #.replace后代码为了去掉jsonpath检测方式的“[]”

        return result
