#!/usr/bin/env bash
# Does not overwrite previous launchers, tools or menu entries.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
[ -f "$HERE/phantom_spine_live_v0_2_0.py" ] && [ -f "$HERE/index.html" ] || { echo '[ERROR] Incomplete PHANTOM SPINE Live package' >&2; exit 2; }
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
BIN="$HOME/.local/bin/phantom-spine-live-v020"
if [ ! -e "$BIN" ] && [ ! -L "$BIN" ]; then
  cat > "$BIN" <<EOF
#!/usr/bin/env bash
exec /bin/bash "$HERE/START_PHANTOM_SPINE_LIVE.sh" "\$@"
EOF
  chmod 755 "$BIN"
  echo '[PASS] Short command created: phantom-spine-live-v020'
else
  echo '[NOTICE] Short command already exists; preserved (use START_PHANTOM_SPINE_LIVE.sh directly if it points elsewhere).'
fi
DESKTOP_DIR=""
if command -v xdg-user-dir >/dev/null 2>&1; then DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || true)"; fi
if [ -z "$DESKTOP_DIR" ] || [ "$DESKTOP_DIR" = "$HOME" ]; then DESKTOP_DIR="$HOME/Desktop"; fi
mkdir -p "$DESKTOP_DIR"
MENU="$HOME/.local/share/applications/phantom-spine-live-signal-v020.desktop"
DESKTOP="$DESKTOP_DIR/Phantom-Spine-Live-v020.desktop"
HUNT="$DESKTOP_DIR/Phantom-Spine-Real-Hunt-v020.desktop"
if [ ! -e "$MENU" ] && [ ! -L "$MENU" ]; then
  cat > "$MENU" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PHANTOM SPINE Live Signal v0.2.0
Comment=Public-source intelligence recipes and live tool operations
Exec=/bin/bash "$HERE/OPEN_LIVE_GUIDE.sh"
Icon=$HERE/assets/phantom-spine-emblem.svg
Terminal=false
Categories=Development;Utility;
EOF
  chmod 755 "$MENU"
  echo '[PASS] Application-menu shortcut created.'
else
  echo '[NOTICE] App-menu shortcut exists; preserved.'
fi
if [ ! -e "$DESKTOP" ] && [ ! -L "$DESKTOP" ]; then
  cp -- "$MENU" "$DESKTOP"
  chmod 755 "$DESKTOP"
  echo '[PASS] Recipe-page desktop shortcut created.'
else
  echo '[NOTICE] Recipe-page desktop shortcut exists; preserved.'
fi
if [ ! -e "$HUNT" ] && [ ! -L "$HUNT" ]; then
  cat > "$HUNT" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=PHANTOM SPINE v0.2.0 Real Hunt (example.com)
Comment=Live public DNS research of example.com; sends domain to public providers
Exec=/bin/bash "$HERE/START_LIVE_HUNT.sh"
Icon=$HERE/assets/phantom-spine-emblem.svg
Terminal=true
Categories=Development;Utility;
EOF
  chmod 755 "$HUNT"
  echo '[PASS] Separate real-hunt terminal desktop shortcut created.'
else
  echo '[NOTICE] Real-hunt desktop shortcut already exists; preserved.'
fi
for file in "$DESKTOP" "$HUNT"; do
  if command -v gio >/dev/null 2>&1; then gio set "$file" metadata::trusted true 2>/dev/null || true; fi
done
printf '%s\n' '[DONE] PHANTOM SPINE Live shortcuts installed independently. Older tools were not changed.'
