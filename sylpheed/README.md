Sylpheed 3.7.0, the GTK 2 mail client, built from its unmodified source
against gtk-made-qt: it runs as a Qt application without GTK.

Notes on the recipes:

- The source is Debian's copy of the release tarball (the same file in
  Ubuntu); sylpheed.sraoss.jp has the original.
- Linked with `gtk-made-qt-env --shared`: Sylpheed's plugin library
  (libsylpheed-plugin) calls GTK too, and a static copy of the toolkit in
  the program and another in the library would be two toolkits.
- Built with OpenSSL (POP3/IMAP/SMTP over TLS) and without GPGME, GtkSpell
  and X-Face (compface), which keeps the dependencies to what every
  distribution has; `--disable-rpath` because the libraries go to the
  system library directory.
- The check starts Sylpheed headless in an empty home: it opens its first
  run dialog (where to create the mailbox) and quits.
- Needs gtk-made-qt d7f2d73 or newer (tree view column fields and row
  events, text anchors and tag positions, key bindings, the accel map,
  GtkStatusIcon, GdkPixbuf).

Tested (installed): the first run dialogs (mailbox location, account
wizard), an MH mailbox with messages (folder tree, message list with its
icon columns and sorting, message view with header, quote and link
colours, the separator line), the compose window with its ruler, compared
with the same version built against real GTK 2.
