#!/usr/bin/env python3
"""
Generate comprehensive link validation reports in multiple formats.
"""

import json
import csv
from pathlib import Path
import sys
from collections import defaultdict
from typing import Dict, List, Any
from datetime import datetime

DISCOVERY_FILE = Path("website/docs/link-discovery.json")
VALIDATION_FILE = Path("website/docs/link-validation.json")
REPORT_MD = Path("website/docs/link-validation-report.md")
REPORT_JSON = Path("website/docs/link-validation-report.json")
REPORT_CSV = Path("website/docs/link-validation-report.csv")


def generate_markdown_report(discovery_data: Dict, validation_data: Dict) -> str:
    """Generate markdown report."""
    lines = []
    
    lines.append("# Link Validation Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    
    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    summary = validation_data["summary"]
    lines.append(f"- **Total Links**: {summary['total_links']}")
    lines.append(f"- **Total Issues**: {summary['total_issues']}")
    lines.append(f"- **Duplicate Links**: {summary['duplicate_links_count']}")
    lines.append("")
    
    lines.append("### Issues by Severity")
    lines.append("")
    for severity, count in sorted(summary["issues_by_severity"].items()):
        lines.append(f"- **{severity.title()}**: {count}")
    lines.append("")
    
    lines.append("### Issues by Type")
    lines.append("")
    for issue_type, count in sorted(summary["issues_by_type"].items()):
        lines.append(f"- **{issue_type.title()}**: {count}")
    lines.append("")
    
    # Broken Links
    broken_links = [i for i in validation_data["issues"] if i["type"] == "broken"]
    if broken_links:
        lines.append("## Broken Links")
        lines.append("")
        lines.append(f"Found {len(broken_links)} broken links (target file does not exist):")
        lines.append("")
        for issue in broken_links[:50]:  # Limit to first 50
            link = issue["link"]
            lines.append(f"- **{link['source_file']}** (line {link['line']}):")
            lines.append(f"  - Link: `{link['text']}` → `{link['url']}`")
            lines.append(f"  - Issue: {issue['message']}")
            lines.append("")
        if len(broken_links) > 50:
            lines.append(f"... and {len(broken_links) - 50} more broken links")
            lines.append("")
    
    # Path Issues
    path_issues = [i for i in validation_data["issues"] if i["type"] == "path"]
    if path_issues:
        lines.append("## Path Issues")
        lines.append("")
        lines.append(f"Found {len(path_issues)} path issues:")
        lines.append("")
        for issue in path_issues[:50]:
            link = issue["link"]
            lines.append(f"- **{link['source_file']}** (line {link['line']}):")
            lines.append(f"  - Link: `{link['url']}`")
            lines.append(f"  - Issue: {issue['message']}")
            if issue.get("suggestion"):
                lines.append(f"  - Suggestion: `{issue['suggestion']}`")
            lines.append("")
        if len(path_issues) > 50:
            lines.append(f"... and {len(path_issues) - 50} more path issues")
            lines.append("")
    
    # Format Issues
    format_issues = [i for i in validation_data["issues"] if i["type"] == "format"]
    if format_issues:
        lines.append("## Format Issues")
        lines.append("")
        lines.append(f"Found {len(format_issues)} format issues:")
        lines.append("")
        for issue in format_issues[:50]:
            link = issue["link"]
            lines.append(f"- **{link['source_file']}** (line {link['line']}):")
            lines.append(f"  - Link: `{link['url']}`")
            lines.append(f"  - Issue: {issue['message']}")
            if issue.get("suggestion"):
                lines.append(f"  - Suggestion: {issue['suggestion']}")
            lines.append("")
        if len(format_issues) > 50:
            lines.append(f"... and {len(format_issues) - 50} more format issues")
            lines.append("")
    
    # Duplicate Links
    if validation_data["duplicates"]:
        lines.append("## Duplicate Links")
        lines.append("")
        lines.append(f"Found {len(validation_data['duplicates'])} sets of duplicate links:")
        lines.append("")
        for dup in validation_data["duplicates"][:20]:
            lines.append(f"- **{dup['source_file']}**: {dup['count']} links to `{dup['url']}`")
            lines.append("")
        if len(validation_data["duplicates"]) > 20:
            lines.append(f"... and {len(validation_data['duplicates']) - 20} more duplicate sets")
            lines.append("")
    
    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    if broken_links:
        lines.append("1. **Fix Broken Links**: Review and fix all broken links where target files don't exist")
        lines.append("")
    if path_issues:
        lines.append("2. **Fix Path Issues**: Correct paths that point to wrong directories")
        lines.append("")
    if format_issues:
        lines.append("3. **Fix Format Issues**: Convert remaining markdown links to HTML format with relative_url filter")
        lines.append("")
    if validation_data["duplicates"]:
        lines.append("4. **Remove Duplicates**: Consider removing duplicate links from same source files")
        lines.append("")
    
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Run `python website/scripts/fix-comprehensive-links.py --dry-run` to see what can be auto-fixed")
    lines.append("2. Run `python website/scripts/fix-comprehensive-links.py --apply` to apply auto-fixes")
    lines.append("3. Manually review and fix remaining issues")
    lines.append("4. Re-run validation to verify fixes")
    lines.append("")
    
    return "\n".join(lines)


def generate_csv_report(validation_data: Dict) -> List[List[str]]:
    """Generate CSV report."""
    rows = [["Source File", "Line", "Link Text", "Link URL", "Link Type", "Issue Type", "Severity", "Message", "Suggestion"]]
    
    for issue in validation_data["issues"]:
        link = issue["link"]
        rows.append([
            link["source_file"],
            str(link["line"]),
            link["text"],
            link["url"],
            link["type"],
            issue["type"],
            issue["severity"],
            issue["message"],
            issue.get("suggestion", "")
        ])
    
    return rows


def main():
    """Main function."""
    if not DISCOVERY_FILE.exists():
        print(f"Error: Discovery file not found: {DISCOVERY_FILE}", file=sys.stderr)
        print("Please run discover-all-links.py first.", file=sys.stderr)
        sys.exit(1)
    
    if not VALIDATION_FILE.exists():
        print(f"Error: Validation file not found: {VALIDATION_FILE}", file=sys.stderr)
        print("Please run validate-comprehensive-links.py first.", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 60)
    print("Generate Link Validation Reports")
    print("=" * 60)
    
    # Load data
    discovery_data = json.loads(DISCOVERY_FILE.read_text(encoding='utf-8'))
    validation_data = json.loads(VALIDATION_FILE.read_text(encoding='utf-8'))
    
    # Generate Markdown report
    print("Generating Markdown report...")
    md_content = generate_markdown_report(discovery_data, validation_data)
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text(md_content, encoding='utf-8')
    print(f"✓ Saved: {REPORT_MD}")
    
    # Generate JSON report (enhanced version)
    print("Generating JSON report...")
    report_data = {
        "generated": datetime.now().isoformat(),
        "discovery": discovery_data["summary"],
        "validation": validation_data["summary"],
        "issues": validation_data["issues"],
        "duplicates": validation_data["duplicates"]
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(report_data, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"✓ Saved: {REPORT_JSON}")
    
    # Generate CSV report
    print("Generating CSV report...")
    csv_rows = generate_csv_report(validation_data)
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
    print(f"✓ Saved: {REPORT_CSV}")
    
    print(f"\n✅ Reports generated successfully!")
    print(f"\nView reports:")
    print(f"  - Markdown: {REPORT_MD}")
    print(f"  - JSON: {REPORT_JSON}")
    print(f"  - CSV: {REPORT_CSV}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

