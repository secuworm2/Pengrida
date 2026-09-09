import sys
from pathlib import Path

core = Path(sys.argv[1])

# --- lib/agent/agent.vala: log the agent_ctrlfd-based transport URI ---
path1 = core / "lib" / "agent" / "agent.vala"
text1 = path1.read_text(encoding="utf-8")

old1 = '\t\t\t\t\tagent_parameters_with_transport_uri = "socket:%d%s".printf (agent_ctrlfd, agent_parameters);\n\t\t\t\t\tagent_parameters = agent_parameters_with_transport_uri;'
new1 = '\t\t\t\t\tagent_parameters_with_transport_uri = "socket:%d%s".printf (agent_ctrlfd, agent_parameters);\n\t\t\t\t\tGLib.info ("DEBUG_AGENT: agent_ctrlfd=%d transport=[%s]", agent_ctrlfd, agent_parameters_with_transport_uri);\n\t\t\t\t\tagent_parameters = agent_parameters_with_transport_uri;'
assert text1.count(old1) == 1, f"anchor1 count={text1.count(old1)}"
text1 = text1.replace(old1, new1)

path1.write_text(text1, encoding="utf-8")
print("inserted debug prints into", path1)
