import unittest, tempfile, pathlib, subprocess, importlib.util, copy, json
spec=importlib.util.spec_from_file_location('fg',pathlib.Path(__file__).resolve().parents[1]/'scripts/flowguard.py')
f=importlib.util.module_from_spec(spec); spec.loader.exec_module(f)
class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.t.name)
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        self.file=self.root/'arbitrary.language'; self.file.write_text('first\nsecond\n')
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture'],check=True)
        self.r=dict(version=1,target=dict(commit=f.git(self.root,'rev-parse','HEAD'),scope='fixture'),adapters=[],frontier=[dict(trigger='file',question='why',action='read',observation='unknown',next='stop')],coverage=[dict(inspected=['file'],not_inspected=['runtime'])],gaps=[],findings=[dict(id='F1',claim='example',status='hypothesis',severity='high',confidence='low',trigger='input',effect='unknown',evidence=[dict(path=self.file.name,line_start=1,line_end=2,sha256=f.digest(self.file))],counterevidence=[],boundary='source',remedy='verify')],decision=dict(outcome='Insufficient-evidence',rationale='unknown',owner='unassigned'))
    def tearDown(self): self.t.cleanup()
    def test_valid_and_no_mutation(self):
        before=f.snapshot(self.root); self.assertTrue(f.validate(self.r,self.root)); self.assertEqual(before,f.snapshot(self.root))
    def test_stale_evidence(self):
        self.file.write_text('changed'); self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_path_escape(self):
        self.r['findings'][0]['evidence'][0]['path']='../outside'; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_bad_range(self):
        self.r['findings'][0]['evidence'][0]['line_end']=99; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_symlink(self):
        p=self.root/'link'; p.symlink_to(self.file); self.r['findings'][0]['evidence'][0]['path']='link'; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_go_blocked(self):
        self.r['decision']['outcome']='Go'; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_waiver_required(self):
        self.r['decision']['outcome']='Exception'; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_missing_dependencies(self):
        self.assertTrue(all(not x['available'] for x in f.doctor(self.root).values()))
    def test_snapshot_detects_untracked_change(self):
        before=f.snapshot(self.root); (self.root/'untracked').write_text('new'); self.assertNotEqual(before,f.snapshot(self.root))
    def test_gap_owner_required(self):
        self.r['gaps']=[dict(scope='runtime')]; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_frontier_rationale_required(self):
        self.r['frontier']=[{}]; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_adapter_mode_required(self):
        self.r['adapters']=[{}]; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_wrong_commit(self):
        self.r['target']['commit']='0'*40; self.assertRaises(ValueError,f.validate,self.r,self.root)
    def test_snapshot_missing_directory(self):
        self.assertRaises(ValueError, f.snapshot, self.root/'missing')
    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'requires FIFO support')
    def test_snapshot_refuses_special_file(self):
        __import__('os').mkfifo(self.root/'pipe')
        self.assertRaises(ValueError, f.snapshot, self.root)
if __name__=='__main__': unittest.main()
