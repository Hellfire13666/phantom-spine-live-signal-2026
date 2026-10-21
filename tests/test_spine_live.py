from __future__ import annotations
import io
import contextlib
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch
from spine_live import core as s

class LiveSignalTests(unittest.TestCase):
    def test_valid_domains(self):
        self.assertEqual(s.safe_domain('Facebook.com'),'facebook.com')
        self.assertEqual(s.safe_domain('example.com'),'example.com')
        for name in ['http://example.com','evil.com/path','user@facebook.com','foo.test','localhost','192.168.0.1','abc.onion','bad..domain.com','test.local','facebook.com?cookie=x', 'bad-.com']:
            with self.subTest(name=name), self.assertRaises(s.SpineError):s.safe_domain(name)
    def test_fixed_dns_url(self):
        self.assertEqual(s.dns_url('google','example.com','A'), 'https://dns.google/resolve?name=example.com&type=A')
        self.assertTrue(s.dns_url('cloudflare','example.com','AAAA').startswith('https://cloudflare-dns.com/dns-query?'))
    def test_valid_answer_excludes_private_and_email(self):
        self.assertIsNone(s.valid_answer({'type':1,'name':'example.com.','data':'10.0.0.1'},'example.com',1))
        self.assertEqual(s.valid_answer({'type':1,'name':'example.com.','data':'1.1.1.1'},'example.com',1),'1.1.1.1')
        self.assertEqual(s.valid_answer({'type':15,'name':'example.com.','data':'5 mx.example.com.'},'example.com',15),'mx.example.com')
        self.assertIsNone(s.valid_answer({'type':15,'name':'example.com.','data':'5 x@test.com'},'example.com',15))
    def test_real_result_parsing_from_mocked_https(self):
        calls=[]
        def respond(provider,domain,qtype,timeout):
            calls.append((provider,domain,qtype))
            k={'A':1,'AAAA':28,'MX':15,'NS':2}[qtype]
            response={'Status':0,'Answer':[{'type':k,'name':domain+'.','data': {'A':'1.1.1.1','AAAA':'2606:4700:4700::1111','MX':'1 mail.example.com.','NS':'a.ns.example.com.'}[qtype]}]}
            return s.dns_url(provider,domain,qtype),response
        out=io.StringIO()
        with contextlib.redirect_stdout(out): rc=s.run_native('example.com',4,50,'never',fetch=respond)
        self.assertEqual(rc,0)
        self.assertEqual(len(calls),6)
        self.assertIn('1.1.1.1',out.getvalue())
        self.assertIn('https://dns.google/resolve?',out.getvalue())
        self.assertIn('6 usable',out.getvalue())
        self.assertIn('UNIQUE PUBLIC OBSERVATIONS',out.getvalue())
    def test_no_provider_success_returns_failure(self):
        def nope(*args):raise OSError('test mock: no access')
        out=io.StringIO()
        with contextlib.redirect_stdout(out):rc=s.run_native('example.com',3,10,'never',fetch=nope)
        self.assertEqual(rc,3)
        self.assertIn('0 usable / 6 failed',out.getvalue())
        self.assertNotIn('◆ A     1.1.1.1',out.getvalue())
    def test_no_fabricated_result_on_nxdomain(self):
        def nx(provider,domain,qtype,timeout):return s.dns_url(provider,domain,qtype),{'Status':3}
        out=io.StringIO()
        with contextlib.redirect_stdout(out):rc=s.run_native('example.com',3,10,'never',fetch=nx)
        self.assertEqual(rc,0)
        self.assertIn('No public DNS observations',out.getvalue())
    def test_providers_reject_duplicates(self):
        for raw in ['','dns,dns','bad','dns,bad','dns,']:
            with self.assertRaises(s.SpineError):s.provider_names(raw)
    def test_native_refuses_unsupported_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            paths=s.home_paths(temp)
            out=io.StringIO()
            with contextlib.redirect_stdout(out):rc=s.main(['hunt','example.com','--engine','native','--providers','dns,ripe'],paths)
            self.assertEqual(rc,2)
            self.assertIn('supports only dns',out.getvalue())
    def test_detects_hex_new_and_legacy_paths(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'PhantomLabsLaunchers';paths=s.home_paths(td)
            paths['hex_old'].parent.mkdir(parents=True);paths['hex_old'].write_text('old')
            out=io.StringIO()
            with contextlib.redirect_stdout(out):rc=s.main(['hunt','example.com','--engine','hexbazaar'],paths)
            self.assertEqual(rc,2);self.assertIn('legacy HEXBAZAAR',out.getvalue())
            paths['hex'].parent.mkdir(parents=True);paths['hex'].write_text('#new')
            class Child:
                stdout=io.StringIO('  [PASS] DNS       2 observations | ok\n  ◆ www.example.com | sources:dns\n')
                def wait(self,timeout=None): return 0
            calls=[]
            def runner(cmd,**kwargs):
                calls.append(cmd)
                self.assertEqual(kwargs.get('stdout'),s.subprocess.PIPE)
                return Child()
            with contextlib.redirect_stdout(io.StringIO()):rc=s.bridge_hex('example.com',['dns','ripe'],5,35,'never',paths,runner)
            self.assertEqual(rc,0)
            self.assertIn('--live',calls[0]);self.assertIn('--view',calls[0]);self.assertIn('full',calls[0]);self.assertNotIn('--out',calls[0])
            self.assertIn('example.com',calls[0]);self.assertTrue(any('v0_1_2' in x for x in calls[0]))
    def test_hex_all_failed_not_claimed_pass(self):
        with tempfile.TemporaryDirectory() as td:
            script=Path(td)/'hex.py';script.write_text('# fake versioned location only for process adapter test')
            paths={'hex':script, 'hex_old':Path(td)/'missing'}
            class Child:
                stdout=io.StringIO('  [NOTICE] DNS 0 observations | HTTP Error 502\n[NOTICE] Every provider failed or timed out.\n')
                def wait(self,timeout=None):return 0
            out=io.StringIO()
            with contextlib.redirect_stdout(out):rc=s.bridge_hex('example.com',['dns'],3,20,'never',paths,lambda cmd,**kw:Child())
            self.assertEqual(rc,3)
            self.assertIn('NOT a live observation PASS',out.getvalue())

    def test_local_hash_real_data(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'evidence.txt';p.write_bytes(b'real local evidence bytes')
            out=io.StringIO()
            with contextlib.redirect_stdout(out):rc=s.hash_file(str(p),'never')
            self.assertEqual(rc,0)
            self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest(),out.getvalue())
            self.assertNotIn('evidence.txt',out.getvalue())
    def test_rift_bridge_strict_verified_sha(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'local.txt';p.write_text('hello')
            rift=Path(td)/'rift.py';rift.write_text('pass')
            paths={'rift':(rift,)}
            dig=hashlib.sha256(b'hello').hexdigest()
            out=io.StringIO()
            fake=Mock(return_value=SimpleNamespace(returncode=0,stdout=' SHA256 '+dig+'\n BYTES 5\n',stderr=''))
            with contextlib.redirect_stdout(out):self.assertEqual(s.rift_bridge(str(p),'never',paths,runner=fake),0)
            self.assertNotIn('local.txt',out.getvalue())
            fake.return_value=SimpleNamespace(returncode=0,stdout=' SHA256 '+'0'*64+'\n BYTES 5\n',stderr='')
            with self.assertRaises(s.SpineError):s.rift_bridge(str(p),'never',paths,runner=fake)
    def test_start_never_network(self):
        with patch.object(s,'dns_fetch',side_effect=AssertionError('No internet in start')):
            out=io.StringIO()
            with contextlib.redirect_stdout(out):self.assertEqual(s.main(['start']),0)
            self.assertIn('LIVE EASY',out.getvalue())
            self.assertIn('phantom-spine-live-v020 hunt',out.getvalue())

if __name__=='__main__': unittest.main()
