import pprint,json, pytest

from collatorx.common.provider import Provider
from collatorx.providers.coinbase import CoinbaseClient

pp = pprint.pprint

# @pytest.fixture(scope="class")
# def base_provider():
#     '''An instance of Provider base class'''
#     provider = Provider()
#     return provider

# @pytest.fixture
# def base_provider_settings():
#     '''An instance of Provider base class'''
#     return base_provider.settings

def print_values(values):

    if type(values) == dict:
        serialized = json.dumps(values)
        pprint.pprint(serialized)
    else:
        pprint.pprint(values)

def test_base_provider():
    base_provider = Provider()
    
    settings = base_provider.settings

    # pretty print to log
    print_values('Base Settings:')
    print_values(settings)
    
    assert type(settings) == dict
    assert "api_key" in settings
    assert "api_secret" in settings
    assert "api_pass" in settings

def test_coinbase_client():
    coinbase_client = CoinbaseClient()
    
    settings = coinbase_client.settings

    # pretty print to log
    print_values('CoinbaseClient Settings:')
    print_values(settings)

    assert type(settings) == dict
    assert "api_key" in settings
    assert "api_secret" in settings
    assert "api_pass" in settings

    accounts = coinbase_client.accounts
    
    print_values('CoinbaseClient Accounts:')
    print_values(accounts)

    all_accounts_history = coinbase_client.get_all_accounts_history()

    print_values('CoinbaseClient All Accounts History:')
    print_values(all_accounts_history[0:10])


if __name__ == '__main__':

    test_base_provider()
    test_coinbase_provider