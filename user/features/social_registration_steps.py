from allauth.socialaccount.models import SocialApp
from common.lettuce_utils import *

from lettuce import step


@step(u'I register as a Facebook user')
def i_register_as_a_facebook_user(step):
    wait_for_element_with_link_text_to_be_clickable("SIGN IN").click()
    wait_for_element_with_css_selector_to_be_clickable('#md-Login .loginFacebookButton').click()
    clear_and_send_keys(wait_for_element_with_id_to_be_displayed('email'), 'iqbarld_laverdetstein_1446602162@tfbnw.net')
    clear_and_send_keys(wait_for_element_with_id_to_be_displayed('pass'), 'tinville')
    wait_for_element_with_id_to_be_clickable('loginbutton').click()

@step(u'I click the Instagram signin link I should get to the signin page')
def i_register_as_an_instagram_user(step):
    wait_for_element_with_link_text_to_be_clickable("SIGN IN").click()
    wait_for_element_with_css_selector_to_be_clickable('#md-Login .loginInstagramButton').click()
    wait_for_element_with_id_to_be_displayed('id_username')
    wait_for_element_with_id_to_be_displayed('id_password')
    # Can't pursue since there are no test IG users :(

@step(u'I should have a pop-up message saying I have signed in with "([^"]*)"')
def i_register_as_a_facebook_user(step, email):
    wait_for_element_with_class_to_be_displayed('alert')
    assert_selector_contains_text('.alert', email)
    wait_for_element_with_css_selector_to_be_clickable("#messagesModal .close").click()


@step(u'Tinville has the proper Social account connection')
def tinville_has_proper_social_account_connection(step):
    fb = SocialApp(provider='facebook', name='fb', client_id='184315011902646', secret='9434ef88ce2dee7d4917bdcc5fa2d15b')
    fb.save()
    fb.sites.add(1)
    ig = SocialApp(provider='instagram', name='ig', client_id='c9a2b8210c774bca8e89f2742555bc8f', secret='1edc52d41a78442580ac405ebd22ee0d')
    ig.save()
    ig.sites.add(1)