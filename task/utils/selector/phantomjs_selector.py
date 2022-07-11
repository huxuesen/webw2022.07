import ast
from collections import OrderedDict
from playwright.sync_api import sync_playwright
from task.utils.selector.selector import SelectorABC as FatherSelector

#js = """Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"""
class PhantomJSSelector(FatherSelector):
    def __init__(self, debug=False):
        self.debug = debug

    def get_html(self, url, headers):
        browser_args = [
            '--window-size=1300,570',
            '--window-position=000,000',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-web-security',
            '--disable-features=site-per-process',
            '--disable-setuid-sandbox',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--single-process',
            '--disable-gpu',
            '--use-gl=egl',
            '--disable-blink-features=AutomationControlled',
            '--disable-background-networking',
            '--enable-features=NetworkService,NetworkServiceInProcess',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-component-extensions-with-background-pages',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-features=Translate',
            '--disable-hang-monitor',
            '--disable-ipc-flooding-protection',
            '--disable-popup-blocking',
            '--disable-prompt-on-repost',
            '--disable-renderer-backgrounding',
            '--disable-sync',
            '--force-color-profile=srgb',
            '--metrics-recording-only',
            '--enable-automation',
            '--password-store=basic',
            '--use-mock-keychain',
            '--hide-scrollbars',
            '--mute-audio'
        ]
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, args=browser_args)
            page = browser.new_page()
            #page.add_init_script(js)1
            if headers:
                header_dict = ast.literal_eval(headers)
                if type(header_dict) != dict:
                    page.set_extra_http_headers({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.49'})
                page.set_extra_http_headers(header_dict)

            page.goto(url, timeout = 0)
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
