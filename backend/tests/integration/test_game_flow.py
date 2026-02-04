"""
Integration tests for complete game flow
"""

import pytest
import json


class TestGameFlow:
    
    def test_start_game(self, client):
        """Test starting a new game"""
        response = client.post('/api/game/start', json={
            'language': 'en',
            'category': 'all'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'session_id' in data['data']
        assert 'question' in data['data']
        assert data['data']['possible_places_count'] > 0
    
    def test_complete_game_flow(self, client):
        """Test complete game from start to guess"""
        # Start game
        response = client.post('/api/game/start', json={
            'language': 'en',
            'category': 'countries'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        session_id = data['data']['session_id']
        
        # Answer questions
        max_questions = 10
        for i in range(max_questions):
            response = client.post('/api/game/answer', json={
                'session_id': session_id,
                'answer': 'yes'
            })
            
            assert response.status_code == 200
            data = json.loads(response.data)
            
            # Should eventually get a guess
            if data['data']['type'] == 'guess':
                assert 'guess' in data['data']
                break
            
            # Otherwise continue with next question
            assert data['data']['type'] == 'question'
    
    def test_invalid_session(self, client):
        """Test answering with invalid session"""
        response = client.post('/api/game/answer', json={
            'session_id': 'invalid-session-id',
            'answer': 'yes'
        })
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_invalid_answer(self, client):
        """Test submitting invalid answer"""
        # Start game first
        response = client.post('/api/game/start', json={
            'language': 'en'
        })
        session_id = json.loads(response.data)['data']['session_id']
        
        # Submit invalid answer
        response = client.post('/api/game/answer', json={
            'session_id': session_id,
            'answer': 'invalid_answer'
        })
        
        assert response.status_code == 400
    
    def test_validate_correct_guess(self, client):
        """Test validating a correct guess"""
        # Start and play game to get a guess
        response = client.post('/api/game/start', json={'language': 'en'})
        session_id = json.loads(response.data)['data']['session_id']
        
        # Answer questions until guess
        for _ in range(10):
            response = client.post('/api/game/answer', json={
                'session_id': session_id,
                'answer': 'yes'
            })
            data = json.loads(response.data)
            if data['data']['type'] == 'guess':
                break
        
        # Validate guess as correct
        response = client.post('/api/game/guess', json={
            'session_id': session_id,
            'correct': True
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['data']['result'] == 'correct'
    
    def test_get_game_state(self, client):
        """Test retrieving game state"""
        # Start game
        response = client.post('/api/game/start', json={'language': 'en'})
        session_id = json.loads(response.data)['data']['session_id']
        
        # Get state
        response = client.get(f'/api/game/state/{session_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'session_id' in data['data']
        assert 'status' in data['data']
    
    def test_end_game(self, client):
        """Test ending a game session"""
        # Start game
        response = client.post('/api/game/start', json={'language': 'en'})
        session_id = json.loads(response.data)['data']['session_id']
        
        # End game
        response = client.delete(f'/api/game/end/{session_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True