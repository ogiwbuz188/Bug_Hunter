import os
import sys
import html
import argparse
import platform
import clang.cindex

class AdvancedCBugHunter:

    def __init__(self, file_path):
        self.file_path = file_path
        self.index = clang.cindex.Index.create()
        
        self.file_path = os.path.abspath(file_path)
        if not os.path.exists(self.file_path):
            print(f"❌ Error: Target file '{self.file_path}' not found.)")
            return
                
        try:
            self.translation_unit = self.index.parse(self.file_path, args=['-Xclang', '-fsyntax-only'])
        except Exception as e:
            print(f"❌ Clang Parsing Error on {self.file_path}: {e}")
            self.translation_unit = None

        self.findings = []
        self.scope_stack = [{}]

    def analyze(self):
        """Starts the compilation traversal and analytical phases."""
        if not self.translation_unit:
            return
        root_node = self.translation_unit.cursor
        self._traverse_scope(root_node)
        self._flush_remaining_scopes()
                
    def _traverse_scope(self, current_node):
        """Recursively parses individual scopes and monitors syntax entities."""
        if not current_node.location.file or current_node.location.file.name != self.file_path:
                return
                        
        is_new_scope = (current_node.kind == clang.cindex.CursorKind.COMPOUND_STMT)
        if is_new_scope:
            self.scope_stack.append({})
                            
        # 1.POINTER SCOPE TRACKING FOR POINTER LEAKS
        if current_node.kind == clang.cindex.CursorKind.VAR_DECL:
            var_name = current_node.spelling
            if self._has_child_call(current_node, "malloc"):
                self.scope_stack[-1][var_name] = current_node.location.line

        if current_node.kind == clang.cindex.CursorKind.CALL_EXPR and current_node.spelling == "free":
             freed_var = self._get_first_argument_name(current_node)

             if freed_var:
                self._remove_pointer_from_tracking(freed_var)

        # 2. INTEGER OVERFLOW DETECTION
        if current_node.kind == clang.cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR:
            if self._has_binary_operator_child(current_node):
                self.findings.append({
                    "type": "Security/Integer Overflow",
                    "severity": "CRITICAL",
                    "line": current_node.location.line,
                    "msg": f"Unsanitized arithemetic expression inside an array subscript. Risk of Integer Overflow/Underflow exploitation."
                   })

        for child in current_node.get_children():
                self._traverse_scope(child)

        if is_new_scope:
            popped_scope = self.scope_stack.pop()
            for var_name, line in popped_scope.items():
                self.findings.append({
                    "type": "Resource Management (Memory Leak)",
                    "severity": "HIGH",
                    "line": line,
                    "msg": f"Pointer allocation '{var_name}' lost context scope without recieving a mandatory 'free()' call."
                  })

    def _has_child_call(self,node, function_name):
        if node.kind == clang.cindex.CursorKind.CALL_EXPR and node.spelling == function_name:
            return True
        for child in node.get_children():
            if self._has_child_call(child, function_name):
                return True
        return False

    def _get_first_argument_name(self, node):
        args = [child for child in node.get_children()
            if child.kind != clang.cindex.CursorKind.UNEXPOSED_EXPR]
        if args and args[0].kind ==clang.cindex.CursorKind.DECL_REF_EXPR:
            return args[0].spelling
        for child in node.get_children():
            res = self._get_first_argument_name(child)
            if res: return res
        return None

    def _remove_pointer_from_tracking(self, var_name):
        for scope in reversed(self.scope_stack):
            if var_name in scope:
                del scope[var_name]
                return
                                    
    def _flush_remaining_scopes(self):
        while self.scope_stack:
            popped = self.scope_stack.pop()
            for var_name, line in popped.items():
                self.findings.append({
                    "type": "Resource Management (Global/File Leak)",
                    "severity": "HIGH",
                    "line": line,
                    "msg": f"Pointer allocation '{var_name}' was never explicitly freed."
                })

    def generate_markdown_report(self, output_path="report.md"):
        """Compiles aggregated formatted Markdown logs across all scanned files."""
        with open(output_path, "w") as f:
            f.write(f"# Static Analysis Security Report\n")
            f.write(f"**Target Analysis File:** `{self.file_path}`\n\n")
            f.write(f"## Executive Vulnerability Summary\n")
            if not self.findings:
                f.write("💫 **No security or stuctural defects identified during evaluation.**\n")
                return

            f.write("| Severity | Vulnerability Traget Category | Line Number | Diagnostic Threat Explanation |\n")  
            f.write("|----------|-------------------------------|-------------|-------------------------------|\n")
            for issue in self.findings:
                f.write(f"| **{issue['severity']}** | `{issue['type']}` | {issue['line']} | {issue['msg']} |\n")
        print(f"📁 Global Markdown report generated at {output_path}")

    def generate_html_report(self, output_path="report.html"):
        """Compiles clean, interactive UI code summary web view dashboard."""
        try:
            with open(self.file_path, "r") as src_file:
                raw_lines = src_file.readlines()
        except OSError:
            raw_lines = []

        html_content = f"""<!DOCTYPE html>
<html>  
<head>
    <title>Bug Hunter AST Report</title>
    <style>
        body{{ font-family: "Georgia", "Times New Roman",serif;
                margin: 0;
                padding: 40px;
                background-color: #1c1917;
                color: #f5f5f4;
                line-height: 1.6;
        }}
        .container{{
            max-width: 900px;
            margin: 0 auto;
        }}
        h1{{
            font-family: "Playfair Display", "Georgia", serif;
            font-weight: 700;
            color: #d6c4a5;
            border-bottom: 1px dashed #78716c;
            padding-bottom: 15px;
            margin-bottom: 5px;
            font-size: 2.5rem;
            letter-spacing: -0.5px;
        }}
        h2{{
            font-family: "georgia", serif;
            font-weight: 400;
            font-style: italic;
            color: #a8a29e;
            font-size: 1.2rem;
            margin-top: 0;
            margin-bottom: 40px;
        }}
        .card {{ 
            background-color: #2e2a24;
            border: 1px solid #44403c;
            padding: 25px;  
            margin-bottom: 20px;
            border-radius: 4px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            position: relative;
        }}
        .card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 4px;
            }}
        .CRITICAL::before {{ background-color: #991b1b; }}
        .HIGH::before {{ background-color: #c2410c; }}
        
        .badge {{ 
            display: inline-block;
            padding: 3px 9px;
            font-family: monospace;
            font-weight: bold;
            border-radius: 2px;
            font-size: 11px;
            color: #1c1917;
            margin-right: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-CRITICAL {{ background-color: #fca5a5; color: #7f1d1d; }}
        .badge-HIGH {{ background-color: #fed7aa; color: #7c2d12; }}

        .vuln-tiltle {{
            font-size: 1.15rem;
            color: #e7e5e4;
            font-family: "Georgia", serif;
        }}
        .file-meta {{
            font-size: 0.9rem;
            color: #a8a29e;
            margin-top: 5px;
            font-family: monospace;
        }}
        p {{
            color: #d6d3d1;
            margin: 15px 0 0 0;
            font-size: 1rem;
        }}
        .clean-state {{
            border: 1px dashed #78716c;
            padding: 30px;
            text-align: center;
            color: #d6c4a5;
            font-style: italic;
            font-size: 1.1rem;
            background-color: #2301b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>The Bug Hunter Archive</h1>
        <h2>Evaluation Portfolio &bull;Static Analysis Record</h2>
"""
        if not self.findings:
            html_content += "<div class='clean-state'>💫 Omnia bene: No structural pointer anomalies or arithmetic exceptions identified.</div>"
        else:
            for issue in self.findings:
                html_content += f"""
                <div class="card {issue['severity']}">
                    <div>
                        <span class="badge badge-{issue['severity']}">{issue['severity']}</span>
                    <span class="vuln-title"><strong>{issue['type']}</strong></span>
                    </div>                                        
                    <div class="file-meta">Location: file://{html.escape(issue['file'])} &bull; Line{issue['line']}</div>
                    <p>{html.escape(issue['msg'])}</p>
                </div>
                """

        html_content += "</div></body>\n</html>"
    

        with open(output_path, "w") as f:
            f.write(html_content)
        print(f"📁 HTML UI dashboard generated at {output_path}")

if __name__ == "__main__":
    current_os = platform.system()
    if current_os == "Windows":
        clang.cindex.Config.set_library_path("C:/Program Files/LLVM/bin")
    elif current_os == "Darwin":
        clang.cindex.Config.set_library_path("/Library/Developer/CommandLineTools/usr/lib")
    #Setup Command-Line Arguments Parsing
    parser = argparse.ArgumentParser(description=" C/C++ Static Analyzer")
    parser.add_argument("target", help="Path to a single C/C++ file OR a complete directory folder profile")
    parser.add_argument("--md", default="report.md", help="Output path for the Markdown report.")
    parser.add_argument("--html", default="report.html", help="Output path for the HTML dashboard")
    args = parser.parse_args()

    if os.path.isdir(args.target):
        print(f"📁 Directory path specified.Crawling folder'{args.target}' recusively...")
        files_to_analyze = []
        for root, _, files in os.walk(args.target):
            for filename in files:
                if filename.lower().endswith((".c", ".cc", ".cpp", ".cxx", ".h", ".hpp")):
                    files_to_analyze.append(os.path.join(root, filename))
                else:
                    files_to_analyze.append(args.target)
                    print(f"Parsing and processing {len(files_to_analyze)}file(s).Evaluating AST Tracks...\n")

                    global_findings=[]
                    for file_path in files_to_analyze:
                        print(f"Auditing Node:{file_path}")
                        hunter=AdvancedCBugHunter(file_path)
                        hunter.analyze()
                        global_findings.extend(hunter.findings)

                        print(f"\nProcessing completed.Writing analytic files...")
                        hunter.generate_markdown_report(global_findings,args.md)
                        hunter.generate_html_report(args.html)
