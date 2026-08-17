#!/usr/bin/env python3
"""
cv_{lang}.md -> cv_{lang}.typ 변환기 (linked-cv 템플릿 전용)

사용법:
  python3 scripts/md_to_typ.py ko     # cv_ko.md → cv_ko.typ (templates/linked-cv-ko)
  python3 scripts/md_to_typ.py en     # cv_en.md → cv_en.typ (templates/linked-cv)

md 규칙:
  # 이름
  - 직함/Title: ...
  - 전화/Phone: ...
  - 이메일/Email: ...
  - LinkedIn: ...

  (소개 문단)

  ## 경력/Experience
  ### 회사명
  - 기간/Period: ...
  - 직책/Position: ...
  #### 프로젝트명
  - 기간/Period: ...
  - 기술/Tech: ...
  * 불릿
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- 언어별 설정 ----

LANG_CONFIG = {
    "ko": {
        "md": ROOT / "cv_ko.md",
        "typ": ROOT / "cv_ko.typ",
        "template": "templates/linked-cv-ko/lib.typ",
        "sections": {"경력": "career", "학력": "career", "연구 경험": "career"},
        "meta_aliases": {
            "직함": "title", "전화": "phone", "이메일": "email",
            "기간": "period", "직책": "position", "기술": "tech",
            "위치": "location", "학위": "degree",
        },
        "section_career": "경력",
        "section_education": "학력",
        "present_words": ("현재",),
    },
    "en": {
        "md": ROOT / "cv_en.md",
        "typ": ROOT / "cv_en.typ",
        "template": "templates/linked-cv/lib.typ",
        "sections": {"Experience": "career", "Education": "career", "Research": "career"},
        "meta_aliases": {
            "title": "title", "phone": "phone", "email": "email",
            "period": "period", "position": "position", "tech": "tech",
            "location": "location", "degree": "degree",
        },
        "section_career": "Experience",
        "section_education": "Education",
        "present_words": ("present", "Present", "current", "Current"),
    },
}

# 모든 언어에서 공통으로 인식하는 메타 키 (정규화 후의 키)
NORMALIZED_META_KEYS = {"title", "phone", "email", "period", "position", "tech", "location", "degree"}

ICON_ALIASES = {
    "python": "python", "fastapi": "fastapi", "react": "react",
    "redis": "redis", "mongodb": "mongodb", "kubernetes": "kubernetes",
    "k8s": "kubernetes", "docker": "docker",
    "javascript": "javascript", "typescript": "typescript", "go": "go",
    "golang": "go", "mysql": "mysql", "postgresql": "postgressql",
    "postgres": "postgressql", "git": "git", "github": "github",
    "graphql": "graphql", "nginx": "nginx", "rust": "rust",
    "aws": "aws", "azure": "azure", "gcp": "googlecloud",
    "terraform": "terraform", "jenkins": "jenkins",
}

META_BULLET_RE = re.compile(r"^[-*]\s*([^:：]+)\s*[:：]\s*(.+)$")
CONTENT_BULLET_RE = re.compile(r"^[*\-]\s+(.+)$")


# ---- 유틸 ----

def convert_inline(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\*\*(.+?)\*\*", "\x00B\x00\\1\x00B\x00", text)
    text = re.sub(r"`([^`]+)`", "\x00Q\x00\\1\x00Q\x00", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", "\\1", text)
    def esc(s):
        return re.sub(r"([\\#$_@<>\[\]{}])", r"\\\1", s)
    text = esc(text)
    text = text.replace("\x00B\x00", "*")
    text = text.replace("\x00Q\x00", '"')
    return text


def matched_icons(tech_str):
    if not tech_str:
        return []
    items = [t.strip() for t in re.split(r"[,\uff0c]", tech_str) if t.strip()]
    icons = []
    for item in items:
        key = re.sub(r"\s+", "", item).lower()
        if key in ICON_ALIASES and ICON_ALIASES[key] not in icons:
            icons.append(ICON_ALIASES[key])
    return icons


def normalize_date(d, cfg):
    d = d.strip()
    if d in cfg["present_words"] or d.lower() in ("현재", "present", "current"):
        return "current"
    m = re.match(r"^(\d{4})[.\-](\d{1,2})$", d)
    if m:
        return f"{int(m.group(2)):02d}-{m.group(1)}"
    return d


def duration_tuple(period, cfg):
    parts = re.split(r"\s*[-–—]\s*", period, maxsplit=1)
    start = normalize_date(parts[0], cfg)
    end = normalize_date(parts[1], cfg) if len(parts) > 1 else "current"
    return start, end


def split_name(name):
    name = name.strip()
    if len(name) <= 1:
        return name, ""
    # 한글 이름(성 1자 + 이름)인지 판별
    if re.match(r"^[\uac00-\ud7a3]+$", name) and len(name) >= 2:
        return name[1:], name[0]  # firstname(이름), lastname(성)
    # 영문 이름: "First Last"
    parts = name.rsplit(" ", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return name, ""


# ---- 파싱 ----

def normalize_meta_key(raw_key, cfg):
    key = raw_key.strip()
    key_lower = key.lower()
    if key_lower == "linkedin":
        return "linkedin"
    if key in cfg["meta_aliases"]:
        return cfg["meta_aliases"][key]
    if key_lower in cfg["meta_aliases"]:
        return cfg["meta_aliases"][key_lower]
    return None


def parse_block(lines, cfg):
    meta = {}
    bullets = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        m = META_BULLET_RE.match(stripped)
        if m:
            norm = normalize_meta_key(m.group(1), cfg)
            if norm and (norm in NORMALIZED_META_KEYS or norm == "linkedin"):
                meta[norm] = m.group(2).strip()
                continue
        m2 = CONTENT_BULLET_RE.match(stripped)
        if m2:
            bullets.append(m2.group(1).strip())
    return meta, bullets


def split_by_heading(lines, level):
    pattern = re.compile(rf"^{'#' * level}\s+(.+)$")
    blocks = []
    cur_title = None
    cur_body = []
    for line in lines:
        m = pattern.match(line)
        if m:
            if cur_title is not None:
                blocks.append((cur_title, cur_body))
            cur_title = m.group(1).strip()
            cur_body = []
        elif cur_title is not None:
            cur_body.append(line)
    if cur_title is not None:
        blocks.append((cur_title, cur_body))
    return blocks


def split_top(lines):
    header_lines = []
    i = 0
    while i < len(lines) and not re.match(r"^##\s+", lines[i]):
        header_lines.append(lines[i])
        i += 1
    sections = split_by_heading(lines[i:], 2)
    return header_lines, sections


def parse_header(header_lines, cfg):
    name = None
    body_lines = []
    for line in header_lines:
        m = re.match(r"^#\s+(.+)$", line.strip())
        if m and name is None:
            name = m.group(1).strip()
            continue
        body_lines.append(line)
    meta, _ = parse_block(body_lines, cfg)
    intro_lines = [
        ln.strip() for ln in body_lines
        if ln.strip() and not META_BULLET_RE.match(ln.strip())
    ]
    intro = " ".join(intro_lines).strip()
    return {
        "name": name,
        "title": meta.get("title"),
        "phone": meta.get("phone"),
        "email": meta.get("email"),
        "linkedin": meta.get("linkedin"),
        "intro": intro,
    }


def parse_career(section_lines, cfg):
    companies = []
    for company, body in split_by_heading(section_lines, 3):
        first_h4 = next((i for i, l in enumerate(body) if re.match(r"^####\s+", l)), None)
        head_part = body if first_h4 is None else body[:first_h4]
        meta, direct_bullets = parse_block(head_part, cfg)
        projects = []
        if first_h4 is not None:
            for ptitle, pbody in split_by_heading(body[first_h4:], 4):
                pmeta, pbullets = parse_block(pbody, cfg)
                projects.append({
                    "title": ptitle,
                    "period": pmeta.get("period", ""),
                    "tech": pmeta.get("tech", ""),
                    "bullets": pbullets,
                })
        companies.append({
            "company": company,
            "period": meta.get("period", ""),
            "position": meta.get("position", ""),
            "projects": projects,
            "direct_bullets": direct_bullets,
        })
    return companies


# ---- typst 코드 생성 ----

def gen_header(h, cfg):
    firstname, lastname = split_name(h["name"])
    socials_lines = []
    if h["email"]:
        socials_lines.append(f'    email: "{h["email"]}",')
    if h["phone"]:
        socials_lines.append(f'    mobile: "{h["phone"]}",')
    socials_lines.append("    github: none,")
    if h["linkedin"]:
        socials_lines.append(f'    linkedin: "{h["linkedin"]}",')

    out = []
    out.append(f'#import "{cfg["template"]}": *\n')
    out.append("#show: linked-cv.with(")
    out.append(f'  firstname: "{firstname}",')
    out.append(f'  lastname: "{lastname}",')
    out.append("  socials: (")
    out.append("\n".join(socials_lines))
    out.append("  ),")
    out.append('  fonts: (headings: "Pretendard", body: "Pretendard"),')
    out.append(")\n")
    out.append("#set text(size: 8pt, hyphenate: false)")
    out.append("#set par(justify: true, leading: 0.52em)\n")
    if h["title"]:
        out.append(
            '#align(center)[#context text(size: 10pt, weight: "bold", '
            'fill: get-accent-colour())[' + convert_inline(h["title"]) + "]]\n"
        )
    if h["intro"]:
        out.append("#typography.summary[")
        out.append(f"  {convert_inline(h['intro'])}")
        out.append("]\n")
    return "\n".join(out)


def gen_project_block(title, period, bullets, tech):
    lines = []
    display_title = f"{title} ({period})" if period else title
    icons = matched_icons(tech)
    if icons:
        icon_list = ", ".join(f'"{i}"' for i in icons)
        lines.append(
            f'      #components.workstream(title: "{convert_inline(display_title)}", '
            f"tech-stack: ({icon_list},))"
        )
    else:
        lines.append(f'      #typography.workstream("{convert_inline(display_title)}")')
    for b in bullets:
        lines.append(f"      - {convert_inline(b)}")
    if tech:
        lines.append(
            f'      #text(style: "italic", size: 7.5pt, fill: gray)[{convert_inline(tech)}]'
        )
    lines.append("      #v(0.6em)")
    return "\n".join(lines)


def gen_career(companies, section_title, cfg):
    out = [f'#components.section("{convert_inline(section_title)}")\n']
    for idx, c in enumerate(companies):
        cid = re.sub(r"[^a-zA-Z0-9]", "", c["company"]).lower() or f"company{idx}"
        if c["period"]:
            s, e = duration_tuple(c["period"], cfg)
            out.append("#components.employer-info(")
            out.append("  none,")
            out.append(f'  name: "{convert_inline(c["company"])}",')
            out.append(f'  duration: ("{s}", "{e}"),')
            out.append(")\n")
        else:
            out.append(f'#typography.subsection[{convert_inline(c["company"])}]')
            out.append("")
        out.append(f'#frame.connected-frames(\n  "{cid}",')
        out.append("  (")
        out.append(f'    title: [{convert_inline(c["position"] or c["company"])}],')
        if c["period"]:
            s, e = duration_tuple(c["period"], cfg)
            out.append(f'    duration: ("{s}", "{e}"),')
        out.append("    body: [")
        if c["projects"]:
            for p in c["projects"]:
                out.append(gen_project_block(p["title"], p["period"], p["bullets"], p["tech"]))
        else:
            for b in c["direct_bullets"]:
                out.append(f"      - {convert_inline(b)}")
        out.append("    ]")
        out.append("  ),")
        out.append(")\n")
    return "\n".join(out)


def gen_section(section_lines, section_title, cfg):
    """모든 ## 섹션을 동일한 구조로 파싱+렌더링."""
    return gen_career(parse_career(section_lines, cfg), section_title, cfg)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in LANG_CONFIG:
        print(f"Usage: {sys.argv[0]} <ko|en>")
        sys.exit(1)

    lang = sys.argv[1]
    cfg = LANG_CONFIG[lang]

    lines = cfg["md"].read_text(encoding="utf-8").splitlines()
    header_lines, sections = split_top(lines)
    header = parse_header(header_lines, cfg)

    parts = [gen_header(header, cfg)]
    for title, body in sections:
        parts.append(gen_section(body, title, cfg))

    cfg["typ"].write_text("\n".join(parts), encoding="utf-8")
    print(f"[{lang}] Wrote {cfg['typ']}")


if __name__ == "__main__":
    main()
