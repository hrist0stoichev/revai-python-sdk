# -*- coding: utf-8 -*-
"""Unit tests for SentimentAnalysisClient"""

import pytest
from src.rev_ai.sentiment_analysis_client import SentimentAnalysisClient
from src.rev_ai import __version__
from src.rev_ai import Transcript, Monologue, Element, InsightsJob, JobStatus, \
    SentimentAnalysisResult, SentimentValue, SentimentMessage

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

TOKEN = 'token'
TEXT = 'Input'
JSON = Transcript([Monologue(0, [Element('text', 'hello', 0.0, 0.1, 100)])])
JOB_ID = '1'
METADATA = 'test'
CALLBACK_URL = 'https://example.com/'
CREATED_ON = '2018-05-05T23:23:22.29Z'
LANGUAGE = 'en'
SCORE = 1
CONTENT = 'random words'
OFFSET = 0
LENGTH = 12


class TestSentimentAnalysisClient:
    def test_constructor_with_success(self):
        client = SentimentAnalysisClient(TOKEN)

        headers = client.default_headers

        assert headers.get('User-Agent') == 'RevAi-PythonSDK/{}'.format(__version__)
        assert headers.get('Authorization') == 'Bearer {}'.format(TOKEN)
        assert client.base_url == 'https://api.rev.ai/sentiment_analysis/v1/'

    @pytest.mark.parametrize('token', [None, ''])
    def test_constructor_with_no_token(self, token):
        with pytest.raises(ValueError, match='access_token must be provided'):
            SentimentAnalysisClient(token)

    def test_submit_job_text_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_text(text=TEXT,
                                          metadata=METADATA,
                                          callback_url=CALLBACK_URL,
                                          delete_after_seconds=0,
                                          language=LANGUAGE)

        assert res == InsightsJob(JOB_ID,
                                  CREATED_ON,
                                  JobStatus.IN_PROGRESS,
                                  metadata=METADATA,
                                  callback_url=CALLBACK_URL,
                                  delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'text': TEXT,
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_submit_job_json_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs')
        data = {
            'id': JOB_ID,
            'status': 'in_progress',
            'created_on': CREATED_ON,
            'metadata': METADATA,
            'callback_url': CALLBACK_URL,
            'delete_after_seconds': 0,
            'language': LANGUAGE,
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.submit_job_from_transcript(transcript=JSON,
                                                metadata=METADATA,
                                                callback_url=CALLBACK_URL,
                                                delete_after_seconds=0,
                                                language=LANGUAGE)

        assert res == InsightsJob(JOB_ID,
                                  CREATED_ON,
                                  JobStatus.IN_PROGRESS,
                                  metadata=METADATA,
                                  callback_url=CALLBACK_URL,
                                  delete_after_seconds=0)
        mock_session.request.assert_called_once_with(
            "POST",
            url,
            json={
                'json': JSON.to_dict(),
                'callback_url': CALLBACK_URL,
                'metadata': METADATA,
                'delete_after_seconds': 0,
                'language': LANGUAGE
            },
            headers=client.default_headers)

    def test_get_result_json_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'messages': [
                {
                    'content': CONTENT,
                    'score': SCORE,
                    'sentiment': SentimentValue.NEGATIVE.value,
                    'offset': OFFSET,
                    'length': LENGTH
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_json(JOB_ID)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_json_with_threshold_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{0}/result?filter_for={1}'
                      .format(JOB_ID, SentimentValue.NEGATIVE.value))
        data = {
            'messages': [
                {
                    'content': CONTENT,
                    'score': SCORE,
                    'sentiment': SentimentValue.NEGATIVE.value,
                    'offset': OFFSET,
                    'length': LENGTH
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_json(JOB_ID, SentimentValue.NEGATIVE)

        assert res == data
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{}/result?'.format(JOB_ID))
        data = {
            'messages': [
                {
                    'content': CONTENT,
                    'score': SCORE,
                    'sentiment': SentimentValue.NEGATIVE.value,
                    'offset': OFFSET,
                    'length': LENGTH
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID)

        assert res == SentimentAnalysisResult(
            [SentimentMessage(
                CONTENT,
                SCORE,
                SentimentValue.NEGATIVE,
                offset=OFFSET,
                length=LENGTH
            )]
        )
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)

    def test_get_result_object_with_threshold_with_success(self, mock_session, make_mock_response):
        client = SentimentAnalysisClient(TOKEN)
        url = urljoin(client.base_url, 'jobs/{0}/result?filter_for={1}'
                      .format(JOB_ID, SentimentValue.POSITIVE.value))
        data = {
            'messages': [
                {
                    'content': CONTENT,
                    'score': SCORE,
                    'sentiment': SentimentValue.POSITIVE.value,
                    'offset': OFFSET,
                    'length': LENGTH
                }
            ]
        }
        response = make_mock_response(url=url, json_data=data)
        mock_session.request.return_value = response

        res = client.get_result_object(JOB_ID, SentimentValue)

        assert res == SentimentAnalysisResult(
            [SentimentMessage(
                CONTENT,
                SCORE,
                SentimentValue.POSITIVE,
                offset=OFFSET,
                length=LENGTH
            )]
        )
        mock_session.request.assert_called_once_with(
            "GET",
            url,
            headers=client.default_headers)