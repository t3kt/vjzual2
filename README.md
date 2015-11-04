# vjzual2
vjzual2 is a modular video processing and VJ performance system built in [TouchDesigner](http://derivative.ca/).

## Goals
* Modular - functionality should be encapsulated in modules which are (relatively) self-contained.
* Configurable - modifying settings such as rendering resolution should be easy, as should managing module parameters (preset saving/loading, etc).
* Extensible - adding new functionality should be (relatively) straightforward (e.g. it should be easier to create a new effect module that has all the control/ui/mapping/etc features that other modules have than it would be to write an FFGL plugin to add an effect to [Resolume](http://resolume.com/))
* Controllable - control in a performance setting should be (relatively) straightforward
* Awesome - yep.

## Structure
The system is structured as tree of modules, with modules nested within other modules.

### Modules
Modules are the main structural element in the system. A module is a COMP (Container COMP) with standardized contents and interfaces.

Each module has:
* main Container COMP that holds all contents of the module
* (promoted) extension class of either VjzModule or a sub-class of VjzModule
* standard custom parameters which are set up by the extension class (Modname, Modbypass, Modshowviewers, etc)
* module-specific custom parameters (Mparscale, Mparrotate, etc)
* (optional) video/audio/control inputs - these are In TOPs/CHOPs in the main COMP
* (optional) video/audio/control outputs - these are Out TOPs/CHOPs in the main COMP
* a standard shell UI which includes a header with toggles for module settings, and other generic UI elements, as well as common infrastructure for bypassing the module
* a standard overlay UI which provides dimming/highlighting for bypassed/soloed modules (ideally this would be part of the shell, but it can't be due to UI layering)
* a set of UI components bound to the module's custom parameters

...

### Parameters
...

### Data Nodes and Selectors
Data nodes are components which expose video, audio, and/or control data. By default, each module has a data node that exposes the module's outputs. The system scans for these nodes and maintains a centralized list of their locations and properties.

Data selectors are components which select data from data nodes, and include a UI with a drop down list of available nodes as well as previewing of the selected data.

Data nodes/selectors are the main routing mechanism through which modules communicate with each other (aside from hard-wired input/output connections).

Example uses:
* warping module selects a video stream from another module to use for distorting its input video stream
* mixer module blends a video stream from another module with its input video stream
* soloing/previewing a module means pointing the main output selector to that module's output node

## UI
...

## Initialization
...

## Development Process
...
