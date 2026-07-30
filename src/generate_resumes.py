#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from PIL import Image

# Base Directory Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
BUILD_DIR = os.path.join(BASE_DIR, "build")
TEX_DIR = os.path.join(BUILD_DIR, "tex")
PDF_DIR = os.path.join(BUILD_DIR, "pdf")
PREVIEW_DIR = os.path.join(BUILD_DIR, "previews")

sys.path.insert(0, os.path.join(BASE_DIR, "src"))
from lint_schema import lint_resume_bank

def ensure_dirs():
    for d in [BUILD_DIR, TEX_DIR, PDF_DIR, PREVIEW_DIR]:
        os.makedirs(d, exist_ok=True)

def escape_latex(text):
    """Escapes raw characters that break LaTeX unless already formatted."""
    replacements = [
        ('&', r'\&'),
        ('%', r'\%'),
        ('#', r'\#'),
        ('$', r'\$'),
        ('_', r'\_'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for char, escaped in replacements:
        text = text.replace(f'\\{char}', f'__ESC_{char}__')
        text = text.replace(char, escaped)
        text = text.replace(f'__ESC_{char}__', f'\\{char}')
    return text

def build_latex_content(data, config_key):
    config = data["configurations"][config_key]
    header = data["header"]
    edu_list = data["education"]
    exp_bank = data["experience_bank"]
    proj_bank = data["project_bank"]
    skills = data["skills"]

    tex = []
    tex.append(r"\documentclass[letterpaper,11pt]{article}")
    tex.append(r"")
    tex.append(r"\usepackage{latexsym}")
    tex.append(r"\usepackage[empty]{fullpage}")
    tex.append(r"\usepackage{titlesec}")
    tex.append(r"\usepackage{marvosym}")
    tex.append(r"\usepackage[usenames,dvipsnames]{color}")
    tex.append(r"\usepackage{verbatim}")
    tex.append(r"\usepackage{enumitem}")
    tex.append(r"\usepackage[hidelinks]{hyperref}")
    tex.append(r"\usepackage{fancyhdr}")
    tex.append(r"\usepackage[english]{babel}")
    tex.append(r"\usepackage{tabularx}")
    tex.append(r"\input{glyphtounicode}")
    tex.append(r"")
    tex.append(r"\pagestyle{fancy}")
    tex.append(r"\fancyhf{}")
    tex.append(r"\fancyfoot{}")
    tex.append(r"\renewcommand{\headrulewidth}{0pt}")
    tex.append(r"\renewcommand{\footrulewidth}{0pt}")
    tex.append(r"")
    tex.append(r"% Adjust margins")
    tex.append(r"\addtolength{\oddsidemargin}{-0.5in}")
    tex.append(r"\addtolength{\evensidemargin}{-0.5in}")
    tex.append(r"\addtolength{\textwidth}{1in}")
    tex.append(r"\addtolength{\topmargin}{-.5in}")
    tex.append(r"\addtolength{\textheight}{1.0in}")
    tex.append(r"")
    tex.append(r"\urlstyle{same}")
    tex.append(r"\raggedbottom")
    tex.append(r"\raggedright")
    tex.append(r"\setlength{\tabcolsep}{0in}")
    tex.append(r"")
    tex.append(r"% Sections formatting")
    tex.append(r"\titleformat{\section}{")
    tex.append(r"  \vspace{-6pt}\scshape\raggedright\large")
    tex.append(r"}{}{0em}{}[\color{black}\titlerule \vspace{-7pt}]")
    tex.append(r"")
    tex.append(r"\pdfgentounicode=1")
    tex.append(r"")
    tex.append(r"% Custom commands")
    tex.append(r"\newcommand{\resumeItem}[1]{")
    tex.append(r"  \item\small{")
    tex.append(r"    {#1 \vspace{-3.5pt}}")
    tex.append(r"  }")
    tex.append(r"}")
    tex.append(r"")
    tex.append(r"\newcommand{\resumeSubheading}[4]{")
    tex.append(r"  \vspace{-3pt}\item")
    tex.append(r"    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}")
    tex.append(r"      \textbf{#1} & #2 \\")
    tex.append(r"      \textit{\small#3} & \textit{\small #4} \\")
    tex.append(r"    \end{tabular*}\vspace{-9pt}")
    tex.append(r"}")
    tex.append(r"")
    tex.append(r"\newcommand{\resumeProjectHeading}[2]{")
    tex.append(r"    \item")
    tex.append(r"    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}")
    tex.append(r"      \small#1 & #2 \\")
    tex.append(r"    \end{tabular*}\vspace{-9pt}")
    tex.append(r"}")
    tex.append(r"")
    tex.append(r"\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}")
    tex.append(r"")
    tex.append(r"\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}")
    tex.append(r"\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}")
    tex.append(r"\newcommand{\resumeItemListStart}{\begin{itemize}}")
    tex.append(r"\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}")
    tex.append(r"")
    tex.append(r"\begin{document}")
    tex.append(r"")

    # Header
    name = header['name']
    phone = header['phone']
    email = header['email']
    linkedin = header['linkedin']
    linkedin_url = header['linkedin_url']
    github = header['github']
    github_url = header['github_url']

    tex.append(r"\begin{center}")
    tex.append(f"    \\textbf{{\\Huge \\scshape {name}}} \\\\ \\vspace{{1pt}}")
    tex.append(f"    \\small {phone} $|$ \\href{{mailto:{email}}}{{\\underline{{{email}}}}} $|$ ")
    tex.append(f"    \\href{{{linkedin_url}}}{{\\underline{{{linkedin}}}}} $|$")
    tex.append(f"    \\href{{{github_url}}}{{\\underline{{{github}}}}}")
    tex.append(r"\end{center}")
    tex.append(r"")

    # Education
    tex.append(r"%-----------EDUCATION-----------")
    tex.append(r"\section{Education}")
    tex.append(r"  \resumeSubHeadingListStart")
    for edu in edu_list:
        inst = escape_latex(edu['institution'])
        loc = escape_latex(edu['location'])
        deg = escape_latex(edu['degree'])
        dates = escape_latex(edu['dates'])
        coursework = escape_latex(edu['coursework'])

        tex.append(f"    \\resumeSubheading")
        tex.append(f"      {{{inst}}}{{{loc}}}")
        tex.append(f"      {{{deg}}}{{{dates}}}")
        tex.append(f"      \\resumeItemListStart")
        tex.append(f"        \\resumeItem{{\\textbf{{Relevant Coursework:}} {coursework}}}")
        tex.append(f"      \\resumeItemListEnd")
    tex.append(r"  \resumeSubHeadingListEnd")
    tex.append(r"")

    # Technical Experience
    tex.append(r"%-----------TECHNICAL EXPERIENCE-----------")
    tex.append(r"\section{Technical Experience}")
    tex.append(r"  \resumeSubHeadingListStart")
    for exp_key in config.get("experiences", ["env_science_lab", "caas_care_lab"]):
        if exp_key not in exp_bank:
            continue
        exp = exp_bank[exp_key]
        comp = escape_latex(exp['company'])
        title = escape_latex(exp['title'])
        loc = escape_latex(exp['location'])
        dates = escape_latex(exp['dates'])

        tex.append(f"    \\resumeSubheading")
        tex.append(f"      {{{comp}}}{{{loc}}}")
        tex.append(f"      {{{title}}}{{{dates}}}")
        tex.append(f"      \\resumeItemListStart")
        for bullet in exp['bullets']:
            b_text = escape_latex(bullet['text'])
            tex.append(f"        \\resumeItem{{{b_text}}}")
        tex.append(f"      \\resumeItemListEnd")
    tex.append(r"  \resumeSubHeadingListEnd")
    tex.append(r"")

    # Projects
    tex.append(r"%-----------PROJECTS-----------")
    tex.append(r"\section{Projects}")
    tex.append(r"    \resumeSubHeadingListStart")
    for proj_key in config["projects"]:
        if proj_key not in proj_bank:
            continue
        proj = proj_bank[proj_key]
        p_name = escape_latex(proj['name'])
        p_stack = escape_latex(proj['tech_stack'])
        p_dates = escape_latex(proj['dates'])

        tex.append(f"      \\resumeProjectHeading")
        tex.append(f"          {{\\textbf{{{p_name}}} $|$ \\emph{{{p_stack}}}}}{{{p_dates}}}")
        tex.append(f"          \\resumeItemListStart")
        for bullet in proj['bullets']:
            b_text = escape_latex(bullet['text'])
            tex.append(f"            \\resumeItem{{{b_text}}}")
        tex.append(f"          \\resumeItemListEnd")
    tex.append(r"    \resumeSubHeadingListEnd")
    tex.append(r"")

    # Skills & Interests
    tex.append(r"%-----------SKILLS & INTERESTS-----------")
    tex.append(r"\section{Technical Skills \& Interests}")
    tex.append(r" \begin{itemize}[leftmargin=0.15in, label={}]")
    tex.append(r"    \small{\item{")
    lang = escape_latex(skills['languages'])
    fw = escape_latex(skills['frameworks'])
    tools = escape_latex(skills['tools'])
    dev_ai = escape_latex(skills.get('developer_ai', 'OpenCode, Anti-Gravity CLI, OpenChamber, Gemini API'))
    interests = escape_latex(skills['interests'])

    tex.append(f"     \\textbf{{Languages}}{{: {lang}}} \\\\")
    tex.append(f"     \\textbf{{Frameworks \& Libraries}}{{: {fw}}} \\\\")
    tex.append(f"     \\textbf{{Tools \& Databases}}{{: {tools}}} \\\\")
    tex.append(f"     \\textbf{{Developer Tools \& AI}}{{: {dev_ai}}} \\\\")
    tex.append(f"     \\textbf{{Interests}}{{: {interests}}}")
    tex.append(r"    }}")
    tex.append(r" \end{itemize}")
    tex.append(r"")
    tex.append(r"\end{document}")

    return "\n".join(tex)

def analyze_image_fill(image_path):
    """Calculates vertical fill percentage of printable page height."""
    img = Image.open(image_path).convert('L')
    width, height = img.size
    
    non_white_rows = []
    for y in range(height):
        row = [img.getpixel((x, y)) for x in range(0, width, 5)]
        if min(row) < 240:
            non_white_rows.append(y)
            
    if not non_white_rows:
        return 0.0, 0, 0
        
    top_margin = non_white_rows[0]
    bottom_margin = non_white_rows[-1]
    content_height = bottom_margin - top_margin
    fill_ratio = (content_height / height) * 100.0
    return fill_ratio, top_margin, bottom_margin

from lint_schema import lint_resume_bank

def main(role_key=None):
    ensure_dirs()

    print("==================================================")
    print("RESUME GENERATION & PREVIEW RENDERER")
    print("==================================================")

    # 1. Run automated JSON Schema linting
    if not lint_resume_bank(quiet=False):
        print("\n❌ Build Halted: Fix JSON schema validation errors in 'data/resume_bank.json' before proceeding.")
        sys.exit(1)

    json_path = os.path.join(DATA_DIR, "resume_bank.json")
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    configurations = data.get("configurations", {})
    if role_key:
        if role_key not in configurations:
            print(f"❌ Error: Specified role key '{role_key}' not found in data/resume_bank.json configurations.")
            print(f"Available roles: {', '.join(configurations.keys())}")
            sys.exit(1)
        target_configs = {role_key: configurations[role_key]}
    else:
        target_configs = configurations

    results = []

    for config_key, config in target_configs.items():
        out_name = config["output_filename"]
        tex_path = os.path.join(TEX_DIR, f"{out_name}.tex")
        pdf_path = os.path.join(PDF_DIR, f"{out_name}.pdf")
        png_prefix = os.path.join(PREVIEW_DIR, f"preview_{out_name}")

        print(f"\n---> Building Variant: [{config['title']}] ({out_name}.pdf)")
        tex_content = build_latex_content(data, config_key)
        
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

        # Compile pdflatex into TEX_DIR and move output to PDF_DIR
        cmd_compile = ["pdflatex", f"-output-directory={PDF_DIR}", "-interaction=nonstopmode", tex_path]
        res = subprocess.run(cmd_compile, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"FAILED: pdflatex compilation error for {tex_path}")
            print(res.stdout[-500:])
            continue

        # Render PNG preview at 150 DPI
        cmd_png = ["pdftoppm", "-png", "-r", "150", pdf_path, png_prefix]
        subprocess.run(cmd_png, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        png_path = f"{png_prefix}-1.png"
        
        # Check PDF page count via pdfinfo
        cmd_info = ["pdfinfo", pdf_path]
        info_res = subprocess.run(cmd_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        page_count = 1
        for line in info_res.stdout.splitlines():
            if line.startswith("Pages:"):
                page_count = int(line.split(":")[1].strip())

        fill_pct, top_m, bot_m = analyze_image_fill(png_path) if os.path.exists(png_path) else (0.0, 0, 0)
        
        results.append({
            "variant": config_key,
            "pdf_path": pdf_path,
            "png_path": png_path,
            "pages": page_count,
            "fill_pct": fill_pct
        })

    print("\n==================================================")
    print("COMPILATION SUMMARY & VISUAL RENDER STATUS")
    print("==================================================")
    print(f"{'Variant':<12} | {'PDF Output Location':<30} | {'Pages':<6} | {'Vertical Fill %':<16} | Status")
    print("-" * 85)

    all_passed = True
    for r in results:
        status = "PASSED (1 Page)" if r['pages'] == 1 else "FAILED (Multi-page overflow!)"
        if r['pages'] != 1:
            all_passed = False
        print(f"{r['variant']:<12} | {r['pdf_path']:<30} | {r['pages']:<6} | {r['fill_pct']:<15.1f}% | {status}")

    print("==================================================")
    if all_passed:
        print("All resume variants compiled successfully into build/pdf/ and rendered PNG previews into build/previews/!")

if __name__ == "__main__":
    main()
