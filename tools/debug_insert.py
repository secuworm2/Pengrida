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

path.write_text(text, encoding="utf-8")
print("inserted debug prints into", path)
