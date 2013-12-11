#!/usr/bin/env python
# Copyright (C) 2013  Andrew A. Usenok <tooogle@mail.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import sys
import re
from argparse import ArgumentParser

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import requests
import bs4


def request(url, *args, **kwargs):
    print('GET {}... '.format(url), end='', file=sys.stderr)
    try:
        res = requests.get(url, *args, **kwargs)
    except requests.exceptions.ConnectionError:
        print('connection error!', file=sys.stderr)
    except requests.exceptions.Timeout:
        print('timeout!', file=sys.stderr)
    else:
        for r in list(res.history) + [res]:
            code = r.status_code
            reason = r.reason
            elapsed = r.elapsed.total_seconds()
            print('{} {} [{} sec]'.format(code, reason, elapsed), file=sys.stderr)

            if 'location' in r.headers:
                location = r.headers['location']
                print('>> GET {}... '.format(location), end='', file=sys.stderr)

        if res.ok:
            return res

    return None


def get_doctype(doctype):
    doctype = doctype.upper()

    if doctype == 'HTML':
        return 'HTML 5'

    for dt in ('HTML 4.01', 'XHTML 1.0', 'XHTML 1.1'):
        if dt in doctype:
            return dt

    return 'unknown'


def get_basename(link):
    return urlparse(link).path.split('/')[-1]


# Regular expression to match against version.  {{{
_VERSION_RE = re.compile(r'''
    (\d+\.)?(\d+\.)(\d+) |                   # x.y.z or x.y
    ([1-2][0-9]{3})([0-1][0-9])([0-3][0-9])  # YYYYMMDD
''', re.VERBOSE)
# }}}

def guess_version(link, base_url):
    # Try to find version in the link.
    match = _VERSION_RE.search(link)
    if match is not None:
        return match.group()

    url = link if re.match(r'^https?://', link) else urljoin(base_url, link)

    # Try to find version in the script itself.
    res = request(url)
    if res is not None:
        for i, line in enumerate(res.iter_lines()):
            if i > 20:  # look only at the beginning
                break
            if len(line) > 200:  # minified script
                break

            match = _VERSION_RE.search(str(line))
            if match is not None:
                return match.group()

    # We did our best... :(
    return 'unknown'


def inspect(url, output, verbose=False):
    # Try to get the document.
    res = request(url)
    if res is None:
        return

    # Parse the document.
    content_type = res.headers.get('content-type', 'text/html')
    if 'charset' not in content_type and 'text' in content_type:
        res.encoding = None  # let BeautifulSoup choose the encoding

    soup = bs4.BeautifulSoup(res.content, 'html5lib', from_encoding=res.encoding)

    # Make a report.
    print(res.url, file=output)
    print('=' * len(res.url), file=output)

    # 'Server' HTTP header.
    if 'server' in res.headers:
        print('* Server:', res.headers['server'], file=output)

    # 'X-Powered-By' HTTP header.
    if 'x-powered-by' in res.headers:
        print('* X-Powered-By:', res.headers['x-powered-by'], file=output)

    # 'Content-Type' HTTP header.
    if 'content-type' in res.headers:
        print('* Content-Type:', res.headers['content-type'], file=output)

    # Page encoding.
    print('* Encoding:', soup.original_encoding, file=output)

    # Page DocType.
    doctypes = [item for item in soup.contents if isinstance(item, bs4.Doctype)]
    if doctypes:
        print('* DocType:', get_doctype(doctypes[0]), file=output)

    # Page title.
    if soup.title is not None:
        print('* Title:', soup.title.string.strip(), file=output)

    # Page meta description.
    description = soup.find('meta', attrs={'name': 'description'}, content=True)
    if description is not None:
        print('* Description:', description['content'].strip(), file=output)

    # Page meta generator.
    generator = soup.find('meta', attrs={'name': 'generator'}, content=True)
    if generator is not None:
        print('* Generator:', generator['content'].strip(), file=output)

    # Cookies.
    print(file=output)
    print('Cookies:', file=output)
    print('--------', file=output)
    for i, (name, value) in enumerate(res.cookies.items(), 1):
        print('{}. {} = {}'.format(i, name, value), file=output)
    if not res.cookies:
        print('Nope', file=output)

    # Page style sheets.
    print(file=output)
    print('Style sheets:', file=output)
    print('-------------', file=output)
    sheets = soup.find_all('link', rel='stylesheet', href=True)
    for i, sheet in enumerate(sheets, 1):
        basename = get_basename(sheet['href'])
        version = guess_version(sheet['href'], res.url)

        print('{}. {} (version {})'.format(i, basename, version), file=output)
        if verbose:
            if sheet.string:
                sheet.string.replace_with('...')  # omit style sheet contents
            print('  ', sheet, file=output)
    if not sheets:
        print('Nope', file=output)

    # Page scripts.
    print(file=output)
    print('Scripts:', file=output)
    print('--------', file=output)
    scripts = soup.find_all('script', src=True)
    for i, script in enumerate(scripts, 1):
        basename = get_basename(script['src'])
        version = guess_version(script['src'], res.url)

        print('{}. {} (version {})'.format(i, basename, version), file=output)
        if verbose:
            if script.string:
                script.string.replace_with('...')  # omit script contents
            print('  ', script, file=output)
    if not scripts:
        print('Nope', file=output)

    return


def main():
    parser = ArgumentParser()
    parser.add_argument('-V', '--version',
            action='version', version='%(prog)s v0.01')
    parser.add_argument('-v', '--verbose',
            action='store_true', help='be more verbose')
    parser.add_argument('-o', '--output',
            help='write report to the file')
    #parser.add_argument('-a', '--auth',
    #        help='HTTP authentication credentials (username:password)')
    #parser.add_argument('-D', '--digest',
    #        action='store_true', help='use HTTP Digest authentication')
    #parser.add_argument('-c', '--cookie',
    #        action='append', dest='cookies',
    #        help='send custom Cookie (can be used several times)')
    #parser.add_argument('-u', '--user-agent',
    #        help='set User-Agent HTTP header')
    #parser.add_argument('-p', '--proxy',
    #        help='use HTTP proxy (http://[username[:password]@]host[:port])')
    parser.add_argument('url',
            metavar='URL', help='URL to inspect')
    args = parser.parse_args()

    # Buffer console output via StringIO.
    output = (StringIO() if args.output is None else
              open(args.output, 'w'))

    inspect(args.url, output, args.verbose)

    if isinstance(output, StringIO):
        print()
        print(output.getvalue(), end='')

    output.close()

if __name__ == '__main__':
    sys.exit(main())
