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

* `/local/modules` - core python scripts. The scripts are here instead of `/_/local/modules` because it makes them more easily accessible from the console.
* `/_` - the root of the `vjzual2` system (`_` is used rather than `project1` or `vjzual2` because it's compatible with all of my other projects)
* `/_/local` - core settings, variables, and centralized tables (data nodes, modules, etc)
* `/_/components` - shared components and scripts. These items are not used directly, but are generally cloned or referenced from elsewhere. The `Text DAT`s that hold scripts for extension classes for shared modules that are cloned are kept outside of the related COMPs in order to avoid having multiple instances of the `Text DAT`s that are bound to the same file.
* `/_/routing` - centralized infrastructure related to MIDI I/O and other control routing

### Modules
Modules are the main structural element in the system. A module is a `Container COMP` with standardized contents and interfaces.

Each module has:
* main `Container COMP` that holds all contents of the module
* (promoted) extension class of either `VjzModule` or a sub-class of `VjzModule`
* standard custom parameters which are set up by the extension class (see Module Settings and State Parameters below)
* module-specific custom parameters (`Mparscale`, `Mparrotate`, etc)
* (optional) video/audio/control inputs - these are `In TOPs`/`In CHOPs` in the module `COMP`
* (optional) video/audio/control outputs - these are Out TOPs/CHOPs in the module `COMP`
* a standard shell UI which includes a header with toggles for module settings, and other generic UI elements, as well as common infrastructure for bypassing the module
* a standard overlay UI which provides dimming/highlighting for bypassed/soloed modules (ideally this would be part of the shell, but it can't be due to UI layering)
* a set of UI components bound to the module's custom parameters

#### Module Settings and State Parameters
Every module has a set of standard custom parameters that are common to all modules. Some of these act as settings for the module (e.g. `Modname`, `Modfullheight`). Others control the state of the module (e.g. `Modcollapsed`, `Modbypass`). These parameters have names that start with "`Mod`".

Parameter | Description
--------- | -----------
`Modname`  | Globally unique ID for each module instance
`Moduilabel` | User-friendly text to show in the module's header (and other places)
`Modbypass` | Bypass the module, output the module's inputs without modifying them
`Modsolo` | Select the module as the main output source (gets sent to display window, recorded video file, etc)
`Modshowviewers` | Show/hide video/etc preview panels in the module's UI
`Modcollapsed` | Expand/collapse the module's UI panel
`Modshowadvanced` | Show/hide advanced parameters in the module's UI
`Modfullheight` | The height of the module UI panel when advanced parameters are shown
`Modcompactheight` | The height of the module UI panel when advanced parameters are hidden
`Modhasadvanced` | Indicates whether the module has any advanced parameters (see `Modshowadvanced`). This controls whether the show/hide advanced toggle is enabled in the module's header.
`Modhasviewers` | Indicates whether the module has any viewer panels (see `Modshowviewers`). This controls whether the show/hide `viewers` toggle is enabled in the module's header.
`Modparuimode` | UI mode for the module's parameters (see below)
`Modhidden` | Controls whether the module shows up in global module lists. This is generally used for master modules which are intended to be cloned.

#### Module Parameters
Each `Module`'s behavior is defined by a set of `Parameters` that are specific to each type of module. They have names that start with "`Mpar`". For example, a transform module would have parameters like `Mparscale`, `Mparrotate`, `Mparsx` (X scale), `Mparsy` (Y scale), etc.

A module `Parameter` is a TD custom parameter on the module, which may be bound to a param component that provides a UI and MIDI/control mapping support. The parameters can be of any type, but not all types are fully supported.


...

## Data Nodes and Selectors
Data nodes are components which expose video, audio, and/or control data. By default, each module has a data node that exposes the module's outputs. The system scans for these nodes and maintains a centralized list of their locations and properties.

Data selectors are components which select data from data nodes, and include a UI with a drop down list of available nodes as well as previewing of the selected data.

Data nodes/selectors are the main routing mechanism through which modules communicate with each other (aside from hard-wired input/output connections).

Example uses:
* warping module selects a video stream from another module to use for distorting its input video stream
* mixer module blends a video stream from another module with its input video stream
* soloing/previewing a module means pointing the main output selector to that module's output node

## UI
The root of the control UI is at `/_/uipanel`. It contains the top level module panels (e.g. layer1, layer2, master, global), which in turn contain other module panels.

Each module panel has a header which includes common controls. Clicking on the header expands/collapses the module panel (via `Modcollapsed`). When a module is bypassed (via `Modbypass`), a gray overlay is shown over the module's inner UI components, but it does not disable them. This makes it possible to bypass a module, modify some settings, and then switch it back on. The parameter UI mode dropdown in the module header switches the parameters in that module between UI modes that show the controls (sliders/toggle buttons/drop-downs), or to edit MIDI mappings, etc.

## Initialization
The parameters of various components need to have been set via scripting. While many of these things persist after closing and reopening `vjzual2`, there are some that do not (such as parameter slider ranges and menu options). This is a bug and should hopefully be fixed at some point. Until then, it is sometimes necessary to re-run the initialization code for a component and its descendants. Any component that needs such initialization (which includes all modules and parameter components) will have a `Text DAT` named `init`, which can be run to handle initialization. Most init scripts call the init scripts of sub-components as follows:
```python
for init in ops('*/init'):
  init.run()
```
Note that init scripts are executable scripts and are not just function definitions (though they may delegate the work to functions). Most components that use extension classes have a method named `Initialize()` which handles the bulk of the initialization work. In order to deal with potential issues related to COMP cloning, init scripts often include setup for the related extension classes as follows:
```python
m = me.parent()
m.python = True
m.par.extension1 = 'mod("...").FooComponent(me)'
m.par.promoteextension1 = True
m.initializeExtensions()

# this calls the Initialize method of the extension class,
# which may not be available until after the extensions
# have been reinitialized
m.Initialize()
```
The editor tools (see below) includes an `Initialize` button which runs init scripts for either the selected COMPs, or the context COMP of the main network editor panel.

## Editor tools
The editor tools panel (typically shown on the side of the main network editor) provides tools for editing components. Many of these are not specific to `vjzual2`, and will at some point be moved out into a separate repository. Most tools currently only work in the context of the main network editor panel (secondary windows don't work, and opening the editor tools panel as a separate window doesn't work). Tools that are intended for COMPs (save .tox file, initialize) first try to operate on whatever is selected in the editor. If nothing applicable is selected, it looks at the context COMP of the editor, and then walks up through its parents until it finds something that can be processed.

## Development Process
...
