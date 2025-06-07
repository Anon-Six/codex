# INTEGRA Electron Wrapper

This directory contains a minimal Electron wrapper for the INTEGRA frontend.
Run `npm install` and `npm start` to launch the desktop application.

Run these commands from inside the `integra_electron` folder of the repository:
```bash
cd /path/to/codex/integra_electron
npm install
npm start
```

To build a Windows installer (requires Node.js and Wine on Linux), run:

```bash
npm run build
```

The generated installer will appear in the `dist/` directory.
