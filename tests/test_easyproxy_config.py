import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'subscribe'))
from config.models import ProcessConfig, StorageConfig, StorageItem
from config.legacy import normalize_legacy_config
import push


class EasyProxyConfigTests(unittest.TestCase):
    def fixture(self):
        return {
            'domains': [{'name': 'seed', 'sub': ['https://example.test/sub'], 'push_to': ['public'],
                         'ignorede': True, 'liveness': True, 'rate': 2.5, 'secure': False}],
            'crawl': {'threshold': 5, 'singlelink': True, 'config': {'push_to': ['public']},
                      'persist': {'subs': 'source-cache'},
                      'telegram': {'users': {'channel': {'push_to': ['public'], 'config': {'rename': 'TG-{name}'}}}}},
            'groups': {'public': {'list': True, 'targets': {'clash': 'nodes'}}},
            'storage': {'engine': 'r2', 'account_id': 'account', 'access_key_id': 'test-access',
                        'secret_access_key': 'test-secret', 'domain': 'https://sub.example.test',
                        'items': {'nodes': {'bucket': 'bucket', 'key': 'candidate/run/clash.yaml',
                                            'content_type': 'application/yaml', 'cache_control': 'no-cache'},
                                  'source-cache': {'bucket': 'bucket', 'key': 'internal/sources.json'}}},
        }

    def test_legacy_sources_and_r2_survive_typed_roundtrip(self):
        raw = self.fixture()
        before = copy.deepcopy(raw)
        config = ProcessConfig.parse(raw)
        self.assertEqual(raw, before)
        self.assertEqual(config.sites[0].nodes.subscribe_list(), ['https://example.test/sub'])
        self.assertEqual(config.sites[0].max_rate, 2.5)
        self.assertTrue(config.sites[0].ignore_default_exclude)
        self.assertEqual(config.crawl.persist.subscribe, 'source-cache')
        self.assertEqual(config.crawl.task.push_to, ['public'])
        self.assertEqual(config.crawl.telegram.channels['channel'].task.rename, 'TG-{name}')
        tool = push.get_instance(config.storage)
        config.verify(tool)
        again = ProcessConfig.parse(config.to_dict())
        self.assertEqual(again.to_dict(), config.to_dict())
        self.assertEqual(tool.raw_url(config.storage.items['nodes']), 'https://sub.example.test/candidate/run/clash.yaml')

    def test_new_keys_cannot_silently_override_conflicting_legacy_keys(self):
        with self.assertRaisesRegex(ValueError, 'conflicting'):
            normalize_legacy_config({'domains': [{'name': 'old'}], 'sites': [{'name': 'new'}]})

    @patch.dict('os.environ', {'WORKER_BASE': '', 'TRIGGER_TOKEN': '', 'R2_BUCKET': ''})
    def test_typed_r2_upload_preserves_headers_and_payload(self):
        config = ProcessConfig.parse(self.fixture())
        tool = push.get_instance(config.storage)
        client = Mock()
        tool._client = client
        self.assertTrue(tool.push_to('proxies: []', item=config.storage.items['nodes'], retry=1))
        args, kwargs = client.upload_fileobj.call_args
        self.assertEqual(args[0].getvalue(), b'proxies: []')
        self.assertEqual(args[1:], ('bucket', 'candidate/run/clash.yaml'))
        self.assertEqual(kwargs['ExtraArgs'], {'ContentType': 'application/yaml', 'CacheControl': 'no-cache'})

    def test_r2_does_not_require_unrelated_push_token(self):
        with patch.dict('os.environ', {}, clear=True):
            tool = push.get_instance(StorageConfig(engine='r2', account_id='account', access_key_id='a', secret_access_key='b'))
            self.assertEqual(tool.endpoint, 'https://account.r2.cloudflarestorage.com')
            self.assertTrue(tool.validate(StorageItem(bucket='bucket', key='key')))


if __name__ == '__main__':
    unittest.main()
