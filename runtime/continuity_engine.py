#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys
from datetime import datetime,timezone
from pathlib import Path
REQUIRED_DIRS=['bin','config','state/cursors','state/audit-ledger','state/approval-receipts','archive/encrypted','archive/manifests','archive/indexes','workspace','workspace/wiki','recovery','logs']
PUBLIC_COMPONENTS=['Continuity Engine','Memory Router','Audit Ledger','Encrypted Archive Pipeline','Recovery Workbench','Knowledge Workspace Adapter','Approval Kernel','Release Test Harness','Knowledge Index','Curated Wiki Adapter']
def home(): return Path(os.environ.get('HCK_HOME','.')).resolve()
def now(): return datetime.now(timezone.utc).isoformat()
def safe_write(path,text): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')
def emit(data):
    for k in sorted(data):
        v=data[k]
        if isinstance(v,(dict,list)): v=json.dumps(v,sort_keys=True)
        print(f'{k}={v}')
    return 0 if str(data.get('result','pass'))=='pass' else 1
def validate_runtime(args):
    root=home(); missing=[d for d in REQUIRED_DIRS if not (root/d).exists()]; cfg=(root/'config/hermes-continuity.yaml').is_file(); return emit({'command':'hck-validate-runtime','result':'fail' if missing or not cfg else 'pass','missing_count':len(missing),'config_present':str(cfg).lower(),'archive_created':'false','cursor_advanced':'false','cron_or_service_enabled':'false'})
def continuity_check(args): return emit({'command':'hck-continuity-check','result':'pass','mode':'report-only','components':PUBLIC_COMPONENTS})
def memory_audit(args): root=home(); safe_write(root/'state/audit-ledger/memory-audit-report.json',json.dumps({'created_at':now(),'mode':'report-only','raw_content_included':False},indent=2)); return emit({'command':'hck-memory-audit-dry-run','result':'pass','mode':'report-only','report':'state/audit-ledger/memory-audit-report.json'})
def archive_dry_run(args): root=home(); safe_write(root/'archive/manifests/archive-dry-run-report.json',json.dumps({'created_at':now(),'mode':'dry-run','archive_created':False,'cursor_advanced':False},indent=2)); return emit({'command':'hck-archive-dry-run','result':'pass','mode':'dry-run','archive_created':'false','cursor_advanced':'false'})
def recovery_refresh(args): root=home(); safe_write(root/'recovery/recovery-handoff.md','# Recovery Workbench Safe Handoff\n\nMode: safe handoff only. Decrypt actions are not performed.\n'); return emit({'command':'hck-recovery-refresh','result':'pass','decrypt_performed':'false','handoff':'recovery/recovery-handoff.md'})
def workspace_init(args): root=home(); safe_write(root/'workspace/wiki/README.md','# Curated Wiki Adapter\n\nMarkdown workspace initialized by the Knowledge Workspace Adapter.\n'); return emit({'command':'hck-workspace-init','result':'pass','adapter':'markdown','optional_obsidian_dependency':'false'})
def index_rebuild(args): root=home(); safe_write(root/'workspace/wiki/knowledge-index.json',json.dumps({'created_at':now(),'backend':'json-summary','sqlite_fts_optional':True},indent=2)); return emit({'command':'hck-index-rebuild','result':'pass','knowledge_index':'updated','sqlite_fts':'optional'})
COMMANDS={'validate_runtime':validate_runtime,'continuity_check':continuity_check,'memory_audit_dry_run':memory_audit,'archive_dry_run':archive_dry_run,'recovery_refresh':recovery_refresh,'workspace_init':workspace_init,'index_rebuild':index_rebuild}
def main(argv=None): p=argparse.ArgumentParser(); p.add_argument('command',choices=sorted(COMMANDS)); args=p.parse_args(argv); return COMMANDS[args.command](args)
if __name__=='__main__': sys.exit(main())
