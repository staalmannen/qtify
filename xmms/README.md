XMMS 1.2.11, the GTK 1.2 audio player, built from its unmodified source
against gtk-made-qt: the proof of concept for GTK 1.2 programs on Qt. It
runs without GTK 1.2 or libX11 (the binary, `libxmms` and all plugins).

It uses the shared gtk-made-qt library (`gtk-made-qt-env --shared`),
because its plugins call GTK themselves.

Things every recipe here does, and why:

- The source is the release tarball as imported into GitHub (deepfire/xmms):
  the xmms.org downloads are not reliably reachable.
- Time stamps are reset (sources, then `aclocal.m4`, then the generated
  `configure`, `Makefile.in` and `*.h.in`), or `make` tries to rerun
  automake 1.x.
- `configure` is the 2007 one and is run directly: it rejects options newer
  build helpers pass (`--runstatedir`).
- No LTO: the old configure's function checks then give false positives
  (it finds BSD's `srandomdev`).
- `-std=gnu17`: GTK 1 era C relies on unprototyped functions, which C23
  (GCC 15's default) no longer has.
- `-fno-tree-vectorize`: GCC 14.2 crashes on the ALSA plugin's code with
  `-ffast-math` (the GCC builds; clang does not need it).
- `ac_cv_lib_SM_SmcOpenConnection=no`: no X11 session management (libSM).
- On musl (Alpine, Chimera) `config.sub` is replaced: the 2007 one does not
  know musl.
- `xmms.desktop` is added (XMMS installs none); its icon is XMMS's own
  `wmxmms.xpm`.

Output plugins: ALSA (works with PipeWire's and PulseAudio's ALSA plugins),
OSS and the disk writer. ESD and the OpenGL visualization are left out.
