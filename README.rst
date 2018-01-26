Buroca
======

"Buroca" is a Python command line tool that helps implementing a "bureaucracy 
as code" philosophy of project management. It was created to help creating documents for a 
partnership project between a public University and the Federal Goverment in Brazil, -- 
a case that we can certainly expect lots of pointless paperwork. Buroca can 
also help with other workflows that involves automatic generation of documents.

A "buroca" project keeps a centralized data store and a set of document 
templates. It fills the gaps by providing automatic document generation and 
easy synchronization of generated documents with the data store. Buroca 
understands arbitrary text files (e.g: markdown, LaTeX, etc) and LibreOffice 
spreadsheets.


Installation
------------

Buroca requires Python 3 and a few other libraries available on pip. You can 
grab it from pip::

    $ pip3 install buroca --user

More advanced usage requires `pandoc <http://pandoc.org>` and an working 
instance of LibreOffice. It probably works only on Linux, but you're welcome to
contribute Windows support ;). 


Usage
-----

Start creating by a project folder structure::

    $ buroca init

It will create the following folder structure in the current directory::

    data/
    reports/
    templates/

Data must contain a set of YAML files that encode information about each entity
in your project. You can create arbitrary YAML files representing people, 
inventory, reports or anything you want.

A fairly common usage is to include a person/ sub-folder with one file per 
person::

    data/
     |- band.yml           -- generic project information
     \- person             -- we create one YAML file per member of the
         |- john.yml          project
         |- paul.yml
         |- ringo.yml
         \- george.yml

The content of those files is arbitrary, as long as they encode dictionaries:

.. code-block:: YAML

    # john.yml
    name: John Winston Lennon
    role: singer
    instruments:
        - guitar
        - keyboard
        - harmonica
        - tambourine

Now, we must create some template documents in the "templates" folder. They can 
be either arbitrary text files or Libre Office spreadsheets. Those files are 
interpreted as `Jinja2 <http://jinja.pocoo.org>` templates. The toplevel files 
and folders are exposed as variables in the Jinja templates. 

Consider a ``templates/resumee.md`` file:

.. code-block:: markdown

    # Resumée

    Name: {{ person.name }}

    {{ person.name }} is the {{ person.role }} of {{ band.name }}. He can play
    {% for instrument in person.instruments %}{{ instrument }}
    {%- if not loop.last %}, {% endif %}{% endfor %}.

    {{ person.name }} used to play on {{ band.name }}, the greatest rock band 
    in history!

Now that we have a template, we can generate files from YAML data::

    $ buroca do resumee.md person/john

This will create a resume-john.md file under "reports/" that inserts all 
information in the YAML files into the correct places. If we want to generate 
files for all members at once, just type::

    $ buroca do resumee.md person/*

It will scan all files like ``data/person/*.yml`` and create a report for each 
person. 

Export to PDF
-------------

Buroca integrates with `pandoc <http://pandoc.org>` and can convert several
input files to pdf. This is particularly useful to aggregate reports for different
entities into a single file. This is useful, for instance, when you want to send
files for printing::

    $ buroca do resumee.md person/* -t pdf --single


What about this name?
---------------------

"Buroca" is the informal way Brazillians calls "bureaucracy". Pointless 
bureacracy is so prevalent in Brazillian life that we have to invent cute names 
to better cope with it ;)
