#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, shutil, stat, sys
from datetime import datetime, timezone
from pathlib import Path
DIRS=['bin','config','state/cursors','state/audit-ledger','state/approval-receipts','archive/encrypted','archive/manifests','archive/indexes','workspace','workspace/wiki','recovery','logs','lib/hermes_continuity_runtime']
COMMANDS=['hck-validate-runtime','hck-continuity-check','hck-memory-audit-dry-run','hck-archive-dry-run','hck-recovery-refresh','hck-workspace-init','hck-index-rebuild']
PROFILES={'minimal','standard','advanced'}
PLACEHOLDER_CONFIG="# Hermes Agent Continuity Kit runtime config\nprofile: {profile}\nruntime_home: <HCK_RUNTIME_HOME>\ncontinuity_engine:\n  mode: report-only\nmemory_router:\n  default_action: report-only\naudit_ledger:\n  path: state/audit-ledger\nencrypted_archive_pipeline:\n  default_action: dry-run\n  production_requires_approval: true\nrecovery_workbench:\n  decrypt_enabled: false\nknowledge_workspace_adapter:\n  provider: markdown\n  path: workspace/wiki\nknowledge_index:\n  enabled: {knowledge_index_enabled}\n  backend: sqlite-fts-optional\napproval_kernel:\n  require_explicit_approval_for:\n    - archive-production\n    - cursor-advancement\n    - scheduler-enable\n    - decrypt\n"
def repo_root(): return Path(__file__).resolve().parents[1]
def parse_simple_yaml(path):
    data={}
    if not path: return data
    for raw in path.read_text(encoding='utf-8').splitlines():
        line=raw.strip()
        if not line or line.startswith('#') or ':' not in line: continue
        k,v=line.split(':',1); data[k.strip()]=v.strip().strip('"\'')
    return data
def safe_target(path):
    target=Path(path).expanduser().resolve()
    if target==Path('/') or len(str(target))<5: raise SystemExit('installer_result=fail\nreason=unsafe_target')
    return target
def make_wrapper(command):
    action=command.replace('hck-','').replace('-','_')
    return '#!/usr/bin/env sh\nset -eu\nHCK_HOME="${HCK_HOME:-$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)}"\nexport HCK_HOME\nexport PYTHONPATH="$HCK_HOME/lib${PYTHONPATH:+:$PYTHONPATH}"\nexec python3 -B -m hermes_continuity_runtime.continuity_engine '+action+' "$@"\n'
def install(args):
    if args.profile not in PROFILES: print('installer_result=fail\nreason=invalid_profile'); return 2
    target=safe_target(args.target); config_data=parse_simple_yaml(Path(args.config).resolve()) if args.config else {}; profile=config_data.get('profile',args.profile); kie='true' if profile=='advanced' else 'false'
    print(f'installer_profile={profile}'); print(f'installer_target={target}'); print(f'installer_dry_run={str(args.dry_run).lower()}'); print('cron_or_service_enabled=false'); print('archive_created=false'); print('cursor_advanced=false')
    if args.dry_run:
        [print(f'would_create={d}') for d in DIRS]; [print(f'would_install_command={c}') for c in COMMANDS]; print('installer_result=pass'); return 0
    if target.exists() and any(target.iterdir()): print('installer_result=fail\nreason=target_exists_non_empty'); return 3
    for d in DIRS: (target/d).mkdir(parents=True, exist_ok=True)
    src_runtime=repo_root()/'runtime'; dst_runtime=target/'lib/hermes_continuity_runtime'
    for src in src_runtime.glob('*.py'): shutil.copy2(src,dst_runtime/src.name)
    (dst_runtime/'__init__.py').write_text('"""Installed Hermes Agent Continuity Kit runtime."""\n',encoding='utf-8')
    (target/'config/hermes-continuity.yaml').write_text(PLACEHOLDER_CONFIG.format(profile=profile,knowledge_index_enabled=kie),encoding='utf-8')
    receipt={'installed_at':datetime.now(timezone.utc).isoformat(),'profile':profile,'target':'<HCK_RUNTIME_HOME>','cron_or_service_enabled':False,'archive_created':False,'cursor_advanced':False}
    (target/'state/approval-receipts/install-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True),encoding='utf-8')
    for command in COMMANDS:
        out=target/'bin'/command; out.write_text(make_wrapper(command),encoding='utf-8'); out.chmod(out.stat().st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
    install_cmd=target/'bin/hck-install'; install_cmd.write_text('#!/usr/bin/env sh\nset -eu\nexec python3 -B "'+str((repo_root()/'installer/hermes_continuity_installer.py').resolve())+'" "$@"\n',encoding='utf-8'); install_cmd.chmod(0o755)
    print('installer_result=pass'); return 0
def main(argv=None):
    p=argparse.ArgumentParser(description='Install the Hermes Agent Continuity Kit runtime MVP safely.'); p.add_argument('--profile',choices=sorted(PROFILES),default='minimal'); p.add_argument('--target',required=True); p.add_argument('--dry-run',action='store_true'); p.add_argument('--non-interactive',action='store_true'); p.add_argument('--config'); args=p.parse_args(argv)
    if not args.non_interactive: print('installer_result=fail\nreason=non_interactive_required'); return 2
    return install(args)
if __name__=='__main__': sys.exit(main())
