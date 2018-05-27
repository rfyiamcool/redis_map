from redis_map import RedisDict

if __name__ == '__main__':
    import time

    d = RedisDict(namespace='app_name')
    assert 'random' not in d
    d['random'] = 4
    assert d['random'] == '4'
    assert 'random' in d
    del d['random']
    assert 'random' not in d
    deep = ['key', 'key1', 'key2']
    deep_val = 'mister'
    d.chain_set(deep, deep_val)

    assert deep_val == d.chain_get(deep)
    d.chain_del(deep)

    try:
        d.chain_get(deep)
    except KeyError:
        pass
    except Exception:
        print('failed to throw KeyError')
    else:
        print('failed to throw KeyError')

    assert 'random' not in d
    d['random'] = 4
    dd = RedisDict(namespace='app_name_too')
    assert len(dd) == 0

    dd['random'] = 5

    assert d['random'] == '4'
    assert 'random' in d

    assert dd['random'] == '5'
    assert 'random' in dd

    del d['random']
    assert 'random' not in d

    assert dd['random'] == '5'
    assert 'random' in dd

    del dd['random']
    assert 'random' not in dd

    with dd.expire_at(1):
        dd['gone_in_one_sec'] = 'gone'

    assert dd['gone_in_one_sec'] == 'gone'

    time.sleep(1.1)

    try:
        dd['gone_in_one_sec']
    except KeyError:
        pass
    except Exception:
        print('failed to throw KeyError')
    else:
        print('failed to throw KeyError')

    assert len(dd) == 0

    items = {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}
    for key, val in items.items():
        dd.chain_set(['keys', key], val)

    assert len(dd) == len(items)
    assert sorted(dd.multi_get('keys')) == sorted(list(items.values()))
    assert dd.multi_dict('keys') == items

    dd['one_item'] = 'im here'
    dd.multi_del('keys')

    assert len(dd) == 1

    del(dd['one_item'])
    assert len(dd) == 0

    print('all is well')
