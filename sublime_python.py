import os
import sublime
import sublime_plugin
import urllib.request
import urllib.parse


class NoRedirection(urllib.request.HTTPRedirectHandler):

    def http_error_302(self, req, fp, code, msg, hdrs):
        return hdrs['Location']


supportedLexer = {
      'actionscript': 'as',
      'python': 'python',
      'c++': 'cpp',
      'c#': 'csharp',
      'java': 'java',
      'html': 'html',
      'lua': 'lua',
      'javascript': 'js',
      'xml': 'xml',
      'haskell': 'haskell'
}


class PythonSharePasteCommand(sublime_plugin.WindowCommand):

    def run(self, *args):
        result = ''

        view = self.window.active_view()

        first = True
        for selection in view.sel():
            region = view.substr(sublime.Region(selection.begin(), selection.end()))
            if not region.strip():
                continue
            result += region
            if not first:
                result += '\n\n...\n\n'
            first = False

        syntax = os.path.basename(view.settings().get('syntax'))
        fn, ext = os.path.splitext(syntax)
        lexer = supportedLexer.get(fn.lower(), '')

        opener = urllib.request.build_opener(NoRedirection)
        data = urllib.parse.urlencode({'data': result, 'lexer': lexer})
        r = opener.open("http://paste.in.ua", data.encode('utf-8'))
        sublime.set_clipboard(r)
