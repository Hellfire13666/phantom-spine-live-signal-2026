"""PHANTOM SPINE live public-source orchestrator, versioned and nonintrusive.

Real HTTPS DNS provider requests only; optional existing HEXBAZAAR v0.1.2 bridge.
No browser/cookie/account access or direct target scanning.
"""
from __future__ import annotations
import argparse
import hashlib
import queue
import threading
import ipaddress
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

VERSION = '0.2.0'
BANNER = 'PHANTOM SPINE // LIVE SIGNAL BRIDGE'
HEX_NAME = 'hexbazaar_savage_intel_shop_v0_1_2_rc1.py'
HEX_FOLDER = 'hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_savage'
HEX_OLD = ('hexbazaar-savage-intel-shop-v0_1_0', 'hexbazaar_savage_intel_shop_v0_1_0.py')
RIFT_PATHS = (
    ('riftseal-evidence-forge-2026', 'riftseal_evidence_forge.py'),
    ('riftseal-evidence-forge-v1_0_0', 'riftseal_evidence_forge_v1_0.py'),
)
HEX_PROVIDERS = frozenset(('dns','crtsh','wayback','urlscan','certspotter','ripe'))
COL = {'pink':'\033[95m','teal':'\033[96m','lime':'\033[92m','amber':'\033[93m','reset':'\033[0m'}

class SpineError(Exception): pass

def echo(msg, tint='teal', color='auto'):
    if color == 'always' or (color == 'auto' and sys.stdout.isatty()):
        print(COL.get(tint,'') + msg + COL['reset'], flush=True)
    else:
        print(msg, flush=True)

def header(color):
    echo('╔══════════════════════════════════════════════════════════╗','pink',color)
    echo('║  PHANTOM SPINE // LIVE SIGNAL BRIDGE v0.2.0          ║','teal',color)
    echo('╚══════════════════════════════════════════════════════════╝','pink',color)

def safe_domain(value):
    if not value or value.strip() != value or len(value)>253:
        raise SpineError('Use one public domain such as example.com (not a URL).')
    try: domain=value.encode('idna').decode('ascii').lower()
    except (UnicodeError,ValueError): raise SpineError('Invalid domain') from None
    labels=domain.split('.')
    if len(labels)<2 or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?',x) for x in labels):
        raise SpineError('Invalid public domain. Do not enter a URL, IP or username.')
    if labels[-1] in {'local','internal','localhost','invalid','test','onion'} or labels[-1].isdigit():
        raise SpineError('Only public-style domain names are accepted.')
    try: ipaddress.ip_address(domain)
    except ValueError: pass
    else: raise SpineError('Use a domain name, not an IP address.')
    return domain

def script_file(path):
    try:
        s=path.lstat()
        return stat.S_ISREG(s.st_mode) and not path.is_symlink()
    except OSError: return False

def home_paths(home=None):
    root=Path(home if home is not None else Path.home())/'PhantomLabsLaunchers'
    return {'hex':root/HEX_FOLDER/HEX_NAME,
            'hex_old':root/HEX_OLD[0]/HEX_OLD[1],
            'rift':tuple(root/f/n for f,n in RIFT_PATHS)}

def dns_url(provider,domain,qtype):
    if provider=='google':
        return 'https://dns.google/resolve?' + urlencode({'name':domain,'type':qtype})
    if provider=='cloudflare':
        return 'https://cloudflare-dns.com/dns-query?' + urlencode({'name':domain,'type':qtype})
    raise SpineError('Unknown DNS provider.')

def dns_fetch(provider,domain,qtype,timeout):
    url=dns_url(provider,domain,qtype)
    headers={'User-Agent':'GlitchByte-Phantom-Spine/0.2 (public DNS research)', 'Accept':'application/dns-json'}
    request=Request(url,headers=headers)
    with urlopen(request, timeout=timeout) as response:
        if response.status!=200: raise OSError('Provider returned non-200 HTTP status')
        if not response.geturl().startswith(('https://dns.google/','https://cloudflare-dns.com/')):
            raise OSError('Unexpected DNS redirect')
        body=response.read(160001)
    if len(body)>160000: raise OSError('Provider response exceeds size limit')
    data=json.loads(body.decode('utf-8'))
    if not isinstance(data,dict) or not isinstance(data.get('Status'),int):
        raise ValueError('Unexpected DNS JSON structure')
    return url,data

def valid_answer(row, domain, rtype):
    if not isinstance(row,dict) or row.get('type')!=rtype: return None
    value=row.get('data');name=row.get('name')
    if not isinstance(value,str) or len(value)>253 or not isinstance(name,str): return None
    if name.rstrip('.').lower()!=domain.rstrip('.').lower(): return None
    if rtype in (1,28):
        try:
            addr=ipaddress.ip_address(value)
            return str(addr) if addr.is_global else None
        except ValueError:return None
    if rtype==15:
        parts=value.rstrip('.').split(' ',1)
        if len(parts)!=2 or not parts[0].isdigit():return None
        value=parts[1]
    host=value.rstrip('.').lower()
    try:
        if safe_domain(host)!=host:return None
    except SpineError:return None
    return host

def run_native(domain, timeout, limit, color, fetch=dns_fetch):
    """Query public Google/Cloudflare HTTPS DNS APIs. All output is from responses."""
    echo('◆ ENGINE  LIVE HTTPS DNS • google + cloudflare (no target host requests)','amber',color)
    echo('◆ TARGET  '+domain,'teal',color)
    seen={};success=0;failed=0;start=time.monotonic()
    queries=[('google','A',1),('google','AAAA',28),('google','MX',15),('google','NS',2),
             ('cloudflare','A',1),('cloudflare','AAAA',28)]
    for provider,typ,code in queries:
        t=time.monotonic(); url=dns_url(provider,domain,typ)
        try:
            got_url,data=fetch(provider,domain,typ,timeout)
            # Ground links to the strict expected query URL, not provider-supplied content.
            if got_url!=url:raise ValueError('Unexpected source URL')
            rcode=data['Status']
            answers=data.get('Answer',[])
            if not isinstance(answers,list):raise ValueError('Malformed response')
            if rcode not in (0,3):raise ValueError('DNS response status '+str(rcode))
            success+=1
            new=0
            for row in answers[:200]:
                value=valid_answer(row,domain,code)
                if value is None: continue
                key=(typ,value)
                if key not in seen and len(seen)<limit:
                    seen[key]=[provider]
                    new+=1
                    echo('  ◆ '+typ.ljust(5)+ ' '+value+' | provider='+provider,'teal',color)
                elif key in seen and provider not in seen[key]:
                    seen[key].append(provider)
            echo(f'  [OK] {provider.upper():10} {typ:5} +{new} findings | HTTP 200 / DNS {rcode} | {time.monotonic()-t:.1f}s','lime',color)
            echo('      source: '+url,'teal',color)
        except (OSError,ValueError,TimeoutError,UnicodeError, json.JSONDecodeError) as e:
            failed+=1
            # Do not dump raw child/provider content or credentials in errors.
            echo(f'  [PARTIAL] {provider.upper():10} {typ:5} unavailable ({type(e).__name__}); {time.monotonic()-t:.1f}s','amber',color)
            echo('      source attempted: '+url,'teal',color)
    echo('◆ UNIQUE PUBLIC OBSERVATIONS  '+str(len(seen)),'pink',color)
    echo(f'◆ PROVIDER QUERIES  {success} usable / {failed} failed | elapsed {time.monotonic()-start:.1f}s','amber',color)
    if failed:echo('[PARTIAL] Some public DNS requests were unavailable. Results may be incomplete.','amber',color)
    if not seen:echo('[NOTICE] No public DNS observations were returned. This is not proof of absence.','amber',color)
    echo('[SAVE OFF] No report files. Public observations do not establish identity or wrongdoing.','teal',color)
    return 0 if success else 3

def provider_names(raw):
    a=[p.strip().lower() for p in raw.split(',')]
    if not a or len(set(a))!=len(a) or any(p not in HEX_PROVIDERS for p in a):
        raise SpineError('HEX providers must be distinct: dns,crtsh,wayback,urlscan,certspotter,ripe.')
    return a

def bridge_hex(domain,providers,timeout,limit,color,paths,runner=None):
    tool=paths['hex']
    if not script_file(tool):
        if script_file(paths['hex_old']):
            raise SpineError('Only the legacy HEXBAZAAR adapter was found. Install v0.1.2 for verified command compatibility.')
        raise SpineError('HEXBAZAAR v0.1.2 is missing. Use --engine native --providers dns for actual HTTPS DNS research.')
    terminal_color='always' if color=='auto' and sys.stdout.isatty() else ('never' if color=='auto' else color)
    command=[sys.executable,'-u','-B',str(tool),'--color',terminal_color,'domain',domain,
             '--live','--providers',','.join(providers),'--view','full',
             '--timeout',str(timeout),'--limit',str(limit),'--delay','1']
    echo('◆ ENGINE  INSTALLED HEXBAZAAR v0.1.2 • REAL LIVE PROVIDERS','amber',color)
    echo('◆ TARGET  '+domain,'teal',color)
    echo('◆ STREAM  REAL HEXBAZAAR SOURCE STATUS, PROVENANCE AND FINDINGS','teal',color)
    runner = runner or subprocess.Popen
    try:
        child=runner(command,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,
                     stdin=subprocess.DEVNULL,text=True,bufsize=1)
    except OSError:
        raise SpineError('Could not launch HEXBAZAAR; check tool installation.') from None
    events=queue.Queue(maxsize=400)
    def collect():
        try:
            if child.stdout is not None:
                for line in child.stdout:
                    events.put(line)
        finally:
            events.put(None)
    thread=threading.Thread(target=collect,daemon=True)
    thread.start()
    deadline=time.monotonic()+min(300,max(40,round(len(providers)*(timeout+18)+18)))
    ok_providers=0
    notices=0
    timed_out=False
    while True:
        remaining=deadline-time.monotonic()
        if remaining<=0:
            timed_out=True
            break
        try: line=events.get(timeout=min(1.0,remaining))
        except queue.Empty: continue
        if line is None:break
        print(line,end='',flush=True)
        if re.search(r'\[PASS\]\s+(?:DNS|CRTSH|WAYBACK|URLSCAN|CERTSPOTTER|RIPE)\s+\d+ observations',line):ok_providers+=1
        if re.search(r'\[NOTICE\]\s+(?:DNS|CRTSH|WAYBACK|URLSCAN|CERTSPOTTER|RIPE)',line):notices+=1
    if timed_out:
        child.terminate()
        try: child.wait(timeout=3)
        except subprocess.TimeoutExpired:child.kill();child.wait()
        echo('[TIMEOUT] HEXBAZAAR live process exceeded its bounded wait.','amber',color)
        return 3
    try: exitcode=child.wait(timeout=3)
    except subprocess.TimeoutExpired:
        child.kill();child.wait()
        echo('[TIMEOUT] HEXBAZAAR did not finish cleanly.','amber',color)
        return 3
    if exitcode:
        echo(f'[ERROR] HEXBAZAAR returned status {exitcode}; public provider run incomplete.','amber',color)
        return 3
    if ok_providers==0:
        echo('[PARTIAL] HEXBAZAAR terminated but no provider reported success; this is NOT a live observation PASS.','amber',color)
        return 3
    echo(f'[DONE] HEXBAZAAR finished. {ok_providers} usable provider(s), {notices} notices; see actual observations above.','lime',color)
    echo('[SAVE OFF] No report requested by PHANTOM SPINE.','teal',color)
    return 0

def hash_file(file,color):
    p=Path(file)
    try:
        stat_info=p.lstat()
        if not stat.S_ISREG(stat_info.st_mode) or p.is_symlink():raise SpineError('Choose an ordinary file, not a link or folder.')
        if stat_info.st_size>100_000_000:raise SpineError('100 MB per-file limit; choose a smaller file.')
        s=hashlib.sha256();count=0
        with p.open('rb') as f:
            while True:
                buf=f.read(1024*1024)
                if not buf:break
                count+=len(buf);s.update(buf)
    except OSError:raise SpineError('Selected file could not be read.') from None
    echo('◆ ENGINE  REAL LOCAL FILE FINGERPRINT • NO INTERNET','amber',color)
    echo('◆ SHA256  '+s.hexdigest(),'teal',color)
    echo('◆ BYTES   '+str(count),'teal',color)
    echo('[PASS] Read-only local calculation. No filename printed and no report saved.','lime',color)
    return 0

def rift_bridge(file,color,paths,runner=None):
    rift=next((p for p in paths['rift'] if script_file(p)),None)
    if rift is None:raise SpineError('Installed RIFTSEAL adapter not detected. Use evidence --file to compute a real local fingerprint.')
    # Compute independent local digest, compare with RIFTSEAL output and bytes, never display file paths.
    p=Path(file)
    if not script_file(p):raise SpineError('Select one ordinary, non-symlink file.')
    if p.stat().st_size>100_000_000:raise SpineError('File exceeds 100 MB limit.')
    runner=runner or subprocess.run
    try:
        result=runner([sys.executable,'-B',str(rift),'--file',str(p),'--color','never'],
                      capture_output=True,text=True,timeout=40,check=False)
    except (OSError,subprocess.TimeoutExpired):raise SpineError('RIFTSEAL adapter unavailable or timed out.') from None
    if result.returncode:raise SpineError('RIFTSEAL returned a nonzero exit status.')
    got_sha=re.search(r'\bSHA256\s+([0-9a-f]{64})\b',result.stdout)
    got_size=re.search(r'\bBYTES\s+(\d+)\b',result.stdout)
    if not got_sha or not got_size:raise SpineError('Unexpected RIFTSEAL output format.')
    s=hashlib.sha256();count=0
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            count+=len(block);s.update(block)
    if s.hexdigest()!=got_sha.group(1) or count!=int(got_size.group(1)):
        raise SpineError('RIFTSEAL and PHANTOM SPINE fingerprints do not match.')
    echo('◆ ENGINE  INSTALLED RIFTSEAL VERIFIED AGAINST LOCAL SHA256','amber',color)
    echo('◆ SHA256  '+s.hexdigest(),'teal',color)
    echo('◆ BYTES   '+str(count),'teal',color)
    echo('[PASS] Two matching real calculations. No report or filename displayed.','lime',color)
    return 0

def parser():
    p=argparse.ArgumentParser(prog='phantom-spine-live-v020', description='Real public-source domain intel + local evidence verification; no fabricated results.')
    p.add_argument('--color',choices=('always','auto','never'),default='auto')
    p.add_argument('--version',action='version',version='PHANTOM SPINE LIVE '+VERSION)
    sub=p.add_subparsers(dest='command',required=True)
    h=sub.add_parser('hunt',help='LIVE public-source domain research; makes HTTPS public-provider requests')
    h.add_argument('domain',help='Public domain, e.g. example.com or facebook.com')
    h.add_argument('--engine',choices=('auto','native','hexbazaar'),default='auto',help='auto selects installed v0.1.2 HEXBAZAAR for advanced providers; native is independent DNS')
    h.add_argument('--providers',default='dns',help='dns for native; HEXBAZAAR also supports crtsh,wayback,urlscan,certspotter,ripe')
    h.add_argument('--timeout',type=float,default=5,help='2..15 seconds per public HTTPS provider request')
    h.add_argument('--limit',type=int,default=60,help='1..200 public observations')
    e=sub.add_parser('evidence',help='Genuine local SHA256 calculation; optional installed RIFTSEAL bridge')
    e.add_argument('--file',required=True,help='Read-only local file to fingerprint')
    e.add_argument('--via',choices=('local','riftseal'),default='local')
    sub.add_parser('shop',help='Check optional installed engine compatibility without network')
    sub.add_parser('start',help='Show beginner LIVE commands; does not run until a hunt is selected')
    return p

def main(argv=None,paths=None):
    options=parser().parse_args(argv)
    try:
        header(options.color)
        paths=paths or home_paths()
        if options.command=='shop':
            echo('◆ LIVE NATIVE DNS  READY • actual requests only during hunt','lime',options.color)
            echo('◆ HEXBAZAAR  v0.1.2 '+('FOUND' if script_file(paths['hex']) else 'NOT INSTALLED'),'lime' if script_file(paths['hex']) else 'amber',options.color)
            echo('◆ RIFTSEAL  '+('FOUND' if any(script_file(p) for p in paths['rift']) else 'NOT INSTALLED'),'lime' if any(script_file(p) for p in paths['rift']) else 'amber',options.color)
            echo('◆ LEGACY PHANTOM SPINE  original folders are not modified','teal',options.color)
            echo('[NOTE] Local detection is not a live provider integration test.','amber',options.color)
            return 0
        if options.command=='start':
            echo('◆ 1  LIVE EASY: phantom-spine-live-v020 hunt example.com --engine native','teal',options.color)
            echo('◆ 2  LIVE MEDIUM: phantom-spine-live-v020 hunt facebook.com --engine hexbazaar --providers dns,ripe,certspotter,urlscan','teal',options.color)
            echo('◆ 3  EVIDENCE: phantom-spine-live-v020 evidence --file README.md','teal',options.color)
            echo('◆ HELP: phantom-spine-live-v020 --help','teal',options.color)
            echo('[NOTE] Only hunt commands contact public providers. Start is a command guide.','amber',options.color)
            return 0
        if options.command=='evidence':
            return rift_bridge(options.file,options.color,paths) if options.via=='riftseal' else hash_file(options.file,options.color)
        domain=safe_domain(options.domain)
        echo('◆ REQUEST UTC  '+time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'teal',options.color)
        if not (2<=options.timeout<=15 and options.timeout==options.timeout) or not (1<=options.limit<=200):
            raise SpineError('Use --timeout 2..15 and --limit 1..200.')
        providers=provider_names(options.providers)
        if options.engine=='native' or (options.engine=='auto' and not script_file(paths['hex'])):
            if providers!=['dns']:
                raise SpineError('Native HTTPS engine supports only dns. For other sources, install HEXBAZAAR v0.1.2 and use --engine hexbazaar.')
            if options.engine=='auto':echo('[NOTICE] No HEXBAZAAR v0.1.2; using genuine HTTPS DNS requests.','amber',options.color)
            return run_native(domain,options.timeout,options.limit,options.color)
        return bridge_hex(domain,providers,options.timeout,options.limit,options.color,paths)
    except SpineError as e:
        echo('[STOP] '+str(e),'amber',options.color)
        return 2
    except KeyboardInterrupt:
        echo('[STOP] Interrupted.','amber',options.color)
        return 130

if __name__=='__main__':
    raise SystemExit(main())
