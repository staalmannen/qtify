# Dependency & Compatibility Analysis for `qtify` Target Applications

This report evaluates the dependency trees and toolkit requirements of four classic legacy applications (**NEdit**, **Asunder**, **Sylpheed**, and **XmGrace**) against the current capabilities of `motif-on-qt` and `gtk-made-qt`.

---

## Executive Summary

| Application | Toolkit Target | Shim Compatibility | Primary Risk / Missing Feature | Recommended Priority |
| :--- | :--- | :--- | :--- | :--- |
| **NEdit / XNEdit** | Motif 2.x / X11 | **Very High** | Heavy custom `DrawingArea` text widget & X11 font/clipboard edge cases | **1 (Immediate Win)** |
| **Asunder** | GTK 2.4+ | **Very High** | Minor `GdkPixbuf` icon loading (`gdk-pixbuf2` required at link/runtime) | **2 (Immediate Win)** |
| **XmGrace** | Motif 2.x / X11 | **High** | Custom Xlib/Motif canvas & optional third-party scientific libs (FFTW, NetCDF) | **3 (High Value)** |
| **Sylpheed** | GTK 2.24+ | **Moderate–High** | Heavy `GtkTreeView` cell renderers, `GdkPixbuf` inline images, & drag-and-drop | **4 (Stress Test)** |

---

## 1. NEdit (or XNEdit) — Motif / X11

**Overview:** A fast, compact programmer's text editor written in ANSI C89, relying purely on Motif and Xlib without external desktop environment frameworks.

### Dependency Tree
* **GUI & Windowing (Replaced by `motif-on-qt`):**
  * `libXm` (Motif 1.2+ / 2.3)
  * `libXt` (X Toolkit Intrinsics)
  * `libX11`, `libXext`, `libXmu`, `libXpm`
* **System / Core:**
  * `glibc` (Standard C library)
  * *Optional (XNEdit fork only):* `fontconfig`, `libXft` (anti-aliased font rendering)

### Compatibility with `motif-on-qt`
* **Strengths:**
  * Uses standard Motif primitives and managers (`XmMainWindow`, `XmRowColumn` menu bars, `XmForm`, `XmBulletinBoard`, `XmPushButton`, `XmToggleButton`, `XmFileSelectionBox`).
  * Relies heavily on `Xrm` resources, translations, actions, and `Xt` timers/work procs—all explicitly implemented in `motif-on-qt`.
  * Standard `NEdit` avoids `Xft` and uses classic XLFD font names and core X11 drawing (`XDrawLine`, `XCopyArea`, `GCs`), which `motif-on-qt` maps directly onto `QPainter`.
* **Watchouts:**
  * NEdit's main text editing area is a custom-drawn `XmDrawingArea` widget (`textDisp.c`) with custom selection, scrolling, and cursor blinking. While `DrawingArea` and `Expose` events are supported, intense Xlib clipping/XOR cursor drawing will thoroughly test your `QPainter` X11 backend.
  * *Recommendation:* Target upstream **NEdit 5.7** first rather than **XNEdit**, as XNEdit introduces `libXft` dependencies not covered by core Xlib shims.

---

## 2. Asunder — GTK 2

**Overview:** A lightweight, standalone graphical Audio CD ripper and encoder written in plain C. It is frequently targeted for removal in modern Linux distributions solely due to its GTK 2 dependency.

### Dependency Tree
* **GUI & Core GLib Stack:**
  * `gtk2` (`>= 2.4.0`) — *Replaced by `gtk-made-qt`*
  * `glib2` (`GLib`, `GObject`) — *Required natively alongside `gtk-made-qt`*
  * `gdk-pixbuf2` — *Required for toolbar/status icons*
* **Domain / Backend Libraries (Non-GUI):**
  * `cdparanoia` (CDDA extraction)
  * `libcddb` (`>= 0.9.5`, freedb/CDDB metadata lookup)
  * `glibc`
* **Runtime CLI Encoders (Optional / Subprocess-based):**
  * `lame`, `flac`, `vorbis-tools`, `opus-tools`, `wavpack` (Invoked via CLI pipes, zero GUI impact)

### Compatibility with `gtk-made-qt`
* **Strengths:**
  * Very small widget footprint: uses `GtkWindow`, `GtkVBox`/`GtkHBox`, `GtkTable`, `GtkToolbar`, `GtkTreeView` (simple track list with toggle and text cell renderers), `GtkEntry`, `GtkCheckButton`, `GtkComboBox`, `GtkProgressBar`, and `GtkDialog`/`GtkFileChooserDialog`.
  * Uses `g_timeout_add()` / `g_idle_add()` to poll ripping/encoding progress bars, which works natively on Qt's GLib-integrated event loop.
  * Does not use custom CSS, complex `GtkBuilder` overrides, or custom widget subclassing.
* **Watchouts:**
  * `gtk-made-qt` notes *"Most of GdkPixbuf"* is missing. Asunder uses `gdk_pixbuf_new_from_file()` or stock icons for its main window icon and toolbar buttons. Linking system `gdk-pixbuf2` (which has no GTK dependency) or stubbing basic pixbuf loading will be sufficient.

---

## 3. XmGrace (Grace) — Motif / X11

**Overview:** A ubiquitous WYSIWYG 2D scientific plotting tool used in physics, chemistry, and engineering labs. It suffers from severe font/scaling issues on modern Wayland/HiDPI desktops due to its unmaintained Motif UI.

### Dependency Tree
* **GUI & Windowing (Replaced by `motif-on-qt`):**
  * `libXm` (Motif 2.x)
  * `libXt`, `libX11`, `libXext`, `libXmu`, `libXpm`
* **Scientific & Export Libraries (Non-GUI):**
  * `libm` / `glibc`
  * *Optional:* `fftw` (Fast Fourier Transforms), `netcdf` (scientific data formats), `libjpeg`, `libpng`, `zlib`, `t1lib` / `freetype` (PostScript/PDF plot export)

### Compatibility with `motif-on-qt`
* **Strengths:**
  * Classic Motif dialog-heavy architecture (`XmForm`, `XmRowColumn`, `XmList`, `XmScale`, `XmTextField`, `XmFileSelectionBox`, `XmDrawingArea`).
  * Eliminating X11 and running XmGrace natively on Qt 6 / Wayland solves its notorious HiDPI scaling problem immediately.
* **Watchouts:**
  * Uses the `XbaeMatrix` widget (a Motif table/spreadsheet widget often bundled internally in Grace's source tree) for editing data sets. `XbaeMatrix` subclasses `XmManager` and uses `XmGadget` / custom drawing—confirming `XbaeMatrix` compiles and renders cleanly will be the main milestone.

---

## 4. Sylpheed — GTK 2

**Overview:** A fast, lightweight, C-based email client and newsreader. Unlike Claws Mail (which ported to GTK 3), Sylpheed remained on GTK 2 and is being dropped by major distributions.

### Dependency Tree
* **GUI & Graphics Stack:**
  * `gtk2` (`>= 2.24.0`) — *Replaced by `gtk-made-qt`*
  * `glib2` (`>= 2.37.3`) — *Required natively*
  * `cairo` (`>= 1.2.4`) & `pango` — *Required natively*
  * `gdk-pixbuf2` (`>= 2.22.0`) — *Inline image attachments & folder icons*
* **Mail, Crypto & Network Libraries (Non-GUI):**
  * `libsylph` (Internal/bundled mail handling engine)
  * `libgpgme` (PGP/MIME encryption and signing)
  * `libcurl` / `gnutls` / `openssl` (SSL/TLS and remote fetching)
  * `libenchant-2` (Spell checking via GtkSpell)
  * `libcompface` (X-Face email header decompression)

### Compatibility with `gtk-made-qt`
* **Strengths:**
  * Built almost entirely around standard GTK 2 layout and data widgets already implemented in `gtk-made-qt`: `GtkPaned` (3-pane mail view), `GtkTreeView` / `GtkTreeStore` (folder tree and message list), `GtkTextView` / `GtkTextBuffer` (message body and compose window with `GtkTextTag` coloring), `GtkMenuBar`, `GtkToolbar`, and `GtkNotebook`.
* **Watchouts:**
  * **Drag-and-Drop:** Moving emails between folders relies on `GtkTreeView` drag sources and destinations (drag sources are currently listed as missing in `gtk-made-qt`).
  * **Pixbuf & Inline Images:** Displaying image attachments and custom status icons in `GtkTreeView` (`GtkCellRendererPixbuf`) exercises `GdkPixbuf` heavily.
  * **Plugin/Spellcheck Dependencies:** Disable `GtkSpell` (`--disable-gtkspell`) on the first build pass so `gtkspell2` doesn't pull in real `libgtk-x11-2.0.so` at link time.

---

## Recommended `qtify` Packaging Sequence

1. **Asunder (`PKGBUILD` / build script):** Simplest GTK 2 codebase, minimal non-GTK dependencies (`cdparanoia`, `libcddb`), instant visual payoff.
2. **NEdit 5.7 (`PKGBUILD` / build script):** Zero external dependencies beyond `motif-on-qt` and `glibc`; iconic Unix tool to showcase Motif-on-Wayland.
3. **XmGrace (`PKGBUILD` / build script):** High impact for academic/scientific Linux users; tests bundled Motif widget subclasses (`XbaeMatrix`).
4. **Sylpheed (`PKGBUILD` / build script):** Comprehensive GTK 2 real-world stress test (build initially with `--disable-gtkspell` and `--disable-compface` to isolate the core UI).
