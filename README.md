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
* standard custom parameters which are set up by the extension class (see Module Settings and State Parameters below)
* module-specific custom parameters (Mparscale, Mparrotate, etc)
* (optional) video/audio/control inputs - these are In TOPs/CHOPs in the main COMP
* (optional) video/audio/control outputs - these are Out TOPs/CHOPs in the main COMP
* a standard shell UI which includes a header with toggles for module settings, and other generic UI elements, as well as common infrastructure for bypassing the module
* a standard overlay UI which provides dimming/highlighting for bypassed/soloed modules (ideally this would be part of the shell, but it can't be due to UI layering)
* a set of UI components bound to the module's custom parameters

#### Module Settings and State Parameters
Every module has a set of standard custom parameters that are common to all modules. Some of these act as settings for the module (e.g. Modname, Modfullheight). Others control the state of the module (e.g. Modcollapsed, Modbypass). These parameters have names that start with "Mod".

Parameter | Description
--------- | -----------
Modname  | Globally unique ID for each module instance
Moduilabel | User-friendly text to show in the module's header (and other places)
Modbypass | Bypass the module, output the module's inputs without modifying them
Modsolo | Select the module as the main output source (gets sent to display window, recorded video file, etc)
Modshowviewers | Show/hide video/etc preview panels in the module's UI
Modcollapsed | Expand/collapse the module's UI panel
Modshowadvanced | Show/hide advanced parameters in the module's UI
Modfullheight | The height of the module UI panel when advanced parameters are shown
Modcompactheight | The height of the module UI panel when advanced parameters are hidden
Modhasadvanced | Indicates whether the module has any advanced parameters (see Modshowadvanced). This controls whether the show/hide advanced toggle is enabled in the module's header.
Modhasviewers | Indicates whether the module has any viewer panels (see Modshowviewers). This controls whether the show/hide viewers toggle is enabled in the module's header.
Modparuimode | UI mode for the module's parameters (see below)
Modhidden | Controls whether the module shows up in global module lists. This is generally used for master modules which are intended to be cloned.

#### Module Parameters
Each module's behavior is defined by a set of parameters that are specific to each type of module. They have names that start with "Mpar". For example, a transform module would have parameters like Mparscale, Mparrotate, Mpartx (translate X), Mparty (translate Y), etc.

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
