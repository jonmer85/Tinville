from common.lettuce_utils import *


@step(u'Then the zendesk icon should exist')
def then_zendesk_icon_should_exist(step):
    assert_id_exists('launcher')

