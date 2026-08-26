# Bug_Hunter
A high-performance static analysis tool written in C/C++ to detect memory leaks, buffer overflows, and concurrency bugs in source code.


### Key Technical Systems
1. **Dynamic Cross-OS Linker:** Automatically maps system platform dependencies across Windows binaries, macOS Developer Tools, and Linux compiler loops.
2. **Deterministic Scoped Pointer Stack:** Simulates operating system variable context boundaries using an internal context frame stack tracker (`O(1)` operations) to catch complex, multi-layered pointer memory leaks.
3. **AST Integer Rule Interceptor:** Intercepts subscript and array bounds expressions to catch algebraic integer bounds vulnerability exploits prior to compilation.

---

## ⚡ Setup & Dependency Management

### 1. Engine Core Compiler Installation
The Python bindings interface directly with system compilation infrastructures:
* **Ubuntu / Debian Linux:** `sudo apt-get update && sudo apt-get install -y libclang-dev llvm`
* **Windows 11:** Install LLVM win64 setup and ensure you check **"Add LLVM to system PATH"** during installation.

### 2. Dependency Map
```bash
pip install clang
```

---

## 🚀 Execution & Command-Line Utility Map

Run the analyzer engine against any single module code asset or an entire source program tree directory:

```bash
# Evaluate a single source block
python script.py target_code.c

# Recursively analyze an entire multi-file project folder architecture
python script.py path/to/c_source_directory/
```

### Output Artefacts
* `report.md`: Structured markdown metrics table, perfectly mapped for integration with Github pipelines.
* `report.html`: An interactive, **visual safety dashboard** logging critical boundary flaws.

---

## 🛠️ Automated Cloud Engineering (DevOps)

This workspace integrates a continuous continuous security auditing pipeline via a **GitHub Action file** located in `.github/workflows/`. Every direct source revision push maps, compiles dependencies, runs python engine validation cycles, and archives structural reports directly as pipeline build artifacts.

