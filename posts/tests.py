import unittest

from django.conf import settings
from django.test import TestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .models import Post


class PostListTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path=settings.GECKODRIVER_PATH)

    def tearDown(self):
        self.browser.quit()

    def test_can_get_a_list(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('나만의 블로그', self.browser.title)
        # data가 있는 경우
        try:
            post_list = self.browser.find_element_by_id('post-list')
            self.assertNotEqual('', post_list.text)
        # data가 없는 경우
        except NoSuchElementException:
            no_data = self.browser.find_element_by_id('no-data')
            self.assertIn('표시할 내용이 없습니다.', no_data.text)

class PostModelTestCase(TestCase):
    def setUp(self):
        self.post_title = 'Hello, Post'
        self.post = Post(title=self.post_title)

    def test_model_can_create_a_post(self):
        old_count = Post.objects.count()
        self.post.save()
        new_count = Post.objects.count()
        self.assertNotEqual(old_count, new_count)
