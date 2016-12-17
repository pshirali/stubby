# Stubby


#### Preface


> Stubby is a demo project which was presented as part of a talk on Dependency Injection in Python. It uses the [Aglyph](http://aglyph.readthedocs.io/en/latest/) DI framework to instantiate the application. The focus of this project is primarily on how the application builds its dependencies using a DI framework.

> 
> As a HTTP stub server it provides a minimal features. If you are here looking for a feature-rich high-performance HTTP stub server, this might not be the right choice. However, you are welcome to evaluate it.


## Introduction


Stubby is a HTTP stub server written in Python using Bottle. Stubby listens to all HTTP requests over methods that Bottle supports, and returns an empty 200-OK response. Stubby keeps a count of the requests's method, url and query-string in-memory. A dump of the current stats can be sought during runtime.


## Installation


#### Prerequisites


1. Python 2 or 3 (latest preferable)
2. VirtualEnv and virtualenvwrapper


#### Deployment


As Stubby is a demo project intended for code introspection and tinkering, it is not available as a `pip installable`. You can download the repo as an archive. If you use `git`, you can clone the repo. Following are all the commands you need for preparing a virtualenv and installing the required packages.


```
git clone https://github.com/pshirali/stubby
cd stubby
mkvirtualenv stubby
pip install -r requirements.txt
```


Once you have done the above, you can run `./st` which is Stubby's entrypoint script.


```
./st -h
```


## Features & Usage


Stubby listens to `localhost` on port `8080` by default. The HTTP methods supported are `GET`, `PUT`, `POST`, `DELETE` and `PATCH`. You can make requests to any URI. Stubby only stores the HTTP method, URI path and the query-string (as a single string `<path>?<query>`)


Stubby also registers some control routes under the prefix `/_st/*` to allow accessing its features during runtime.


```
GET http://localhost:8080/_st/help     # shows routes and description
GET http://localhost:8080/_st/stats    # returns all the stats on requests collected so far
GET http://localhost:8080/_st/reset    # resets the stats
```


Signals SIGUSR1 and SIGUSR2 are also registered for retrieval of stats and resetting of stats. When stats are retrieved through a signal, they are pretty-printed on console. The switch `--skip-ctrl` can be used to skip registering all `/_st/*` routes (thereby allowing a stub even on these URLs). The `INFO` logs during startup display Stubby's `PID`. You can send a signal using the following command on linux.


```
kill -SIGUSR1 <pid>
```


## The Application Context


Classes and their dependencies are wired through the XML context file `app-context.xml`. This XML maps the id of the service against the dotted-name of the class that must be used for it. Hence, any changes to use a different class against a service need to be made in this file.


**Example:** To use a different logger class for the application's logger, the compoent `st-logger`'s dotted-name could be changed to say `stubby.logger.BasicLogger` instead of `stubby.logger.ColorLogger`.


## Logging and Tracing


Stubby, by default logs all modules under `stubby` with `INFO` level logging. This can be enhanced to `DEBUG` by supplying the `--debug` switch on CLI.


A switch `--trace` optionally traces the instantiation of traceable classes. This can be used to inspect the order in which classes and dependencies from the context were assembled. If you'd like to dig further, you can also enabled the logging on Aglyph library using the switch `--aglyph`. The loglevel chosen applies to both `stubby` and `aglyph`.


## Presentation and further reading


1. Stubby is example code which was written as part of the presentation [Dependency Injection in Python](http://pshirali.github.io/dependency_injection) available [here](https://github.com/pshirali/dependency_injection/)

2. Aglyph's documentation also explains Martin Fowler's example on Dependency Injection. You can read the latest docs [here](http://http://aglyph.readthedocs.io/en/latest/)


## License


The code in this repo has been published under the MIT license.


No part of the code in this repo and the presentation (Dependency Injection in Python) must be considered official documentation or official reference for Aglyph. They are merely a reference implementation, and do not utilize or cover all features that Aglyph has to offer. Please refer to Aglyph's official documentation to know about all of its features.


All copyrights belong to respective authors.