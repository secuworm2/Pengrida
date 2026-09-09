import sys
from pathlib import Path

path = Path(sys.argv[1]) / "src" / "linux" / "linux-host-session.vala"
text = path.read_text(encoding="utf-8")

old1 = 'var process_name = yield helper.get_process_name (package, entrypoint.uid, cancellable);'
new1 = old1 + '\n\t\t\tstderr.printf ("DEBUG_SPAWN: process_name=[%s]\\n", process_name);'
assert text.count(old1) == 1, f"anchor1 count={text.count(old1)}"
text = text.replace(old1, new1)

old5 = 'protected override async void perform_resume (uint pid, Cancellable? cancellable) throws Error, IOError {\n\t\t\tif (spawn_gater != null && spawn_gater.try_resume (pid))\n\t\t\t\treturn;'
new5 = 'protected override async void perform_resume (uint pid, Cancellable? cancellable) throws Error, IOError {\n\t\t\tstderr.printf ("DEBUG_RESUME: perform_resume called for pid=%u\\n", pid);\n\t\t\tif (spawn_gater != null && spawn_gater.try_resume (pid)) {\n\t\t\t\tstderr.printf ("DEBUG_RESUME: handled by spawn_gater\\n");\n\t\t\t\treturn;\n\t\t\t}'
assert text.count(old5) == 1, f"anchor5 count={text.count(old5)}"
text = text.replace(old5, new5)

old6 = 'if (robo_launcher.try_resume (pid))\n\t\t\t\treturn;'
new6 = 'bool robo_handled = robo_launcher.try_resume (pid);\n\t\t\tstderr.printf ("DEBUG_RESUME: robo_launcher.try_resume=%s\\n", robo_handled.to_string ());\n\t\t\tif (robo_handled)\n\t\t\t\treturn;'
assert text.count(old6) == 1, f"anchor6 count={text.count(old6)}"
text = text.replace(old6, new6)

old7 = 'yield helper.resume (pid, cancellable);'
new7 = 'stderr.printf ("DEBUG_RESUME: falling through to helper.resume\\n");\n\t\t\tyield helper.resume (pid, cancellable);'
assert text.count(old7) == 1, f"anchor7 count={text.count(old7)}"
text = text.replace(old7, new7)

path.write_text(text, encoding="utf-8")
print("inserted debug prints into", path)
