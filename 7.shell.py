import os
import sys
import shlex
import subprocess

def run_command(command):
    tokens = shlex.split(command)

    if '>' in tokens:
        idx = tokens.index('>')
        cmd = tokens[:idx]
        outfile = tokens[idx+1]
        with open(outfile, 'w') as f:
            subprocess.run(cmd, stdout=f)
        return

    if '<' in tokens:
        idx = tokens.index('<')
        cmd = tokens[:idx]
        infile = tokens[idx+1]
        with open(infile, 'r') as f:
            subprocess.run(cmd, stdin=f)
        return

    if '|' in tokens:
        idx = tokens.index('|')
        cmd1 = tokens[:idx]
        cmd2 = tokens[idx+1:]
        p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        output = p2.communicate()[0]
        print(output.decode())
        return

    try:
        result = subprocess.run(tokens, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except FileNotFoundError:
        print(f"Command not found: {tokens[0]}")

def main():
    print("Simple Python Shell (type 'exit' to quit)")
    while True:
        try:
            command = input("shell> ")
            if command.strip() == "exit":
                break
            if command.strip() == "":
                continue
            run_command(command)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            break

if __name__ == "__main__":
    main()
