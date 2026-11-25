Grace 5.1.25 (xmgrace), the Motif 2D plotting tool, built from its
unmodified source against motif-on-qt: it runs as a Qt application without
libXm, libXt or libX11.

Notes on the recipes:

- The source is Debian's copy of the release (the same file in Ubuntu).
  Grace's bundled Xbae matrix widget and T1lib are used: system Xbae is
  built for real Motif, and T1lib is no longer packaged.
- configure is pointed at Motif on Qt's headers and libraries with
  `--x-includes` / `--x-libraries` (it would look for the system's X11);
  the paths are the first `-I` / `-L` of `motif-on-qt-env`.
- Off: the PDFlib driver (PDFlib is not free software; PostScript, EPS,
  SVG, PNG and JPEG output stay), netCDF, FFTW (Grace's own FFT is used)
  and the XmHTML help viewer (help opens in a browser).
  grconvert is not built: it needs the XDR library.
- `-std=gnu17` and `-Wno-error=...`: 2000-era C with implicit declarations,
  implicit `int` (Xbae's K&R definitions) and unprototyped functions, which
  GCC 14 / clang 16 and C23 reject; hardened builds also reject T1lib's
  `printf (model)`.
- Grace installs everything into `/usr/share/grace`; the recipes move the
  programs to `/usr/bin` (`xmgrace`, with `gracebat` and `grace` links,
  `convcal`, `fdf2fit`), `libgrace_np.a` and `grace_np.h` to `/usr/lib` and
  `/usr/include`, as Debian's own grace does, and install the man pages.
- The check runs `xmgrace -version`: it starts the toolkit and prints the
  build (Motif, Xbae, T1lib versions).
- Needs motif-on-qt 5704888 or newer (bitmap clip masks, dialogs realized
  with their program classes, Manager GCs, Xt's converter functions).

Built, installed and run on Ubuntu 24.04.

No Alpine or Chimera recipe for now: on musl Grace aborts at start-up. It
closes every file with `pclose()` and falls back to `fclose()` when that
fails; `pclose()` of a stream `popen()` did not open is undefined, and
musl closes it before failing, so the file is closed twice. That is
Grace's own bug (real Motif hits it too) and needs a change to Grace's
source, which qtify does not make. (Both recipes were written and built:
they are in the git history, commit 653739d.)

Tested (installed, Ubuntu): a data file plotted (axis labels from T1lib), the axis
dialog with Grace's own Tab widget and its user-tick Xbae matrix, the data
set dialog's statistics matrix, the font tool, compared with Ubuntu's
grace on real Motif.
