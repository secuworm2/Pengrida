import sys
from pathlib import Path

core = Path(sys.argv[1])

# --- src/linux/frida-helper-backend.vala: instrument monitor()'s message loop ---
path2 = core / "src" / "linux" / "frida-helper-backend.vala"
text2 = path2.read_text(encoding="utf-8")

old1 = '\t\t\t\t\tyield input.read_all_async ((uint8[]) &raw_type, io_priority, io_cancellable, out n);\n\t\t\t\t\tif (n == 0)\n\t\t\t\t\t\tbreak;\n\t\t\t\t\tvar type = (HelperMessageType) raw_type;'
new1 = '\t\t\t\t\tyield input.read_all_async ((uint8[]) &raw_type, io_priority, io_cancellable, out n);\n\t\t\t\t\tstderr.printf ("DEBUG_MONITOR: read n=%zu raw_type=%u\\n", n, (uint) raw_type);\n\t\t\t\t\tif (n == 0) {\n\t\t\t\t\t\tstderr.printf ("DEBUG_MONITOR: n==0, breaking (EOF/closed)\\n");\n\t\t\t\t\t\tbreak;\n\t\t\t\t\t}\n\t\t\t\t\tvar type = (HelperMessageType) raw_type;'
assert text2.count(old1) == 1, f"anchor1 count={text2.count(old1)}"
text2 = text2.replace(old1, new1)

old2 = '\t\t\t\ton_stop (unload_policy);\n\t\t\t} catch (GLib.Error e) {\n\t\t\t\tif (!(e is IOError.CANCELLED))\n\t\t\t\t\ton_stop (IMMEDIATE);\n\t\t\t} finally {\n\t\t\t\tif (start_request != null) {'
new2 = '\t\t\t\tstderr.printf ("DEBUG_MONITOR: loop done, calling on_stop(%d)\\n", (int) unload_policy);\n\t\t\t\ton_stop (unload_policy);\n\t\t\t} catch (GLib.Error e) {\n\t\t\t\tstderr.printf ("DEBUG_MONITOR: caught GLib.Error: %s\\n", e.message);\n\t\t\t\tif (!(e is IOError.CANCELLED))\n\t\t\t\t\ton_stop (IMMEDIATE);\n\t\t\t} finally {\n\t\t\t\tstderr.printf ("DEBUG_MONITOR: finally, start_request!=null: %s\\n", (start_request != null).to_string ());\n\t\t\t\tif (start_request != null) {'
assert text2.count(old2) == 1, f"anchor2 count={text2.count(old2)}"
text2 = text2.replace(old2, new2)

path2.write_text(text2, encoding="utf-8")
print("inserted debug prints into", path2)
