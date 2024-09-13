from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from .models import Tournament, User
from .enums import StatusChoices

class TournamentViewTestCase(TestCase):
    def setUp(self):
        # Create a user and generate a token for authentication
        self.user = User.objects.create_user(email='testuser@example.com', password='password', username='testuser', alias_name='zort')
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Create sample tournaments
        self.pending_tournament = Tournament.objects.create(name="Pending Tournament", status=StatusChoices.PENDING.value)
        self.finished_tournament = Tournament.objects.create(name="Finished Tournament", status=StatusChoices.FINISHED.value)
        self.progressing_tournament = Tournament.objects.create(name="Progressing Tournament", status=StatusChoices.PROGRESS.value)

    def test_get_pending_tournaments(self):
        response = self.client.get(reverse('tournament-view'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('tournaments', response.data)
        self.assertEqual(len(response.data['tournaments']), 1)
        self.assertEqual(response.data['tournaments'][0]['name'], "Pending Tournament")

    def test_no_pending_tournaments(self):
        Tournament.objects.all().delete()
        response = self.client.get(reverse('tournament-view'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['message'], "No Tournaments available")

    def test_create_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                     data={'action': 'create',
                                        'alias_name': self.user.alias_name,
                                        'tournament_name': 'Test Tournament'})
        self.assertEqual(response.status_code, 201)

    def test_join_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.pending_tournament.id,
                                        'alias_name': self.user.alias_name
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Player joined tournament")

    def test_join_tournament_without_alias(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.pending_tournament.id
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Tournament is full or alias missing")

    def test_join_progressing_tournament(self):
        response = self.client.post(reverse('tournament-view'),
                                    data={
                                        'action': 'join',
                                        'tournament_id': self.progressing_tournament.id,
                                        'alias_name': self.user.alias_name
                                    },
                                    format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Tournament is full or alias missing")

