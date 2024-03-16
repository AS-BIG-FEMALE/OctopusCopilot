import unittest

from domain.strings.sanitized_list import sanitize_list, sanitize_environments, sanitize_projects, sanitize_tenants, \
    sanitize_feeds, sanitize_accounts, sanitize_workerpools, sanitize_machinepolicies, sanitize_tenanttagsets, \
    sanitize_projectgroups, sanitize_channels, sanitize_releases, sanitize_lifecycles, sanitize_certificates, \
    sanitize_targets, sanitize_runbooks


class SanitizeList(unittest.TestCase):
    def test_sanitize_projects(self):
        self.assertFalse(sanitize_projects("Project A"))
        self.assertFalse(sanitize_projects("ProjectA"))
        self.assertFalse(sanitize_projects("Project1"))
        self.assertFalse(sanitize_projects("MyProject"))
        self.assertFalse(sanitize_projects("My Project"))
        self.assertTrue(sanitize_projects("Valid project"))

    def test_sanitize_tenants(self):
        self.assertFalse(sanitize_tenants("TenantA"))
        self.assertFalse(sanitize_tenants("Tenant A"))
        self.assertFalse(sanitize_tenants("Tenant 1"))
        self.assertFalse(sanitize_tenants("MyTenant"))
        self.assertFalse(sanitize_tenants("My Tenant"))
        self.assertTrue(sanitize_tenants("Valid tenant"))

    def test_sanitize_feeds(self):
        self.assertFalse(sanitize_feeds("FeedA"))
        self.assertFalse(sanitize_feeds("Feed A"))
        self.assertFalse(sanitize_feeds("Feed 1"))
        self.assertFalse(sanitize_feeds("MyFeed"))
        self.assertFalse(sanitize_feeds("My Feed"))
        self.assertTrue(sanitize_feeds("Valid Feed"))

    def test_sanitize_accounts(self):
        self.assertFalse(sanitize_accounts("AccountA"))
        self.assertFalse(sanitize_accounts("Account A"))
        self.assertFalse(sanitize_accounts("Account 1"))
        self.assertFalse(sanitize_accounts("MyAccount"))
        self.assertFalse(sanitize_accounts("My Account"))
        self.assertTrue(sanitize_accounts("Valid Account"))

    def test_sanitize_channels(self):
        self.assertFalse(sanitize_channels("ChannelA"))
        self.assertFalse(sanitize_channels("Channel A"))
        self.assertFalse(sanitize_channels("Channel 1"))
        self.assertFalse(sanitize_channels("MyChannel"))
        self.assertFalse(sanitize_channels("My Channel"))
        self.assertTrue(sanitize_channels("Valid Channel"))

    def test_sanitize_releases(self):
        self.assertFalse(sanitize_releases("ReleaseA"))
        self.assertFalse(sanitize_releases("Release A"))
        self.assertFalse(sanitize_releases("Release 1"))
        self.assertFalse(sanitize_releases("MyRelease"))
        self.assertFalse(sanitize_releases("My Release"))
        self.assertTrue(sanitize_releases("Valid Release"))

    def test_sanitize_lifecycles(self):
        self.assertFalse(sanitize_lifecycles("LifecycleA"))
        self.assertFalse(sanitize_lifecycles("Lifecycle A"))
        self.assertFalse(sanitize_lifecycles("Lifecycle 1"))
        self.assertFalse(sanitize_lifecycles("MyLifecycle"))
        self.assertFalse(sanitize_lifecycles("My Lifecycle"))
        self.assertTrue(sanitize_lifecycles("Valid Lifecycle"))

    def test_sanitize_certificates(self):
        self.assertFalse(sanitize_certificates("CertificateA"))
        self.assertFalse(sanitize_certificates("Certificate A"))
        self.assertFalse(sanitize_certificates("Certificate 1"))
        self.assertFalse(sanitize_certificates("MyCertificate"))
        self.assertFalse(sanitize_certificates("My Certificate"))
        self.assertTrue(sanitize_certificates("Valid Certificate"))

    def test_sanitize_runbooks(self):
        self.assertFalse(sanitize_runbooks("RunbookA"))
        self.assertFalse(sanitize_runbooks("Runbook A"))
        self.assertFalse(sanitize_runbooks("Runbook 1"))
        self.assertFalse(sanitize_runbooks("MyRunbook"))
        self.assertFalse(sanitize_runbooks("My Runbook"))
        self.assertTrue(sanitize_runbooks("Valid Runbook"))

    def test_sanitize_targets(self):
        self.assertFalse(sanitize_targets("TargetA"))
        self.assertFalse(sanitize_targets("Target A"))
        self.assertFalse(sanitize_targets("Target 1"))
        self.assertFalse(sanitize_targets("MyTarget"))
        self.assertFalse(sanitize_targets("My Target"))
        self.assertFalse(sanitize_targets("MachineA"))
        self.assertFalse(sanitize_targets("Machine A"))
        self.assertFalse(sanitize_targets("Machine 1"))
        self.assertFalse(sanitize_targets("MyMachine"))
        self.assertFalse(sanitize_targets("My Machine"))
        self.assertTrue(sanitize_targets("Valid Target"))

    def test_sanitize_workerpools(self):
        self.assertFalse(sanitize_workerpools("WorkerPoolA"))
        self.assertFalse(sanitize_workerpools("WorkerPool A"))
        self.assertFalse(sanitize_workerpools("Worker Pool A"))
        self.assertFalse(sanitize_workerpools("WorkerPool 1"))
        self.assertFalse(sanitize_workerpools("Worker Pool 1"))
        self.assertFalse(sanitize_workerpools("MyWorkerPool"))
        self.assertFalse(sanitize_workerpools("MyWorker Pool"))
        self.assertFalse(sanitize_workerpools("My Worker Pool"))
        self.assertTrue(sanitize_workerpools("Valid Worker Pool"))

    def test_sanitize_machinepolicies(self):
        self.assertFalse(sanitize_machinepolicies("MachinePolicyA"))
        self.assertFalse(sanitize_machinepolicies("MachinePolicy A"))
        self.assertFalse(sanitize_machinepolicies("Machine Policy A"))
        self.assertFalse(sanitize_machinepolicies("MachinePolicy 1"))
        self.assertFalse(sanitize_machinepolicies("Machine Policy 1"))
        self.assertFalse(sanitize_machinepolicies("MyMachinePolicy"))
        self.assertFalse(sanitize_machinepolicies("My MachinePolicy"))
        self.assertFalse(sanitize_machinepolicies("My Machine Policy"))
        self.assertTrue(sanitize_machinepolicies("Valid MachinePolicy"))

    def test_sanitize_tenanttagsets(self):
        self.assertFalse(sanitize_tenanttagsets("TagSetA"))
        self.assertFalse(sanitize_tenanttagsets("TagSet A"))
        self.assertFalse(sanitize_tenanttagsets("Tag Set A"))
        self.assertFalse(sanitize_tenanttagsets("TagSet 1"))
        self.assertFalse(sanitize_tenanttagsets("Tag Set 1"))
        self.assertFalse(sanitize_tenanttagsets("MyTagSet"))
        self.assertFalse(sanitize_tenanttagsets("My TagSet"))
        self.assertFalse(sanitize_tenanttagsets("My Tag Set"))
        self.assertTrue(sanitize_tenanttagsets("Valid Tag Set"))

    def test_sanitize_projectgroups(self):
        self.assertFalse(sanitize_projectgroups("ProjectGroupA"))
        self.assertFalse(sanitize_projectgroups("ProjectGroup A"))
        self.assertFalse(sanitize_projectgroups("Project Group A"))
        self.assertFalse(sanitize_projectgroups("ProjectGroup 1"))
        self.assertFalse(sanitize_projectgroups("Project Group 1"))
        self.assertFalse(sanitize_projectgroups("MyProjectGroup"))
        self.assertFalse(sanitize_projectgroups("My ProjectGroup"))
        self.assertFalse(sanitize_projectgroups("My Project Group"))
        self.assertTrue(sanitize_projectgroups("Valid Project Group"))

    def test_sanitize_list(self):
        self.assertFalse(sanitize_list("Machine A", "Machine\\s*[A-Za-z0-9]"))
        self.assertFalse(sanitize_list(["*"], "\\*"))
        self.assertFalse(sanitize_list([" ", "  ", "   "]))
        self.assertTrue(sanitize_list([" ", "  ", "  i "]))
        self.assertFalse(sanitize_list([]))
        self.assertFalse(sanitize_list(None))
        self.assertFalse(sanitize_list(5))
        self.assertFalse(sanitize_list([5]))
        self.assertFalse(sanitize_list(5.5))
        self.assertFalse(sanitize_list([5.5]))
        self.assertFalse(sanitize_list(True))
        self.assertFalse(sanitize_list([True]))
        self.assertFalse(sanitize_list([[True]]))
        self.assertEqual(0, len(sanitize_list(None)))
        self.assertFalse(sanitize_list(""))
        self.assertFalse(sanitize_list(" "))
        self.assertFalse(sanitize_list("Machine A", "Machine"))
        self.assertTrue(sanitize_list("Machine A", "^Machine$"))
        self.assertTrue(sanitize_list("hi"))
        self.assertTrue(sanitize_list(["hi"]))
        self.assertFalse(sanitize_list([["hi"]]))
        self.assertFalse(sanitize_environments(None))
