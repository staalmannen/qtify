DDD 3.4.1, the GNU Data Display Debugger (a graphical front end for gdb and
other debuggers), built from its unmodified source against motif-on-qt: it
runs as a Qt application without libXm, libXaw, libXt or libX11. DDD mixes
Motif with Athena widgets (its data display graph sits in an Athena Porthole
with a Panner); both come from motif-on-qt.

Notes on the recipes:

- The source is Debian's copy of the release (the same file in Ubuntu).
  It has a generated `configure`, which the recipes use as it is.
- `ac_cv_lib_Xft_XftFontOpen=no`: configure would otherwise find the
  system's libXft, which pulls in the real libX11. Motif on Qt draws its
  fonts through Qt, so Xft is not needed.
- flex generates `rxscan.C` during the build. bison is listed as well,
  because configure looks for it.
- The check runs `ddd --version`. That starts the toolkit, reads the
  command line through Xrm and prints the version without a debugger.
- gdb is a run-time dependency: DDD starts it for the program you debug.
- Chimera: the template turns off the `int` hardening. DDD adds the
  `INT_MIN` sentinels of an empty graph's region at start-up (an upstream
  signed overflow that the trap stops, with real Motif too).
- Needs motif-on-qt 80f6839 or newer (Athena widgets, Xpm, converters,
  `XmIsXxx` class bits, Xrm escapes, XmText's cursor rules, events for
  destroyed widgets).

Tested: loading a program, the source window with line numbers, setting a
breakpoint from the gdb console, running to it (the execution arrow), and a
data display in the graph window.
