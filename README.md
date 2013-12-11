inspect.py
==========

A simple tool for a quick web page inspection. It supports both Python 2 and 3.

Install
-------

    $ pip install -r requirements.txt

Example
-------

    $ python inspect.py http://2gle.me
    GET http://2gle.me... 301 Moved Permanently [0.108643 sec]
    >> GET http://www.2gle.me/... 200 OK [0.224851 sec]

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
    1. bootstrap.no-icons.min.css (version 2.3.1)
    2. font-awesome.min.css (version 3.2.1)

    Scripts:
    --------
    1. jquery.min.js (version 1.10.2)
    2. bootstrap.min.js (version 2.3.1)

Todo
----

* HTTP authentication (Basic and Digest)
* Custom Cookies
* Custom User-Agent header
* HTTP proxy support

PRs are welcome! :)

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
