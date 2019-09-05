## Description

Documentation for the Lab DB RESTful API.

While this API is specific to the [LIMS](https://en.wikipedia.org/wiki/Laboratory_information_management_system) designed for the [Linington Lab](https://linington.chem.sfu.ca/), minor changes could be made to suit any NP Chemistry research groups needs.

This API drives a MySQL database, for which the schema can be found [here](schema).

---

## Overview

### API Root

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](api_root)|[/api/v1/](api_root)|List API resources
[GET](api_root)|[/api/v1/heartbeat](api_root)|API Heartbeat

### Authentication

**TODO**

### Divers

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](divers)|[/api/v1/divers](divers)|List all divers
[POST](divers)|[/api/v1/divers](divers)|Create a new diver
[GET](divers)|[/api/v1/divers/:id](divers)|Get one diver
[DELETE](divers)|[/api/v1/divers/:id](divers)|Delete one diver
[PUT](divers)|[/api/v1/divers/:id](divers)|Update one diver

### Dive Sites

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](divesites)|[/api/v1/divesites](divesites)|List all dive sites
[POST](divesites)|[/api/v1/divesites](divesites)|Create a new dive site
[GET](divesites)|[/api/v1/divesites/:id](divesites)|Get one divesite
[DELETE](divesites)|[/api/v1/divesites/:id](divesites)|Delete one divesite
[PUT](divesites)|[/api/v1/divesites/:id](divesites)|Update one divesite

### Extracts

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](extracts)|[/api/v1/extracts](extracts)|List all extracts
[POST](extracts)|[/api/v1/extracts](extracts)|Create a new extract
[GET](extracts)|[/api/v1/extracts/:id](extracts)|Get one extract
[DELETE](extracts)|[/api/v1/extracts/:id](extracts)|Delete one extract
[PUT](extracts)|[/api/v1/extracts/:id](extracts)|Update one extract

### Fractions

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](fractions)|[/api/v1/fractions](fractions)|List all fractions
[POST](fractions)|[/api/v1/fractions](fractions)|Create a new fraction
[GET](fractions)|[/api/v1/fractions/:id](fractions)|Get one fraction
[DELETE](fractions)|[/api/v1/fractions/:id](fractions)|Delete one fraction
[PUT](fractions)|[/api/v1/fractions/:id](fractions)|Update one fraction

### Isolates

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](isolates)|[/api/v1/isolates](isolates)|List all isolates
[POST](isolates)|[/api/v1/isolates](isolates)|Create a new isolate
[GET](isolates)|[/api/v1/isolates/:id](isolates)|Get one isolate
[DELETE](isolates)|[/api/v1/isolates/:id](isolates)|Delete one isolate
[PUT](isolates)|[/api/v1/isolates/:id](isolates)|Update one isolate

### Media

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](media)|[/api/v1/media](media)|List all media
[POST](media)|[/api/v1/media](media)|Create a new media
[GET](media)|[/api/v1/media/:id](media)|Get one medium
[DELETE](media)|[/api/v1/media/:id](media)|Delete one medium
[PUT](media)|[/api/v1/media/:id](media)|Delete one medium

### Permits

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](permits)|[/api/v1/permits](permits)|List all permits
[POST](permits)|[/api/v1/permits](permits)|Create a new permit
[GET](permits)|[/api/v1/permits/:id](permits)|Get one permit
[DELETE](permits)|[/api/v1/permits/:id](permits)|Delete one permit
[PUT](permits)|[/api/v1/permits/:id](permits)|Update one permit

### Samples

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](samples)|[/api/v1/samples](samples)|List all samples
[POST](samples)|[/api/v1/samples](samples)|Create a new sample
[GET](samples)|[/api/v1/samples/:id](samples)|Get one sample
[DELETE](samples)|[/api/v1/samples/:id](samples)|Delete one sample
[PUT](samples)|[/api/v1/samples/:id](samples)|Update one sample

### Sample Types

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](sampletypes)|[/api/v1/sampletypes](sampletypes)|List all sampletypes
[POST](sampletypes)|[/api/v1/sampletypes](sampletypes)|Create a new sampletype
[GET](sampletypes)|[/api/v1/sampletypes/:id](sampletypes)|Get one sampletype
[DELETE](sampletypes)|[/api/v1/sampletypes/:id](sampletypes)|Delete one sampletype
[PUT](sampletypes)|[/api/v1/sampletypes/:id](sampletypes)|Update one sampletype

### Screen Plates

HTTP Method|Endpoint|Function
-----------|--------|--------
[GET](screenplates)|[/api/v1/screenplates](screenplates)|List all screenplates
[POST](screenplates)|[/api/v1/screenplates](screenplates)|Create a new screenplate
[GET](screenplates)|[/api/v1/screenplates/:id](screenplates)|Get one screenplate
[DELETE](screenplates)|[/api/v1/screenplates/:id](screenplates)|Delete one screenplate
[PUT](screenplates)|[/api/v1/screenplates/:id](screenplates)|Update one screenplate


---

## Versioning

This is the first version of the API.

---

## Changes

*No changes*