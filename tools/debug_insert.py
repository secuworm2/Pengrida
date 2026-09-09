import sys
from pathlib import Path

path = Path(sys.argv[1]) / "src" / "linux" / "linux-host-session.vala"
text = path.read_text(encoding="utf-8")

old1 = 'var process_name = yield helper.get_process_name (package, entrypoint.uid, cancellable);'
new1 = old1 + '\n\t\t\tstderr.printf ("DEBUG_SPAWN: process_name=[%s]\\n", process_name);'
assert text.count(old1) == 1, f"anchor1 count={text.count(old1)}"
text = text.replace(old1, new1)

old2 = 'if (colon != -1)\n\t\t\t\t\tpackage_name = package_name[:colon];'
new2 = old2 + '\n\n\t\t\t\tstderr.printf ("DEBUG_ZYMBIOTE: hello.process_name=[%s] package_name=[%s] has_key=%s\\n", hello.process_name, package_name, spawn_requests.has_key (package_name).to_string ());'
assert text.count(old2) == 1, f"anchor2 count={text.count(old2)}"
text = text.replace(old2, new2)

old3 = 'if (spawn_requests.unset (package_name, out spawn_request)) {\n\t\t\t\t\tspawn_request.resolve (hello.pid);\n\t\t\t\t\tneeds_resume = true;'
new3 = 'if (spawn_requests.unset (package_name, out spawn_request)) {\n\t\t\t\t\tstderr.printf ("DEBUG_ZYMBIOTE: resolving spawn_request with pid=%u\\n", hello.pid);\n\t\t\t\t\tspawn_request.resolve (hello.pid);\n\t\t\t\t\tstderr.printf ("DEBUG_ZYMBIOTE: resolved\\n");\n\t\t\t\t\tneeds_resume = true;'
assert text.count(old3) == 1, f"anchor3 count={text.count(old3)}"
text = text.replace(old3, new3)

old4 = 'pid = yield request.future.wait_async (cancellable);'
new4 = 'stderr.printf ("DEBUG_SPAWN: awaiting request.future...\\n");\n\t\t\t\t\tpid = yield request.future.wait_async (cancellable);\n\t\t\t\t\tstderr.printf ("DEBUG_SPAWN: got pid=%u\\n", pid);'
assert text.count(old4) == 1, f"anchor4 count={text.count(old4)}"
text = text.replace(old4, new4)

path.write_text(text, encoding="utf-8")
print("inserted debug prints into", path)
