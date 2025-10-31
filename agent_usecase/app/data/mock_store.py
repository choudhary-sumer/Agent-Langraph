"""
Mock Data Store

In-memory storage for accounts, facilities, and notes
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta


class MockDataStore:
    """Centralized mock data storage"""

    def __init__(self):
        """Initialize mock data"""
        self._initialize_accounts()
        self._initialize_facilities()
        # Legacy user-based notes (kept for compatibility)
        self.notes: Dict[str, List[Dict[str, Any]]] = {}
        # Account-based notes (preferred)
        self.account_notes: Dict[str, List[Dict[str, Any]]] = {}
        self._initialize_notes()

    def _initialize_accounts(self):
        """Initialize mock account data"""
        self.accounts: Dict[str, Dict[str, Any]] = {
            "A-011977763": {
                "account_id": "A-011977763",
                "name": "Dimod Account",
                "status": "ACTIVE",
                "is_tna": False,
                "created_at": "2025-02-18T04:46:02.486+00:00",
                "pricing_model": "ACCOUNT_LOYALTY",
                "address_line1": "100 WYCLIFFE",
                "address_line2": "",
                "address_city": "IRVINE",
                "address_state": "CA",
                "address_postal_code": "92602-1206",
                "address_country": "",
                "facilities": [
                    {"id": "F-013203268", "name": "TEST Delete Facility", "status": "INACTIVE"},
                    {"id": "F-015766066", "name": "Diamond Facility", "status": "ACTIVE"},
                ],
                "total_amount_due": 0,
                "total_amount_due_this_week": 0,
                "invoice_id": "",
                "invoice_amount": 0,
                "invoice_due_date": "",
                "current_balance": 0,
                "points_earned_this_quarter": 0,
                "pending_balance": 50,
                "current_tier": "Member",
                "next_tier": "silver",
                "points_to_next_tier": 40,
                "quarter_end_date": "2025-09-30T23:59:59-07:00",
                "free_vials_available": 29,
                "rewards_required_for_next_free_vial": 9,
                "rewards_redeemed_towards_next_free_vial": 1,
                "rewards_status": "OPTED_IN",
                "rewards_updated_at": "2025-04-25T13:40:50.176+00:00",
                "evolux_level": "LEVEL_0",
            }
        }

    def _initialize_facilities(self):
        """Initialize mock facility data"""
        self.facilities: Dict[str, Dict[str, Any]] = {
            "F-013203268": {
                "id": "F-013203268",
                "name": "TEST Delete Facility",
                "status": "INACTIVE",
                "has_signed_medical_liability_agreement": True,
                "medical_license_id": "CA-G38840",
                "medical_license_state": "CA",
                "medical_license_number": "G38840",
                "medical_license_involvement": "WORKS_AT_ACCOUNT",
                "medical_license_expiration_date": "2026-09-30T00:00:00.000+00:00",
                "medical_license_is_expired": False,
                "medical_license_status": "Renewed & Current",
                "medical_license_owner_first_name": "GAYLE",
                "medical_license_owner_last_name": "MISLE",
                "account_id": "A-011977763",
                "account_name": "Dimod Account",
                "account_status": "ACTIVE",
                "account_has_signed_financial_agreement": True,
                "account_has_accepted_jet_terms": False,
                "shipping_address_line1": "15035 E 14TH ST",
                "shipping_address_line2": "",
                "shipping_address_city": "SAN LEANDRO",
                "shipping_address_state": "CA",
                "shipping_address_zip": "94578",
                "shipping_address_commercial": True,
                "sponsored": False,
                "agreement_status": "SIGNED",
                "agreement_signed_at": "2025-04-24T05:22:40.173+00:00",
                "agreement_type": "MEDICAL_LIABILITY",
            },
            "F-015766066": {
                "id": "F-015766066",
                "name": "Diamond Facility",
                "status": "ACTIVE",
                "has_signed_medical_liability_agreement": True,
                "medical_license_id": "CA-G38840",
                "medical_license_state": "CA",
                "medical_license_number": "G38840",
                "medical_license_involvement": "WORKS_AT_ACCOUNT",
                "medical_license_expiration_date": "2026-09-30T00:00:00.000+00:00",
                "medical_license_is_expired": False,
                "medical_license_status": "Renewed & Current",
                "medical_license_owner_first_name": "GAYLE",
                "medical_license_owner_last_name": "MISLE",
                "account_id": "A-011977763",
                "account_name": "Dimod Account",
                "account_status": "ACTIVE",
                "account_has_signed_financial_agreement": True,
                "account_has_accepted_jet_terms": False,
                "shipping_address_line1": "15035 E 14TH ST",
                "shipping_address_line2": "",
                "shipping_address_city": "SAN LEANDRO",
                "shipping_address_state": "CA",
                "shipping_address_zip": "94578",
                "shipping_address_commercial": True,
                "sponsored": False,
                "agreement_status": "SIGNED",
                "agreement_signed_at": "2025-02-18T04:51:09.920+00:00",
                "agreement_type": "MEDICAL_LIABILITY",
            },
        }

    def _initialize_notes(self):
        """Seed mock notes for demo/testing"""
        users = [
            "sumer.choudhary@bitcot.com",
            "kaushal.sethia.c@evolus.com",
        ]
        now = datetime.utcnow()
        for u in users:
            self.notes[u] = [
                {
                    "note_id": "N-000001",
                    "user_id": u,
                    "content": "Kickoff call summary: discussed account overview and next steps.",
                    "created_at": now - timedelta(days=5),
                    "updated_at": now - timedelta(days=5),
                },
                {
                    "note_id": "N-000002",
                    "user_id": u,
                    "content": "Follow-up: pending balance and rewards status reviewed.",
                    "created_at": now - timedelta(days=2),
                    "updated_at": now - timedelta(days=2),
                },
                {
                    "note_id": "N-000003",
                    "user_id": u,
                    "content": "Meeting 29/10/2025: confirmed free vials availability.",
                    "created_at": datetime(2025, 10, 29, 10, 0, 0),
                    "updated_at": datetime(2025, 10, 29, 10, 0, 0),
                },
            ]

        self.account_notes["A-011977763"] = [
            {
                "note_id": "AN-000001",
                "user_id": "account:A-011977763",
                "content": "Account kickoff notes.",
                "created_at": now,
                "updated_at": now,
            }
        ]

    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        return self.accounts.get(account_id)

    def get_all_accounts(self) -> List[Dict[str, Any]]:
        return list(self.accounts.values())

    def get_facility(self, facility_id: str) -> Optional[Dict[str, Any]]:
        return self.facilities.get(facility_id)

    def get_all_facilities(self) -> List[Dict[str, Any]]:
        return list(self.facilities.values())

    def save_note(self, account_id: str, content: str) -> Dict[str, Any]:
        if account_id not in self.account_notes:
            self.account_notes[account_id] = []
        note = {
            "note_id": f"AN-{len(self.account_notes[account_id]) + 1:06d}",
            "user_id": f"account:{account_id}",
            "content": content,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        self.account_notes[account_id].append(note)
        return note

    def get_notes(
        self,
        account_id: Optional[str] = None,
        date: Optional[str] = None,
        last_n: int = 5,
        order: str = "desc",
    ) -> List[Dict[str, Any]]:
        all_notes: List[Dict[str, Any]] = []
        if account_id:
            all_notes = self.account_notes.get(account_id, [])
        else:
            for acc_notes in self.account_notes.values():
                all_notes.extend(acc_notes)
        if date:
            all_notes = [
                note for note in all_notes if note["created_at"].strftime("%Y-%m-%d") == date
            ]
        reverse = order != "asc"
        all_notes.sort(key=lambda x: x["created_at"], reverse=reverse)
        return all_notes[:last_n]


# Global instance
mock_store = MockDataStore()


