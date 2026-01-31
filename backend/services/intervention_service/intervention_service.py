"""
Intervention Tracking Service
==============================

Service for managing student interventions and tracking their outcomes.
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class InterventionService:
    """Service for intervention tracking and management"""
    
    VALID_STATUSES = ['scheduled', 'in_progress', 'completed', 'cancelled']
    VALID_TYPES = ['meeting', 'counseling', 'mentor', 'academic_support', 
                   'financial_aid', 'attendance_warning', 'other']
    VALID_OUTCOMES = ['positive', 'neutral', 'negative', 'pending']
    
    def __init__(self):
        """Initialize intervention service"""
        self.db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'database',
            'interventions.json'
        )
        self._load_data()
    
    def _load_data(self):
        """Load intervention data from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Interventions file not found, creating new one")
            self.data = {
                'metadata': {
                    'description': 'Intervention tracking database',
                    'last_updated': datetime.now().isoformat(),
                    'next_id': 1
                },
                'interventions': {}
            }
            self._save_data()
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in interventions file")
            self.data = {'metadata': {'next_id': 1}, 'interventions': {}}
    
    def _save_data(self):
        """Save intervention data to JSON file"""
        try:
            self.data['metadata']['last_updated'] = datetime.now().isoformat()
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving interventions: {e}")
            return False
    
    def _get_next_id(self) -> int:
        """Get next intervention ID"""
        next_id = self.data['metadata'].get('next_id', 1)
        self.data['metadata']['next_id'] = next_id + 1
        return next_id
    
    def create_intervention(self, intervention_data: Dict) -> Optional[Dict]:
        """
        Create a new intervention
        
        Args:
            intervention_data: Intervention details
            
        Returns:
            Created intervention with ID or None if failed
        """
        try:
            # Validate required fields
            required_fields = ['student_id', 'type', 'status', 'assigned_to']
            for field in required_fields:
                if field not in intervention_data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate status and type
            if intervention_data['status'] not in self.VALID_STATUSES:
                raise ValueError(f"Invalid status. Must be one of: {self.VALID_STATUSES}")
            
            if intervention_data['type'] not in self.VALID_TYPES:
                raise ValueError(f"Invalid type. Must be one of: {self.VALID_TYPES}")
            
            # Generate ID
            intervention_id = self._get_next_id()
            
            # Create intervention object
            intervention = {
                'id': intervention_id,
                'student_id': intervention_data['student_id'],
                'type': intervention_data['type'],
                'status': intervention_data['status'],
                'assigned_to': intervention_data['assigned_to'],
                'scheduled_date': intervention_data.get('scheduled_date'),
                'completed_date': intervention_data.get('completed_date'),
                'notes': intervention_data.get('notes', ''),
                'outcome': intervention_data.get('outcome', 'pending'),
                'follow_up_date': intervention_data.get('follow_up_date'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            # Save to database
            self.data['interventions'][str(intervention_id)] = intervention
            self._save_data()
            
            return intervention
            
        except Exception as e:
            print(f"Error creating intervention: {e}")
            return None
    
    def get_intervention(self, intervention_id: int) -> Optional[Dict]:
        """
        Get intervention by ID
        
        Args:
            intervention_id: Intervention ID
            
        Returns:
            Intervention data or None if not found
        """
        return self.data['interventions'].get(str(intervention_id))
    
    def get_student_interventions(self, student_id: str) -> List[Dict]:
        """
        Get all interventions for a student
        
        Args:
            student_id: Student roll number
            
        Returns:
            List of interventions
        """
        interventions = []
        for intervention in self.data['interventions'].values():
            if intervention['student_id'] == student_id:
                interventions.append(intervention)
        
        # Sort by created_at (most recent first)
        interventions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return interventions
    
    def update_intervention(self, intervention_id: int, updates: Dict) -> Optional[Dict]:
        """
        Update an intervention
        
        Args:
            intervention_id: Intervention ID
            updates: Fields to update
            
        Returns:
            Updated intervention or None if failed
        """
        try:
            intervention = self.get_intervention(intervention_id)
            if not intervention:
                return None
            
            # Update allowed fields
            allowed_fields = ['status', 'notes', 'outcome', 'completed_date', 
                            'follow_up_date', 'scheduled_date', 'assigned_to']
            
            for field, value in updates.items():
                if field in allowed_fields:
                    intervention[field] = value
            
            # Validate status if updated
            if 'status' in updates and updates['status'] not in self.VALID_STATUSES:
                raise ValueError(f"Invalid status: {updates['status']}")
            
            # Validate outcome if updated
            if 'outcome' in updates and updates['outcome'] not in self.VALID_OUTCOMES:
                raise ValueError(f"Invalid outcome: {updates['outcome']}")
            
            # Auto-set completed_date if status changed to completed
            if updates.get('status') == 'completed' and not intervention.get('completed_date'):
                intervention['completed_date'] = datetime.now().isoformat()
            
            intervention['updated_at'] = datetime.now().isoformat()
            
            # Save to database
            self.data['interventions'][str(intervention_id)] = intervention
            self._save_data()
            
            return intervention
            
        except Exception as e:
            print(f"Error updating intervention: {e}")
            return None
    
    def delete_intervention(self, intervention_id: int) -> bool:
        """
        Delete an intervention
        
        Args:
            intervention_id: Intervention ID
            
        Returns:
            Success status
        """
        try:
            if str(intervention_id) in self.data['interventions']:
                del self.data['interventions'][str(intervention_id)]
                self._save_data()
                return True
            return False
        except Exception as e:
            print(f"Error deleting intervention: {e}")
            return False
    
    def get_all_interventions(self, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Get all interventions with optional filters
        
        Args:
            filters: Optional filters (status, type, assigned_to, etc.)
            
        Returns:
            List of interventions
        """
        interventions = list(self.data['interventions'].values())
        
        if filters:
            if 'status' in filters:
                interventions = [i for i in interventions if i['status'] == filters['status']]
            if 'type' in filters:
                interventions = [i for i in interventions if i['type'] == filters['type']]
            if 'assigned_to' in filters:
                interventions = [i for i in interventions if i['assigned_to'] == filters['assigned_to']]
            if 'student_id' in filters:
                interventions = [i for i in interventions if i['student_id'] == filters['student_id']]
        
        # Sort by created_at (most recent first)
        interventions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return interventions
    
    def get_statistics(self, student_id: Optional[str] = None) -> Dict:
        """
        Get intervention statistics
        
        Args:
            student_id: Optional student ID to filter by
            
        Returns:
            Statistics dictionary
        """
        interventions = self.get_student_interventions(student_id) if student_id else list(self.data['interventions'].values())
        
        total = len(interventions)
        by_status = {}
        by_type = {}
        by_outcome = {}
        
        for intervention in interventions:
            status = intervention['status']
            itype = intervention['type']
            outcome = intervention['outcome']
            
            by_status[status] = by_status.get(status, 0) + 1
            by_type[itype] = by_type.get(itype, 0) + 1
            by_outcome[outcome] = by_outcome.get(outcome, 0) + 1
        
        return {
            'total': total,
            'by_status': by_status,
            'by_type': by_type,
            'by_outcome': by_outcome
        }
    
    def mark_as_contacted(self, student_id: str, contacted_by: str, notes: str = '') -> Optional[Dict]:
        """
        Quick action: Mark student as contacted
        
        Args:
            student_id: Student roll number
            contacted_by: Person who contacted the student
            notes: Optional notes
            
        Returns:
            Created intervention
        """
        intervention_data = {
            'student_id': student_id,
            'type': 'meeting',
            'status': 'completed',
            'assigned_to': contacted_by,
            'completed_date': datetime.now().isoformat(),
            'notes': notes or 'Student contacted',
            'outcome': 'neutral'
        }
        return self.create_intervention(intervention_data)
