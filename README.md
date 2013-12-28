inspect.py
==========

A simple tool for a quick web page inspection. It supports both Python 2 and 3.

Install
-------

    $ pip install -r requirements.txt

Example
-------

    $ python inspect.py http://2gle.me
    GET http://2gle.me... 301 Moved Permanently [0.106582 sec]
    > GET http://www.2gle.me/... 200 OK [0.259101 sec]

    http://www.2gle.me/
    ===================
    * Server: Google Frontend
    * Content-Type: text/html; charset=utf-8
    * Encoding: utf-8
    * DocType: HTML 5
    * Title: 2gle.me
    * Description: Yet another link shortener

    Cookies:
    --------
    Nope

    Style sheets:
    -------------
    1. netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap.no-icons.min.css (version 2.3.1)
    2. netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css (version 3.2.1)

    Scripts:
    --------
    1. ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js (version 1.10.2)
    2. netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js (version 2.3.1)

License
-------

Copyright (C) 2013 Andrew A. Usenok &lt;tooogle@mail.ru&gt;

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
