.. _tutorial_create:

Tutorial - Creating a Service
=============================

StackHut allows you to rapidly deploy your code as an API in the cloud. Your code is wrapped up and runs inside a container whose functions you can call over HTTP. 

This tutorial briefly describes how you can develop, test and deploy a simple service onto StackHut in a few minutes. Fristly just check that you've installed the dependencies as mentioned in :ref:`installation`. We also recommend watching the following, short, companion video that walks you through setting up a Python-based service.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/Y8vBQCgA944" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>


Further information on creating a service can be found in :ref:`usage_cli` and :ref:`usage_project`.

Initialise a Project
--------------------

We start by initialising a StackHut project, let's call this one ``demo-python``,

.. code-block:: bash

    # create and cd into the project directory
    mkdir demo-python
    cd demo-python
    # run stackhut init to initialise the project
    stackhut init fedora python

The ``stackhut init`` command takes two parameters, the base operating system, in this case Fedora, and the language stack to use, here Python. In return it creates a working skeleton project for you to start with. 
This project contains all the files a StackHut service needs, already configured using sensible defaults for the chosen project,

.. code-block:: bash

    demo-python [master] » ls
    api.idl  app.py  Hutfile  README.md  requirements.txt  test_request.json

There are several files here - and we'll cover the important ones in the following sections.
The ``Hutfile`` is a *YAML* file containing configuration regarding our stack and dependencies. More information regarding its parameters can be found in :ref:`usage_project_hutfile`.

.. There is also a README.md markdown file to further describe your service.


Signature
---------

The ``api.idl`` interface-definition (IDL) file describes our service interface - after deployment these entry-points are accessible over HTTP.
The file uses a C/Java-like syntax to describe the service interface using JSON types, e.g. numbers, strings, lists, and objects. This is based on the `Barrister RPC <http://barrister.bitmechanic.com/>`_, and the format is described further in the `project documentation <http://barrister.bitmechanic.com/docs.html>`_.

Let's take a look,

.. code-block:: java

    interface Default {
        // add 2 integers and return the result
        add(x int, y int) int
    }


By default we are exposing a single function, ``add``, that takes two ``ints``, and returns an ``int``. Now let's add a new function, ``multiply``, and write the corresponding signature - all pretty straightforward,

.. code-block:: java

    interface Default {
        // add 2 integers and return the result
        add(x int, y int) int

        // multiply 2 integers and return the result
        multiply(x int, y int) int
    }


Code
----

Having defined our interface we may now write our code. The app code lives in ``app.py`` (or ``app.js`` for JS, and so on), as follows,

.. code-block:: python

    """
    Demo service
    """
    import stackhut

    class DefaultService:
        def __init__(self):
            pass

        def add(self, x, y):
            return x + y

    # export the services
    SERVICES = {"Default": DefaultService()}

As seen, the service is a plain old Python class with a function for each entrypoint. The ``add`` function has already been implemented and is simple enough. Now let's add the ``multiply`` function, no surprises here. 

.. code-block:: python

    """
    Demo service
    """
    import stackhut

    class DefaultService:
        def __init__(self):
            pass

        def add(self, x, y):
            return x + y

        def multiply(self, x, y):
            return x * y

    # export the services
    SERVICES = {"Default": DefaultService()}



Test
----

Now we're done coding and because we're all responsible developers let's test before we deploy. 
By default there is a file called ``test_request.json`` that simulates an HTTP request to our service. This files specifies specifies the ``serviceName``, the ``method``, and ``parameters`` already configured for the ``add`` endpoint 


.. code-block:: json

    {
        "serviceName": "demo-python",
        "req": {
            "method": "add",
            "params": [2, 2]
        }
    }

.. note:: This format is actually JSON-RPC - described further in :ref:`tutorial_use`

Let's run our service this file as-is to test our ``add`` function,

.. code-block:: bash

    stackhut -v run test_request.json

The output of calling this method on the service can be found in the ``run_results`` directory - let's look at the request output, ``response.json``,

.. code-block:: json

    {
        "jsonrpc": "2.0", 
        "id": "7fad6810-35ef-4891-b6b3-769aeb3c1d25"
        "result": 4
    }


Let's modify this to test our multiply function, and run it again,

.. code-block:: json

    {
        "serviceName": "demo-python",
        "req": {
            "method": "multiply",
            "params": [3, 2]
        }
    }

.. code-block:: bash

    stackhut -v run test_request.json

.. code-block:: json

    {
        "jsonrpc": "2.0", 
        "id": "73a04803-ff37-4f7a-9763-349d57e54123"
        "result": 6
    }

Great, so things are all working, right? Well, the ``stackhut run`` command by default runs the service using your own host OS and any dependencies you have installed. However, to be fully test your setup you may wish to locally build the container image and run your code within it. That way you'll be running the exact same code, in the same container, as will be on the server.

You can achieve this by first building the image,

.. code-block:: bash

    stackhut build

and then running it using the ``-c`` flag,

.. code-block:: bash

    stackhut run -c test_request.json

This runs the service request in the container, using the ``test_request.json`` file from the host project directory, and similarly writes the output to the ``run_results`` directory on the host. Looking at ``run_results/output.json``,

.. code-block:: json

    {
        "jsonrpc": "2.0", 
        "id": "7fad6810-35ef-4891-b6b3-769aeb3c1d25"
        "result": 6
    }

Great, so we've built and tested a container with your code, and it's all working against the stack and dependencies specified in the ``Hutfile``. We're now ready to deploy and host your service on the StackHut platform. 


Deploy
------

This couldn't be simpler,

.. code-block:: bash

    stackhut deploy

This packages and builds your service, and then deploys it to StackHut along with metadata such that it may be searched, viewed, and importantly, used, on the platform. 
As soon as this completes, your API is live on `https://api.stackhut.com/run` and can be browsed from our `repository of existing APIs <https://www,stackhut.com/#/services>_`.
 
Use
---

We can view the API from the `website <https://www,stackhut.com/#/services/demo-python>_`, browse the documentation, and for instance, call the ``multiply`` function.
The service is live and ready to receive requests right now in the browser or from anywhere else via HTTP. 

Further documentation on how to call and make use of a StackHut from your code can be found in :ref:`tutorial_use`.
Thanks for reading this - we've been using StackHut to create web-scrapers, image processing tools, video conversion APIs and more and we'd love to see what you come up with. 

