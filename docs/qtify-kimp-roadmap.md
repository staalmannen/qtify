# Qtify Packaging Roadmap: From Legacy Motif/GTK2 to Modern "KIMP" (GIMP)

This roadmap outlines a phased strategy for populating the `qtify` repository using **`gtk-made-qt`** and **`qtmotifextension`**. By progressing from self-contained legacy tools to complex modern applications, each phase validates specific shim layers while delivering immediate value to distributions trying to drop legacy toolkits (such as GTK 2 and Motif/X11).

---

## Priority Overview Matrix

| Phase | Target Tier | Representative Apps | Toolkit Layer | Primary Value Proposition | Key Technical Hurdles |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | Quick Legacy Wins | **Asunder**, **Leafpad**, **Galculator**, **NEdit** | GTK 2 / Motif | Immediate proof-of-concept; zero-patch builds | Minimal; custom Xlib text drawing in NEdit |
| **Phase 2** | High-Value Legacy Desktop | **Sylpheed**, **Xournal**, **DDD**, **XmGrace** | GTK 2 / Motif | Eliminates distro GTK 2 & X11 holdouts | Bundled widgets (`Xbae`), Cairo canvas, `GtkSpell` |
| **Phase 3** | Modern GTK 3/4 Stepping Stones | **Mousepad**, **Transmission**, **Audacious (GTK)** | GTK 3 / GTK 4 | Stresses `GApplication`, `GMenu`, & subclassing | `GtkSourceView`, CSS styling approximations |
| **Phase 4** | Legacy GIMP ("KIMP 2.10") | **GIMP 2.10** | GTK 2 + GEGL/Babl | Major milestone: full creative suite on Qt 6 | Heavy `GdkPixbuf`, custom docks, tablet/XInput |
| **Phase 5** | Modern "KIMP 3.0" | **GIMP 3.0** | GTK 3 + GEGL/Babl | Ultimate showcase: modern GIMP unmodified on Qt 6 | GTK 3 CSS engine, modern `GdkMonitor`/Wayland APIs |

---

## Phase 1: Quick Legacy Wins (Immediate Proof-of-Concept)
**Goal:** Establish working `PKGBUILD` templates and automated headless screenshot tests (`GTKQT_SCRIPT` / `MOTIFQT_SCRIPT`) for simple, single-window C applications.

* **Asunder (GTK 2):** Uses standard `GtkDialog`, `GtkTreeView`, `GtkProgressBar`, and `GtkEntry`. Zero third-party GTK wrapper dependencies.
* **Galculator (GTK 2):** Tests `GtkTable` / `GtkGrid` button layouts, `GtkMenuBar`, and basic widget styling.
* **NEdit / XNEdit (Motif):** Validates `XmText`, `XmRowColumn` menus, `XmFileSelectionBox`, and `XmDrawingArea` custom text rendering.
* **DDD — Data Display Debugger (Motif):** High practical appeal for C/C++ developers on Wayland who want to avoid XWayland scaling artifacts.

---

## Phase 2: High-Value Legacy Desktop Holdouts
**Goal:** Target larger, multi-pane applications that are the primary reason distributions like Arch, KaOS, Fedora, and Debian still maintain legacy `gtk2` or `openmotif` packages.

* **Sylpheed (GTK 2):** A full-featured C email client. Exercises complex `GtkTreeStore` folder hierarchies, multi-pane `GtkPaned` layouts, and `GtkTextView`. *(Tip: Build with `--disable-gtkspell` first).*
* **Xournal (GTK 2):** Classic PDF annotator. Stress-tests `GtkDrawingArea` with Cairo rendering, custom toolbars, and pointer event translation.
* **XmGrace (Motif):** Ubiquitous scientific plotting tool. Tests `XmForm` constraint geometry and requires checking compatibility with its internal `XbaeMatrix` spreadsheet widget.

---

## Phase 3: Modern GTK 3 & GTK 4 Stepping Stones
**Goal:** Validate modern GLib/GIO integration (`GtkApplication`, `GMenuModel`, `GActionMap`, and `GtkBuilder` XML) before tackling GIMP's massive codebase.

* **Transmission GTK (GTK 3 & GTK 4):** Clean, idiomatic C codebase. Ideal for testing `GtkHeaderBar`, `GtkStack`, `GtkApplicationWindow`, and `GMenu` integration with Qt's native menu bars.
* **Mousepad (GTK 3):** Tests `GtkSourceView` (a complex third-party `GtkTextView` subclass) and modern dialog conventions.
* **Audacious — GTK UI (GTK 2/3):** Since Audacious also ships a native Qt 6 interface, compiling its GTK interface via `gtk-made-qt` provides an exact side-by-side visual and functional benchmark.

---

## Phase 4: The "KIMP 2.10" Milestone (GIMP 2.10 on GTK 2)
**Goal:** Recompile GIMP 2.10 against Qt 6 without modifying GIMP's upstream C source code. Targeting 2.10 first avoids GTK 3 CSS engine dependencies while exercising the core `libgimpwidgets` stack.
Historical KIMP from 1998: https://krita.org/en/posts/2009/the-history-of-kimageshop-krayon-krita/

### Critical Subsystem Checklist for GIMP 2.10
1. **`GdkPixbuf` Completeness:** GIMP relies heavily on `GdkPixbuf` for tool icons, brushes, patterns, cursors, and splash screens (scaling, compositing, subpixbufs, and PNG/XPM loaders).
2. **Custom Widget Subclassing (`G_DEFINE_TYPE`):** `libgimpwidgets` defines dozens of custom subclasses (`GimpColorButton`, `GimpScaleEntry`, `GimpRuler`, `GimpPreviewArea`).
3. **Dockable Dialogs & Panes:** GIMP's multi-window and single-window dockable tab system (`GimpDockbook`, `GimpPanedBox`) relies on drag-and-drop (`gtk_drag_source_set` / `gtk_drag_dest_set`) and `GtkNotebook` tab reordering.
4. **Canvas & Input Devices (`GimpDisplayShell`):** Uses Cairo inside `GtkDrawingArea` alongside `GdkDevice` queries for stylus pressure and extended input devices.

---

## Phase 5: Modern "KIMP 3.0" (GIMP 3.0 on GTK 3)
**Goal:** Build GIMP 3.0 unmodified against Qt 6.

### Additional Requirements Beyond GIMP 2.10
* **GTK 3 CSS Styling & Layout:** GIMP 3 relies heavily on `GtkCssProvider` for dark-theme toolbars, compact dock spacing, and custom widget states. Expanding `gtk-made-qt`'s CSS parser to map basic padding, border, and background properties to Qt Style Sheets (QSS) or `QProxyStyle` will be essential for usability.
* **Modern GDK APIs:** `GdkDisplay`, `GdkMonitor`, and `GdkSeat` queries used for multi-monitor color management and high-DPI canvas scaling.
* **Multi-Item Selection & Modern Dialogs:** `GtkFileChooserNative`, `GtkPopover`, and updated `GtkTreeView` multi-selection behaviors.

---

## Recommended Execution Order for `qtify`
1. **Commit `asunder-qt` and `nedit-qt` `PKGBUILD`s** as clean reference templates in `qtify`.
2. **Add CI screenshot verification** using `GTKQT_SCREENSHOT` and `MOTIFQT_SCREENSHOT` to automatically generate visual proof for the repository README.
3. **Tackle `sylpheed-qt` and `transmission-qt-shim`** to harden GTK 2 and GTK 3/4 coverage respectively.
4. **Attempt a headless build of `gimp-2.10`** (`--without-webkit` / minimal plugins) to generate a concrete list of missing `GdkPixbuf` and `GtkWidget` symbols to implement next.
