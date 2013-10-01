import sublime
import sublime_plugin
import urllib.request
import urllib.parse


class NoRedirection(urllib.request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, hdrs):
        return hdrs['Location']


class PythonSharePasteCommand(sublime_plugin.WindowCommand):

    def run(self, *args):
        result = ''

        view = self.window.active_view()

        first = True
        for selection in view.sel():
            result += view.substr(sublime.Region(selection.begin(), selection.end()))
            if not first:
                result += '\n\n...\n\n'
            first = False

        opener = urllib.request.build_opener(NoRedirection)
        data = urllib.parse.urlencode({'data': result, 'lexer': 'python'})
        r = opener.open("http://paste.in.ua", data.encode('utf-8'))
        print(r)
