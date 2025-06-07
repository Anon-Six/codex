#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
import platform

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(REPO_ROOT)


def has_cmd(cmd):
    return shutil.which(cmd) is not None


def run(cmd, **kwargs):
    print(cmd)
    subprocess.check_call(cmd, shell=True, **kwargs)


def ensure_windows():
    if not has_cmd('python') and not has_cmd('py'):
        if has_cmd('winget'):
            run('winget install --id Python.Python.3 -e --silent')
    if not has_cmd('node'):
        if has_cmd('winget'):
            run('winget install --id OpenJS.NodeJS -e --silent')
    if not has_cmd('npm'):
        if has_cmd('winget'):
            run('winget install --id OpenJS.NodeJS -e --silent')
    if not has_cmd('ollama'):
        if has_cmd('winget'):
            run('winget install --id Ollama.Ollama -e --silent')


def ensure_linux():
    pkg = None
    if has_cmd('apt-get'):
        pkg = 'apt-get'
    elif has_cmd('dnf'):
        pkg = 'dnf'
    if pkg:
        if not has_cmd('python3'):
            run(f'sudo {pkg} install -y python3 python3-venv python3-pip')
        if not has_cmd('node'):
            run(f'sudo {pkg} install -y nodejs npm')
    if not has_cmd('ollama') and has_cmd('curl'):
        run('curl -fsSL https://ollama.com/install.sh | sh')


def setup_backend(python_exe):
    run(f'{python_exe} -m venv integra_backend/.venv')
    if platform.system() == 'Windows':
        pip_path = os.path.join('integra_backend', '.venv', 'Scripts', 'pip')
        py_path = os.path.join('integra_backend', '.venv', 'Scripts', 'python')
    else:
        pip_path = os.path.join('integra_backend', '.venv', 'bin', 'pip')
        py_path = os.path.join('integra_backend', '.venv', 'bin', 'python')
    run(f'{pip_path} install -r integra_backend/requirements.txt')
    if not os.path.exists('integra_backend/.env'):
        shutil.copy('integra_backend/.env.example', 'integra_backend/.env')
    return py_path


def ensure_model():
    try:
        out = subprocess.check_output('ollama list', shell=True, text=True)
        if 'gemma:7b' not in out:
            run('ollama pull gemma:7b')
    except Exception:
        pass


def setup_electron():
    run('npm install --silent', cwd='integra_electron')


def main():
    system = platform.system()
    if system == 'Windows':
        ensure_windows()
        python_exe = shutil.which('python') or shutil.which('py')
    else:
        ensure_linux()
        python_exe = shutil.which('python3') or shutil.which('python')
    if not python_exe:
        print('Python is required but not found.')
        sys.exit(1)
    backend_python = setup_backend(python_exe)
    ensure_model()
    setup_electron()
    print('\nInstallation finished. Launching services...')
    try:
        subprocess.Popen('ollama serve', shell=True)
    except Exception:
        pass
    if system == 'Windows':
        act = os.path.join('integra_backend', '.venv', 'Scripts', 'Activate.ps1')
        backend_cmd = f'powershell -NoExit -ExecutionPolicy Bypass -Command "& {act}; python integra_backend\\app.py"'
        subprocess.Popen(backend_cmd, shell=True)
        subprocess.Popen('npm start', cwd='integra_electron', shell=True)
    else:
        subprocess.Popen(f'source integra_backend/.venv/bin/activate && python integra_backend/app.py', shell=True, executable='/bin/bash')
        subprocess.Popen('npm start', cwd='integra_electron', shell=True)
    print('Backend and Electron started.')


if __name__ == '__main__':
    main()
