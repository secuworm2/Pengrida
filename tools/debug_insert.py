import sys
from pathlib import Path

path = Path(sys.argv[1]) / "src" / "linux" / "linux-host-session.vala"
text = path.read_text(encoding="utf-8")

old1 = '\t\t\tvar linjector = (Linjector) injector;\n#if HAVE_EMBEDDED_ASSETS\n\t\t\tid = yield linjector.inject_library_resource (pid, agent, entrypoint, parameters, features, cancellable);'
new1 = '\t\t\tvar linjector = (Linjector) injector;\n\t\t\tstderr.printf ("DEBUG_ATTACH: perform_attach_to entered for pid=%u entrypoint=[%s]\\n", pid, entrypoint);\n#if HAVE_EMBEDDED_ASSETS\n\t\t\tid = yield linjector.inject_library_resource (pid, agent, entrypoint, parameters, features, cancellable);\n\t\t\tstderr.printf ("DEBUG_ATTACH: inject_library_resource returned id=%u\\n", id);'
assert text.count(old1) == 1, f"anchor1 count={text.count(old1)}"
text = text.replace(old1, new1)

old2 = 'IOStream stream = yield linjector.request_control_channel (id, cancellable);\n\t\t\tstream_request.resolve (stream);'
new2 = 'stderr.printf ("DEBUG_ATTACH: requesting control channel for id=%u\\n", id);\n\t\t\tIOStream stream = yield linjector.request_control_channel (id, cancellable);\n\t\t\tstderr.printf ("DEBUG_ATTACH: got control channel\\n");\n\t\t\tstream_request.resolve (stream);'
assert text.count(old2) == 1, f"anchor2 count={text.count(old2)}"
text = text.replace(old2, new2)

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

old8 = 'public bool try_resume (uint pid) {\n\t\t\tZymbioteConnection? connection;\n\t\t\tif (!zymbiote_connections.unset (pid, out connection))\n\t\t\t\treturn false;'
new8 = 'public bool try_resume (uint pid) {\n\t\t\tZymbioteConnection? connection;\n\t\t\tif (!zymbiote_connections.unset (pid, out connection)) {\n\t\t\t\tstderr.printf ("DEBUG_ROBO: try_resume(%u) - no zymbiote connection found\\n", pid);\n\t\t\t\treturn false;\n\t\t\t}\n\t\t\tstderr.printf ("DEBUG_ROBO: try_resume(%u) - found connection, resuming\\n", pid);'
assert text.count(old8) == 1, f"anchor8 count={text.count(old8)}"
text = text.replace(old8, new8)

path.write_text(text, encoding="utf-8")
print("inserted debug prints into", path)
